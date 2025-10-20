import streamlit as st
from data_processing import process_documents
from rag_pipeline import RAGChatbot 
from vector_store_manager import VectorStoreManager # EKLENDİ

# --- Ayarlar ---
INDEX_PATH = "faiss_index"
DATA_PATH = "data"

@st.cache_resource
def load_rag_chatbot():
    """
    RAGChatbot sınıfını yalnızca bir kez yükler ve hafızada tutar.
    Bu, her kullanıcı etkileşiminde modelin yeniden yüklenmesini önler.
    """
    try:
        vsm = VectorStoreManager(index_path=INDEX_PATH)

        if not vsm.exists():
            print(f"'{INDEX_PATH}' bulunamadı. Veri işleme ve veritabanı oluşturma süreci başlatılıyor...")
            
            chunks = process_documents(directory_path=DATA_PATH)
            
            if chunks:
                vsm.create_and_save(chunks)
            else:
                print("İşlenecek doküman bulunamadı. Lütfen 'data' klasörünü kontrol edin.")
                return

        vector_store = vsm.load()
        if not vector_store:
            print("Vektör veritabanı yüklenemedi. Program sonlandırılıyor.")
            return None
        
        chatbot = RAGChatbot(api_key=st.secrets["GOOGLE_API_KEY"], vector_store=vector_store)
        return chatbot

    except Exception as e:
        st.error(f"Chatbot başlatılırken beklenmedik bir hata oluştu: {e}")
        return None


st.set_page_config(page_title="Finansal Okuryazarlık Chatbot", page_icon="💰")
st.title("💰 Finansal Okuryazarlık Chatbot")
st.caption("Kendi belgelerinizden beslenen RAG tabanlı yapay zeka asistanı")

chatbot = load_rag_chatbot()

if chatbot:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Örn: Faiz nedir?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Cevap oluşturuluyor..."):
            response = chatbot.ask(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
else:
    st.warning("Chatbot yüklenemedi. Lütfen terminaldeki hata mesajlarını kontrol edin.")