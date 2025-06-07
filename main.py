from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from email_tool import envia_email
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
tools = [envia_email]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Exemplo de chamada
agent.run("Envie um e-mail para destinatario=teste@exemplo.com; titulo=Olá; corpo=Isso é um teste.")

