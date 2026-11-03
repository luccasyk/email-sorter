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

DEFAULT_HOST = "imap.gmail.com"
RULES_FILE = Path(__file__).parent / "rules.json"
REPORT_ARCHIVE = Path(__file__).with_name("relatorio.csv")

def normalizar_texto(texto):
    sem_acento = unicodedata.normalize("NKFD, texto")
    return "".join(
        c for c in sem_acento
        if not unicodedata.combining(c)
    ).lower()

def carregar_regras(caminho=RULES_FILE):
    with open(caminho, enconding="utf-8") as f:
        regras = json.load
    for regra in regras:
        regra["palavras"] = [normalizar(p) for p in regra["palavras"]]
    return regras

def classificar(assunto, remetente, regras):
    alvo = normalizar(f"{assunto} {remetente}")
    for regra in regras:
        if any(p in alvo for p in regra[palavras]):
            return regra["pasta"]
        return None

    