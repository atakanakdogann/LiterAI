import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents_from_directory(directory_path: str):
    """Belirtilen klasördeki tüm .pdf ve .docx dosyalarını okur."""
    documents = []
    print(f"'{directory_path}' klasöründeki dokümanlar okunuyor...")
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if filename.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif filename.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
        except Exception as e:
            print(f"'{filename}' okunurken bir hata oluştu: {e}")
            continue
    print(f"Toplam {len(documents)} sayfa/doküman okundu.")
    return documents

def split_documents(documents: list):
    """Gelen dokümanları parçalara ayırır."""
    print("Dokümanlar parçalara ayrılıyor...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)
    print(f"Dokümanlar toplam {len(split_docs)} parçaya (chunk) ayrıldı.")
    return split_docs

def process_documents(directory_path: str = "data"):
    """
    Verilen yoldaki dokümanları yükler ve işler.
    Ana fonksiyon olarak bu kullanılır.
    """
    documents = load_documents_from_directory(directory_path)
    if not documents:
        return []
    chunks = split_documents(documents)
    return chunks