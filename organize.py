import argparse
import csv
import imaplib
import json
import os
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from email import message_from_bytes, policy
from email.header import decode_header, make_header
from pathlib import Path

HOST_PADRAO = "imap.gmail.com"
ARQUIVO_REGRAS = Path(__file__).with_name("rules.json")
ARQUIVO_RELATORIO = Path(__file__).with_name("relatorio.csv")


def normalizar(texto):
 
    sem_acento = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).lower()


def carregar_regras(caminho=ARQUIVO_REGRAS):
    with open(caminho, encoding="utf-8") as f:
        regras = json.load(f)
    for regra in regras:
        regra["palavras"] = [normalizar(p) for p in regra["palavras"]]
    return regras


def classificar(assunto, remetente, regras):
    
    alvo = normalizar(f"{assunto} {remetente}")
    for regra in regras:
        if any(p in alvo for p in regra["palavras"]):
            return regra["pasta"]
    return None


def texto_do_cabecalho(valor):
   
    if not valor:
        return ""
    valor = " ".join(str(valor).split())  
    try:
        return str(make_header(decode_header(valor)))
    except Exception:
        return valor


def ler_cabecalhos(mail, uid):

    status, dados = mail.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
    if status != "OK" or not dados or not isinstance(dados[0], tuple):
        return None
    
    msg = message_from_bytes(dados[0][1], policy=policy.default)
    return texto_do_cabecalho(msg["Subject"]), texto_do_cabecalho(msg["From"])


def processar(mail, regras, limite=50, aplicar=False, nao_lidos=False):
    
    mail.select("INBOX", readonly=not aplicar)

    status, dados = mail.uid("search", None, "UNSEEN" if nao_lidos else "ALL")
    if status != "OK":
        raise RuntimeError("Não consegui listar os e-mails.")
    uids = dados[0].split()[-limite:]

    resultados = []
    pastas_prontas = set()
    movidos = 0

    for uid in reversed(uids):  
        cab = ler_cabecalhos(mail, uid)
        if cab is None:
            continue
        assunto, remetente = cab
        destino = classificar(assunto, remetente, regras)

        if destino is None:
            acao = "mantido"
        elif not aplicar:
            acao = "simulado"
        else:
            if destino not in pastas_prontas:
                mail.create(f'"{destino}"')  
                pastas_prontas.add(destino)
            status, _ = mail.uid("copy", uid, f'"{destino}"')
            if status == "OK":
                mail.uid("store", uid, "+FLAGS", r"(\Deleted)")
                movidos += 1
                acao = "movido"
            else:
                acao = "erro"

        resultados.append(
            {"remetente": remetente, "assunto": assunto, "destino": destino, "acao": acao}
        )

    if aplicar and movidos:
        mail.expunge() 

    return resultados


def salvar_relatorio(resultados, caminho=ARQUIVO_RELATORIO):
    novo = not Path(caminho).exists()
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["data_hora", "remetente", "assunto", "destino", "acao"])
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for r in resultados:
            w.writerow([agora, r["remetente"], r["assunto"], r["destino"] or "", r["acao"]])


def imprimir_resumo(resultados, aplicar):
    for r in resultados:
        destino = r["destino"] or "-"
        print(f"[{r['acao']:8}] {destino:14} | {r['remetente'][:32]:32} | {r['assunto'][:50]}")

    contagem = Counter(r["destino"] or "(sem regra)" for r in resultados)
    print("\nResumo:")
    for pasta, qtd in contagem.most_common():
        print(f"  {pasta:14} {qtd}")
    if not aplicar:
        print("\nSimulação: nada foi movido. Rode com --aplicar para mover de verdade.")


def main():
    ap = argparse.ArgumentParser(description="Organiza a caixa de entrada por regras.")
    ap.add_argument("--aplicar", action="store_true", help="move de verdade (sem isso, só simula)")
    ap.add_argument("--limite", type=int, default=50, help="quantos e-mails recentes ler (padrão: 50)")
    ap.add_argument("--nao-lidos", action="store_true", help="considera só e-mails não lidos")
    ap.add_argument("--regras", default=str(ARQUIVO_REGRAS), help="caminho do rules.json")
    args = ap.parse_args()

    usuario = os.environ.get("EMAIL_USER")
    senha = os.environ.get("EMAIL_APP_PASSWORD")
    host = os.environ.get("EMAIL_IMAP_HOST", HOST_PADRAO)
    if not usuario or not senha:
        sys.exit("Defina EMAIL_USER e EMAIL_APP_PASSWORD (veja o README).")

    regras = carregar_regras(args.regras)

    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(usuario, senha)
    except (imaplib.IMAP4.error, OSError) as erro:
        sys.exit(f"Não consegui entrar no e-mail: {erro}")

    try:
        resultados = processar(mail, regras, args.limite, args.aplicar, args.nao_lidos)
    finally:
        try:
            mail.logout()
        except Exception:
            pass

    imprimir_resumo(resultados, args.aplicar)
    if args.aplicar and resultados:
        salvar_relatorio(resultados)
        print(f"Relatório salvo em {ARQUIVO_RELATORIO.name}")


if __name__ == "__main__":
    main()