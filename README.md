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

Variável	Descrição	Obrigatória
EMAIL_USER	Endereço da conta de e-mail.	Sim
EMAIL_APP_PASSWORD	Senha de aplicativo.	Sim
EMAIL_IMAP_HOST	Servidor IMAP (padrão: imap.gmail.com).	Não

Windows (PowerShell):

powershell
$env:EMAIL_USER="seuemail@gmail.com"
$env:EMAIL_APP_PASSWORD="sua_senha_de_aplicativo"
$env:EMAIL_IMAP_HOST="imap.gmail.com"

Linux / macOS:

bash
export EMAIL_USER="seuemail@gmail.com"
export EMAIL_APP_PASSWORD="sua_senha_de_aplicativo"
export EMAIL_IMAP_HOST="imap.gmail.com"

⚠️ Nunca compartilhe suas credenciais nem as publique no repositório.

5. Como executar

Com organize.py e rules.json na mesma pasta, abra o terminal nesse diretório.

Modo de simulação (não move nenhuma mensagem):

bash
py organize.py --limite 15

Movimentação efetiva:

bash
py organize.py --limite 15 --aplicar

⚠️ A opção --aplicar move as mensagens na conta de e-mail.

Em Linux/macOS, use python3 no lugar de py.

Opções disponíveis
Opção	Descrição
--limite N	Define a quantidade máxima de mensagens processadas.
--nao-lidos	Processa somente mensagens não lidas.
--regras ARQUIVO	Usa outro arquivo JSON de regras.
--aplicar	Move as mensagens (sem ela, roda apenas a simulação).
6. Resultados

Durante a execução, o programa mostra no terminal um resumo das classificações.

Quando executado com --aplicar e havendo mensagens movidas, o arquivo relatorio.csv é criado ou atualizado com: data, remetente, assunto, destino e ação.

7. Boas práticas e privacidade
Comece sempre pelo modo de simulação para conferir se as regras fazem sentido.
Faça os testes em uma conta de e-mail criada só para essa finalidade.
O relatorio.csv contém remetentes e assuntos de e-mails reais: adicione-o ao .gitignore e não o publique no repositório.