import streamlit as st

# Agent and LLM
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ConversationalAgent
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# Memory
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
# Tools
from langchain.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities import YouSearchAPIWrapper
from langchain_community.tools.you import YouSearchTool
import re
import os


st.title("Assistente virtual de Saude 🩺")

################################################## 3. Definição das Chaves da API e Ferramentas

GEMINI_API_KEY_PRO = os.getenv("GEMINI_API_KEY_PRO")
SERPER_API_KEY = os.getenv("SERPER_API_KEY") 
YDC_API_KEY = os.getenv("YDC_API_KEY")

search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
search_you = YouSearchAPIWrapper(ydc_api_key=YDC_API_KEY,
                                  num_web_results=1)

triagem = YouSearchTool(api_wrapper=search_you)
################################################## 4. Definindo as Ferramentas para o Agente

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="ferramenta de busca de informações referente o COVID",
    ),
    Tool(
        name="screening",
        func=triagem.run,
        description="Identificar sintomas e diagnosticar o usuario com as possiveis infermidades",
    )
]

################################################## 5. Configuração do Prompt do Agente

prefix = """ Você é um planejador moderno e amigável.
Você pode ajudar os usuários a diagnosticar sintomas do COVID e tambem especialista em 
informações relacionadas.
Você tem acesso às duas ferramentas:
"""

suffix = """
Chat History:
{chat_history}
Latest Question: {input}
{agent_scratchpad}
"""

prompt = ConversationalAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input",
                     "chat_history",
                     "agent_scratchpad"],
)


################################################## 6. Configuração de Memória do Agente

msg = StreamlitChatMessageHistory()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        messages=msg,
        memory_key="chat_history",
        return_messages=True # retorna todas as mensagens
    )
memory = st.session_state.memory


################################################## 7. Configuração do LLM (Modelo de Linguagem)

llm_chain = LLMChain(
    llm=ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY_PRO,
                               temperature=0.8, 
                               model="gemini-1.5-pro"),
    prompt=prompt,
    verbose=True
)

################################################## 8. Configuração do Agente Conversacional

agent = ConversationalAgent(
    llm_chain=llm_chain,
    memory=memory,
    verbose=True,
    max_interactions=3,
    tools=tools
)

################################################## 9. Configuração do Executor do Agente

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                    tools=tools,
                                                    memory=memory,
                                                    verbose=True)


################################################## 10. Interação com o Usuário

query = st.text_input("Como posso ajudar você hoje?", placeholder="Digite aqui...")

if query:
    with st.spinner("Estou pensando..."):
        result = agent_executor.run(query)
        st.info(result, icon="🤖")




################################################## 11. Exibição do Histórico de Chat
import json
with st.expander("Historico do Chat..."):
        for texto in memory.chat_memory.messages:
             if texto.type.upper() == "HUMAN":
                st.markdown(f"**👤 {texto.type.upper()}**: {texto.content.upper()}")
             elif texto.type.upper() == "AI":
            # Ícone de robô para 'AI'
                st.markdown(f"**🤖 {texto.type.upper()}**: {texto.content}")

