

# Gerekli modüllerimizi import ediyoruz
from data_processing import process_documents
from vector_store_manager import VectorStoreManager
from rag_pipeline import RAGChatbot

# --- Ayarlar ---
GOOGLE_API_KEY = "AIzaSyAWjaFDSBd8kRG2AnkKntJ_thkOoY3bby0"
DATA_PATH = "data"
INDEX_PATH = "faiss_index"

def main():
    # API anahtarının girilip girilmediğini kontrol et
    if not GOOGLE_API_KEY:
        print("Lütfen 'app.py' dosyasına Google API anahtarınızı girin.")
        return

    # Vektör veritabanı yöneticisini başlat
    vsm = VectorStoreManager(index_path=INDEX_PATH)

    # Veritabanı diskte mevcut değilse, baştan oluştur
    if not vsm.exists():
        print(f"'{INDEX_PATH}' bulunamadı. Veri işleme ve veritabanı oluşturma süreci başlatılıyor...")
        
        # 1. Dokümanları işle (oku ve parçalara ayır)
        chunks = process_documents(directory_path=DATA_PATH)
        
        # 2. Vektör veritabanını oluştur ve diske kaydet
        if chunks:
            vsm.create_and_save(chunks)
        else:
            print("İşlenecek doküman bulunamadı. Lütfen 'data' klasörünü kontrol edin.")
            return

    # Mevcut veya yeni oluşturulmuş veritabanını yükle
    vector_store = vsm.load()
    if not vector_store:
        print("Vektör veritabanı yüklenemedi. Program sonlandırılıyor.")
        return
    
    # RAG Chatbot'u başlat
    try:
        chatbot = RAGChatbot(api_key=GOOGLE_API_KEY, vector_store=vector_store)
        
        print("\n--- Finansal Okuryazarlık Chatbot ---")
        print("Soru sormaya başlayabilirsiniz. Çıkmak için 'exit' yazın.")

        # Kullanıcı arayüzünü başlat
        while True:
            user_question = input("\nSorunuz: ")
            if user_question.lower() == 'exit':
                print("Görüşmek üzere!")
                break
            
            response = chatbot.ask(user_question)
            print("\nCevap:", response)
    except Exception as e:
        print(f"Chatbot başlatılırken bir hata oluştu: {e}")


if __name__ == "__main__":
    main()