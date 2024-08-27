## instalar openSSH
roda o comando "Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0" num terminal powershell com direitos de administrador;

## gera a chave privada e pública
gera na pasta .ssh do usuário uma chave privada de nome "id_rsa" e uma chave pública de nome "id_rsa.pub" usando o padrão openSSH.
Os parâmetros pra criação de chave são: criptografia RSA e número de bits sendo 2048.