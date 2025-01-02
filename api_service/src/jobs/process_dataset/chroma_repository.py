import spacy
from faker import Faker
from langchain_community.vectorstores.chroma import Chroma

from config import REPLACE_PII_WITH_FAKE_DATA, HIDE_PII, PII_ENTITIES, CHROMA_PATH
from core.loggers import task_logger as logger
from core.utils.file_path import delete_topic_directory
from jobs.process_dataset.document_chunker import persist_chunks
from jobs.process_dataset.embedder import get_embedding_object


def get_nlp_model():
    return spacy.load('en_core_web_sm')


def get_fake_data(label, faker_obj):
    if label == 'PERSON':
        return faker_obj.name()
    elif label == 'GPE':
        return faker_obj.city()
    elif label == 'ORG':
        return faker_obj.company()
    elif label == 'DATE':
        return faker_obj.date()
    elif label == 'TIME':
        return faker_obj.time()
    elif label == 'MONEY':
        return f"${faker_obj.random_number(digits=5)}"
    elif label == 'PHONE':
        return faker_obj.phone_number()
    elif label == 'EMAIL':
        return faker_obj.email()
    else:
        return '[MASKED]'


def anonymize_content(documents):
    nlp = get_nlp_model()
    faker_obj = Faker()
    for document in documents:
        doc = nlp(document.page_content)
        for ent in doc.ents:
            if ent.label_ in PII_ENTITIES:
                if REPLACE_PII_WITH_FAKE_DATA:
                    fake_data = get_fake_data(label=ent.label_, faker_obj=faker_obj)
                    document.page_content = document.page_content.replace(ent.text, fake_data)
                else:
                    document.page_content = document.page_content.replace(ent.text, '[MASKED]')
    return documents


def get_chroma_client(collection):
    embedding_function = get_embedding_object()
    return Chroma(collection_name=collection, embedding_function=embedding_function,
                  persist_directory=CHROMA_PATH)


def delete_collection_data(collection):
    chroma_client = get_chroma_client(collection)
    chroma_client.delete_collection()
    delete_topic_directory(topic_slug=collection)


def add_id_to_all_chunks(chunks, filename):
    last_page_id = None
    current_chunk_id = 0
    logger.info("Assigning id to chunks")
    for chunk in chunks:
        # there are three parts to this id
        # 1. filename
        # 2. page number
        # 3. chunk id
        page = chunk.metadata.get("page", 0)
        current_page_id = f"{filename}:{page}"

        # if the page id is the same as last one, increment the chunk id
        if current_page_id == last_page_id:
            current_chunk_id += 1
        else:
            current_chunk_id = 0

        # Add the chunk id to the current page id
        chunk_id = f"{current_page_id}:{current_chunk_id}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks


def get_new_chunks(db, collection, chunks):
    # get existing chunks in the specified collection of the db
    existing_chunks_in_db = db.get()
    print("existing chunks", existing_chunks_in_db)
    new_chunks = []
    if len(existing_chunks_in_db["metadatas"]) == 0:
        logger.info(f"There are no previously existing chunks for the collection {collection}")
        new_chunks = chunks
    else:
        metadata_of_all_chunks_in_db = existing_chunks_in_db["metadatas"]
        ids_of_all_chunks_in_db = set()
        for metadata in metadata_of_all_chunks_in_db:
            ids_of_all_chunks_in_db.add(metadata["id"])
        for chunk in chunks:
            if chunk.metadata["id"] not in ids_of_all_chunks_in_db:
                logger.info(f"A new chunk to be inserted - {chunk.metadata}")
                new_chunks.append(chunk)
    return new_chunks


def persist_embeddings(topic_slug, chunks, filename):
    db = get_chroma_client(collection=topic_slug)
    chunks = add_id_to_all_chunks(chunks, filename)
    new_chunks = get_new_chunks(db=db, collection=topic_slug, chunks=chunks)

    if len(new_chunks) > 0:
        if HIDE_PII:
            new_chunks = anonymize_content(documents=new_chunks)
        db.add_documents(new_chunks)
        persist_chunks(topic_slug=topic_slug, chunks=chunks)
        logger.info("Persisted the chunks in file and the embeddings in the vector store")
    else:
        logger.info("There are no new chunks")
