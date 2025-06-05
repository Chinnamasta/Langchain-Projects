from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from langchain_core.utils.function_calling import convert_to_openai_function

# --- 1. Definições Pydantic para as Funções ---

# Enum para tipos de e-mail
class TipoEmailEnum(str, Enum):
    todos = 'todos'
    nao_lidos = 'não lidos'
    lidos = 'lidos'

# Enum para status de marcação
class StatusMarcacaoEnum(str, Enum):
    lido = 'lido'
    nao_lido = 'não lido'

# Modelo para a função obter_emails
class ObterEmailsInput(BaseModel):
    """Obtém emails com base no tipo (todos, não lidos, lidos), quantidade, remetente e palavras-chave."""
    tipo: TipoEmailEnum = Field(description="O tipo de emails a serem obtidos: 'todos', 'não lidos' ou 'lidos'.")
    quantidade: int = Field(description="O número de emails que você deseja obter.")
    remetente: Optional[str] = Field(None, description="Opcional: Filtrar emails enviados por um remetente específico.")
    palavras_chave: Optional[str] = Field(None, description="Opcional: Filtrar emails que contenham estas palavras-chave no assunto ou conteúdo.")

# Modelo para a função marcar_email_lido
class MarcarEmailLidoInput(BaseModel):
    """Marca um email como lido ou não lido."""
    id_email: int = Field(description="O ID único do email a ser marcado.")
    status: StatusMarcacaoEnum = Field(description="O status para o qual o email deve ser marcado: 'lido' ou 'não lido'.")

# Modelo para a função enviar_email
class EnviarEmailInput(BaseModel):
    """Envia um novo email para um destinatário."""
    destinatario: str = Field(description="O endereço de email do destinatário.")
    assunto: str = Field(description="O assunto do email.")
    conteudo: str = Field(description="O corpo do email.")


# Converte os modelos Pydantic para ferramentas do LangChain
tool_obter_emails = convert_to_openai_function(ObterEmailsInput)
tool_marcar_email_lido = convert_to_openai_function(MarcarEmailLidoInput)
tool_enviar_email = convert_to_openai_function(EnviarEmailInput)


# --- 2. Simulação de um Banco de Dados de E-mails (Substitui a lista simples) ---

emails_simulados_db = [
    {"id": 1, "assunto": "Reunião de equipe", "lido": True, "conteudo": "Olá, a reunião será amanhã às 10h. Atenciosamente, Ana.", "remetente": "ana@exemplo.com"},
    {"id": 2, "assunto": "Convite: Happy Hour", "lido": False, "conteudo": "Vamos nos encontrar hoje à noite no bar do Zé? Abraços, Pedro.", "remetente": "pedro@exemplo.com"},
    {"id": 3, "assunto": "Notificação de entrega", "lido": True, "conteudo": "Seu pedido #123 foi entregue. Obrigado, Loja ABC.", "remetente": "lojaabc@exemplo.com"},
    {"id": 4, "assunto": "Lembrete: Pagamento da Fatura", "lido": False, "conteudo": "Não se esqueça de pagar sua fatura com vencimento em 07/06. Att, Financeiro.", "remetente": "financeiro@exemplo.com"},
    {"id": 5, "assunto": "Novidades do blog de tecnologia", "lido": False, "conteudo": "Confira nossos últimos artigos sobre IA e Python. Equipe Tech.", "remetente": "blog@tech.com"},
    {"id": 6, "assunto": "Confirmar presença no evento", "lido": True, "conteudo": "Por favor, confirme sua presença no evento até sexta. Grato, Organização.", "remetente": "organizacao@evento.com"},
    {"id": 7, "assunto": "Urgente: Projeto X", "lido": False, "conteudo": "Precisamos discutir o Projeto X com urgência. Disponibilidade para hoje? Abs, Carlos.", "remetente": "carlos@exemplo.com"},
]

# --- 3. Funções Principais do Assistente de E-mail ---

def obter_emails(tipo: str, quantidade: int, remetente: Optional[str] = None, palavras_chave: Optional[str] = None):
    """
    Simula a obtenção de emails com base no tipo, quantidade, remetente e palavras-chave.
    Em um cenário real, esta função se conectaria a um serviço de e-mail (ex: imaplib para Gmail).
    """
    print(f"\n--- Solicitando Emails ---")
    print(f"Tipo: '{tipo}', Quantidade: {quantidade}")
    if remetente:
        print(f"Filtrar por Remetente: '{remetente}'")
    if palavras_chave:
        print(f"Filtrar por Palavras-chave: '{palavras_chave}'")

    emails_filtrados_status = []
    if tipo == 'todos':
        emails_filtrados_status = emails_simulados_db
    elif tipo == 'não lidos':
        emails_filtrados_status = [email for email in emails_simulados_db if not email["lido"]]
    elif tipo == 'lidos':
        emails_filtrados_status = [email for email in emails_simulados_db if email["lido"]]
    else:
        return {"erro": "Tipo de email inválido."}

    # Filtrar por remetente (se fornecido)
    if remetente:
        emails_filtrados_status = [
            email for email in emails_filtrados_status
            if email["remetente"].lower() == remetente.lower()
        ]

    # Filtrar por palavras-chave (se fornecidas)
    if palavras_chave:
        termos = [term.strip().lower() for term in palavras_chave.split(',')]
        emails_filtrados_status = [
            email for email in emails_filtrados_status
            if any(term in email["assunto"].lower() or term in email["conteudo"].lower() for term in termos)
        ]

    # Retornar a quantidade desejada de e-mails
    return emails_filtrados_status[:quantidade]

def marcar_email_lido(id_email: int, status: str):
    """
    Simula a marcação de um email como lido ou não lido.
    Em um cenário real, isso envolveria uma requisição à API do serviço de e-mail.
    """
    print(f"\n--- Solicitando Marcação de Email ---")
    for email in emails_simulados_db:
        if email["id"] == id_email:
            email["lido"] = (status == 'lido') # Converte 'lido'/'não lido' para True/False
            print(f"Email ID {id_email} marcado como: {'Lido' if email['lido'] else 'Não Lido'}.")
            return {"status": "sucesso", "mensagem": f"Email ID {id_email} marcado como {status}."}
    print(f"Erro: Email com ID {id_email} não encontrado.")
    return {"status": "erro", "mensagem": f"Email com ID {id_email} não encontrado."}

def enviar_email(destinatario: str, assunto: str, conteudo: str):
    """
    Simula o envio de um novo email.
    Em um cenário real, isso usaria a biblioteca smtplib do Python ou uma API de e-mail.
    """
    print(f"\n--- Solicitando Envio de Email ---")
    print(f"Para: {destinatario}")
    print(f"Assunto: {assunto}")
    print(f"Conteúdo: {conteudo[:50]}...") # Exibe só um pedaço do conteúdo
    # Em um sistema real, aqui o email seria realmente enviado.
    print("Email simulado enviado com sucesso!")
    return {"status": "sucesso", "mensagem": "Email simulado enviado."}


# --- 4. Exemplos de Uso das Novas Funções (Para você testar!) ---

if __name__ == "__main__":
    print("--- Testando as funções do Assistente de E-mail ---")

    # Teste de obter_emails
    print("\n--- TESTE 1: Obter 2 emails não lidos ---")
    emails_nao_lidos = obter_emails(tipo='não lidos', quantidade=2)
    for email in emails_nao_lidos:
        print(f"- Assunto: {email['assunto']} (Remetente: {email['remetente']}, Lido: {email['lido']})")

    print("\n--- TESTE 2: Obter 1 email de 'ana@exemplo.com' ---")
    emails_ana = obter_emails(tipo='todos', quantidade=1, remetente='ana@exemplo.com')
    for email in emails_ana:
        print(f"- Assunto: {email['assunto']} (Remetente: {email['remetente']}, Lido: {email['lido']})")

    print("\n--- TESTE 3: Obter emails com 'projeto' ou 'urgencia' ---")
    emails_proj_urg = obter_emails(tipo='todos', quantidade=3, palavras_chave='projeto, urgencia')
    for email in emails_proj_urg:
        print(f"- Assunto: {email['assunto']} (Remetente: {email['remetente']}, Lido: {email['lido']})")

    print("\n--- TESTE 4: Obter emails não lidos com 'fatura' ou 'pagamento' ---")
    emails_fatura = obter_emails(tipo='não lidos', quantidade=2, palavras_chave='fatura, pagamento')
    for email in emails_fatura:
        print(f"- Assunto: {email['assunto']} (Remetente: {email['remetente']}, Lido: {email['lido']})")

    # Teste de marcar_email_lido
    print("\n--- TESTE 5: Marcar email ID 2 como lido ---")
    marcar_email_lido(id_email=2, status='lido')
    # Vamos verificar se ele foi marcado
    print("\nVerificando email ID 2 após a marcação:")
    email_verificado = next((e for e in emails_simulados_db if e["id"] == 2), None)
    if email_verificado:
        print(f"Email ID 2 (Assunto: {email_verificado['assunto']}) está Lido: {email_verificado['lido']}")

    # Teste de enviar_email
    print("\n--- TESTE 6: Enviar um email simulado ---")
    enviar_email(destinatario='destino@novo.com', assunto='Olá do Assistente Python', conteudo='Este é um email de teste enviado pelo meu assistente pessoal em Python.')

    print("\n--- Fim dos Testes ---")