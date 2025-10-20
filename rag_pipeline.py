from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGChatbot:
    def __init__(self, api_key: str, vector_store):
        if not vector_store:
            raise ValueError("Vektör veritabanı (vector_store) sağlanmadı veya yüklenemedi.")
        
        self.vector_store = vector_store
        
        print("Dil modeli (LLM) başlatılıyor...")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            google_api_key=api_key
        )
        
        print("RAG zinciri oluşturuluyor...")
        self.rag_chain = self._create_rag_chain()
        print("Chatbot başarıyla başlatıldı ve hazır.")

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _create_rag_chain(self):
        prompt = PromptTemplate.from_template(
            """
            Size verilen konteks bilgilerini kullanarak soruyu cevaplayın. Cevaplarınızı bilgilendirici ve finansal tavsiye vermeden, ansiklopedik bir dille sunun. Eğer cevabı bilmiyorsanız, bilmediğinizi söyleyin, cevap uydurmaya çalışmayın.
            Konteks: {context}
            Soru: {question}
            Cevap:
            """
        )
        retriever = self.vector_store.as_retriever()
        return (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str):
        return self.rag_chain.invoke(question)