from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

chat = ChatOpenAI(model='gpt-4o-mini', openai_api_key="SUA_CHAVE_DE_API_AQUI")

texto_ingles_rh = """
Artificial intelligence (AI) is revolutionizing various aspects of Human Resources (HR).
From automating recruitment processes to enhancing employee engagement, AI offers significant benefits.
For instance, AI-powered tools can screen resumes more efficiently, identify top candidates, and reduce hiring bias.
Furthermore, AI chatbots can answer employee queries, freeing up HR staff for more strategic tasks.
Predictive analytics driven by AI can also help in identifying employees at risk of leaving, allowing HR to take proactive measures.
Overall, AI is transforming HR into a more data-driven and efficient function.
"""

print(f"Texto original em inglês sobre RH e IA: {texto_ingles_rh}")

# Chain tradutor
prompt_traducao_rh = ChatPromptTemplate.from_template('Traduza o texto entre ### para português: ###{texto}###')
translator_rh = prompt_traducao_rh | chat | StrOutputParser()

# Chain Resumo do texto
prompt_resumo_rh = ChatPromptTemplate.from_template('Faça o resumo do seguinte texto em 15 palavras: {texto_traduzido}')
summarizer_rh = prompt_resumo_rh | chat | StrOutputParser()

# Chain combinada
chain_combinada_rh = translator_rh | summarizer_rh

resultado_rh = chain_combinada_rh.invoke({"texto": texto_ingles_rh})

print(f"Texto traduzido e resumido sobre RH e IA: {resultado_rh}")
