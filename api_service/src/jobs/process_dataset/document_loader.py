from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader


def load_documents(path: str):
    loader = None
    if path.endswith(".txt"):
        loader = TextLoader(path)
    elif path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".doc") or path.endswith(".docx"):
        loader = Docx2txtLoader(path)
    elif path.endswith(".csv"):
        loader = CSVLoader(path)
    else:
        raise Exception("Unsupported file format")
    return loader.load()
