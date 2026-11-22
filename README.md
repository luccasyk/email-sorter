Automação da Classificação e Organização de E-mails

Projeto Integrador – Laboratório de Programação Curso: Análise e Desenvolvimento de Sistemas – UNISA

1. Sobre o projeto

Programa em Python que classifica e organiza mensagens de e-mail com base em palavras-chave presentes no assunto e no remetente.

As regras de classificação ficam fora do código, no arquivo rules.json, o que permite alterar categorias e palavras-chave sem mexer no programa.

O programa possui dois modos de execução:

Simulação (padrão): classifica as mensagens e mostra o resultado, sem alterar a caixa de entrada.
Aplicação (--aplicar): move de fato as mensagens para as pastas correspondentes.

Arquivos do projeto
Arquivo	Descrição

organize.py - Código-fonte principal da aplicação.
rules.json - Regras de classificação (categorias e palavras-chave).
relatorio.csv - Gerado automaticamente após a execução com --aplicar, registrando as movimentações.
Formato do rules.json

O arquivo é uma lista de regras. Cada regra tem:

pasta: nome da pasta de destino da mensagem.
palavras: lista de palavras-chave procuradas no assunto e no remetente.

[
    {
        "pasta": "Financeiro",
        "palavras": ["fatura", "boleto", "pagamento", "cobrança", "mensalidade", "reembolso"]
    },
    {
        "pasta": "Cotacoes",
        "palavras": ["cotacao", "orçamento", "proposta", "apolice"]
    }
]

Para criar uma nova categoria, basta adicionar um novo bloco com pasta e palavras. Não é preciso alterar o código.

3. Requisitos
Python 3 instalado no computador.
Conta de e-mail com acesso IMAP habilitado.
Credenciais de acesso, usando senha de aplicativo quando o provedor exigir.

Não são necessárias bibliotecas externas: o programa usa apenas módulos da biblioteca padrão do Python.

4. Configuração

O programa lê as credenciais por variáveis de ambiente, para que nenhuma senha fique no código:
