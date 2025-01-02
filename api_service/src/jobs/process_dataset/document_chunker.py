import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.utils.file_path import chunk_file_path
from jobs.utils.general import load_from_pickle, dump_to_pickle


def chunk_document(document):
    chunk_size = 1000
    chunk_overlap = 200
    doc_chunker = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return doc_chunker.split_documents(document)


def persist_chunks(chunks, topic_slug):
    file_path = chunk_file_path(topic_slug=topic_slug)
    if os.path.exists(file_path):
        data = load_from_pickle(file_path)
        data = data + chunks
        dump_to_pickle(data=data, path=file_path)
    else:
        dump_to_pickle(data=chunks, path=file_path)


def load_chunks(topic_slug):
    chunks = load_from_pickle(path=chunk_file_path(topic_slug=topic_slug))
    return chunks
