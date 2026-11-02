import win32com.client as win32

outlook = win32.Dispatch("Outlook.Application").GetNamespace('MAPI')
account = outlook.Folders['emaildeteste@outlook.com']
inbox = account.Folders['Caixa de Entrada']

