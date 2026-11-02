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


