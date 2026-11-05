import argparse
import csv
import imaplib
import json
import os
import sys
import unicodedata

from collections import Counter
from datetime import datetime
from email import message_from_bytes
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
    e