# Primeiro, importamos a biblioteca 'csv'. 
# Pense nela como uma caixa de ferramentas do Python para criar planilhas.
import csv

# Criamos uma lista com os utensílios que encontramos na receita.
# Uma lista em Python é como uma lista de compras de verdade.
utensilios = ["liquidificador", "tigela", "batedeira", "colher", "forno"]

# Agora, fazemos o mesmo para os ingredientes.
ingredientes = ["cenoura", "ovos", "óleo", "açúcar", "farinha de trigo", "fermento", "manteiga", "chocolate em pó", "leite"]

# --- Função para salvar qualquer lista em CSV ---
def salvar_csv(lista, nome_arquivo, nome_coluna):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow([nome_coluna])
        for item in lista:
            escritor.writerow([item])

# --- Criando os arquivos 'utensilios.csv' e 'ingredientes.csv' ---
salvar_csv(utensilios, "utensilios.csv", "Utensilio")
salvar_csv(ingredientes, "ingredientes.csv", "Ingrediente")

# --- Criando o arquivo 'lista_de_compras.csv' com campo para Quantidade ---
with open('lista_de_compras.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerow(["Ingrediente", "Quantidade"])
    for item in ingredientes:
        escritor.writerow([item, ""])  # Deixa a quantidade em branco para preencher depois

print("Tudo pronto! Criei os arquivos 'utensilios.csv', 'ingredientes.csv' e 'lista_de_compras.csv' para você.")

# --- Simulação de um Agente de Compras com IA ---
print("\n🤖 Iniciando agente de compras inteligente...\n")
for ingrediente in ingredientes:
    print(f"🔎 Verificando necessidade do item: '{ingrediente}'...")
    print(f"✅ '{ingrediente}' adicionado à lista de compras!\n")

print("🛒 Lista de compras finalizada. Preparando envio ao supermercado virtual...")
print("📦 Pedido pronto para checkout!\n")
print("🚀 Agente de compras finalizado com sucesso.")
