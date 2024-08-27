import os
import subprocess
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import tkinter as tk
from tkinter import font

def run_powershell_command(command, as_admin=False):
    if as_admin:
        command = f'Start-Process powershell -Verb runAs -ArgumentList "{command}"'
    process = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return process.stdout, process.stderr

def install_openssh():
    command = 'Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0'
    stdout, stderr = run_powershell_command(command, as_admin=True)
    if stderr:
        print(f"Erro ao instalar OpenSSH: {stderr}")
    else:
        print(f"OpenSSH instalado com sucesso: {stdout}")

def generate_ssh_keys():
    ssh_folder = Path.home() / '.ssh'
    ssh_folder.mkdir(parents=True, exist_ok=True)

    private_key_path = ssh_folder / 'id_rsa'
    public_key_path = ssh_folder / 'id_rsa.pub'

    # Geração da chave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serializando a chave privada
    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Gerando e serializando a chave pública
    public_key = private_key.public_key()
    with open(public_key_path, "wb") as public_key_file:
        public_key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.OpenSSH,
                format=serialization.PublicFormat.OpenSSH
            )
        )

    print(f"Chaves SSH geradas com sucesso em {private_key_path} e {public_key_path}")

def create_interface():
    root = tk.Tk()
    root.title("Processo")
    root.geometry("300x200")
    
    # Centralizando o texto em negrito
    bold_font = font.Font(weight="bold")
    label = tk.Label(root, text="Instalado e gerando chaves!", font=bold_font)
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    root.mainloop()

if __name__ == "__main__":
    create_interface()
    install_openssh()
    generate_ssh_keys()
