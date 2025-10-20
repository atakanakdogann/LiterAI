import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStoreManager:
    def __init__(self, index_path="faiss_index"):
        self.index_path = index_path
        print("Embedding modeli yükleniyor...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        print("Embedding modeli başarıyla yüklendi.")

    def create_and_save(self, chunks: list):
        """Verilen parçalardan bir vektör veritabanı oluşturur ve kaydeder."""
        if not chunks:
            print("Oluşturulacak parça (chunk) bulunamadı. İşlem atlanıyor.")
            return
        print("Vektör veritabanı oluşturuluyor...")
        try:
            vector_store = FAISS.from_documents(documents=chunks, embedding=self.embeddings)
            vector_store.save_local(self.index_path)
            print(f"Vektör veritabanı '{self.index_path}' klasörüne başarıyla kaydedildi.")
        except Exception as e:
            print(f"Vektör veritabanı oluşturulurken hata oluştu: {e}")

    def load(self):
        """Kaydedilmiş vektör veritabanını yükler."""
        if not self.exists():
            return None
        print(f"'{self.index_path}' adresindeki vektör veritabanı yükleniyor...")
        try:
            return FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Vektör veritabanı yüklenirken hata oluştu: {e}")
            return None

    def exists(self) -> bool:
        """Vektör veritabanının diskte var olup olmadığını kontrol eder."""
        return os.path.exists(self.index_path)