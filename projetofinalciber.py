import base64
from Crypto.Util.number import getPrime, inverse, GCD

# Funções para o algoritmo DES (simples e ilustrativo)
def des_criptografar(mensagem, chave):
    chave = chave.encode('utf-8')  # Converte a chave para bytes
    while len(chave) < 8:  # Garante que a chave tenha 8 bytes
        chave += chave
    chave = chave[:8]
    mensagem_bytes = mensagem.encode('utf-8')
    mensagem_bytes = mensagem_bytes.ljust(8, b'\0')  # Preenche com zeros até 8 bytes
    mensagem_cifrada = b''
    for i in range(len(mensagem_bytes)):
        mensagem_cifrada += bytes([mensagem_bytes[i] ^ chave[i % len(chave)]])
    return base64.b64encode(mensagem_cifrada).decode('utf-8')

def des_descriptografar(mensagem_cifrada, chave):
    chave = chave.encode('utf-8')  # Converte a chave para bytes
    while len(chave) < 8:  # Garante que a chave tenha 8 bytes
        chave += chave
    chave = chave[:8]
    mensagem_cifrada = base64.b64decode(mensagem_cifrada)
    mensagem_original = b''
    for i in range(len(mensagem_cifrada)):
        mensagem_original += bytes([mensagem_cifrada[i] ^ chave[i % len(chave)]])
    return mensagem_original.decode('utf-8').rstrip('\0')

# Funções para o algoritmo RSA
def gerar_chaves_rsa(tamanho_primo=512):
    p = getPrime(tamanho_primo)
    q = getPrime(tamanho_primo)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Valor comum para e
    while GCD(e, phi) != 1:
        e += 2
    d = inverse(e, phi)
    return (e, n), (d, n), (p, q)  # Retorna chave pública, chave privada e primos

def rsa_criptografar(mensagem, chave_publica):
    e, n = chave_publica
    mensagem_bytes = [ord(c) for c in mensagem]
    mensagem_cifrada = [pow(m, e, n) for m in mensagem_bytes]
    return mensagem_cifrada

def rsa_descriptografar(mensagem_cifrada, chave_privada):
    d, n = chave_privada
    mensagem_original = ''.join([chr(pow(c, d, n)) for c in mensagem_cifrada])
    return mensagem_original

# Interface do usuário
def menu():
    print("=== Sistema de Criptografia ===")
    print("1. Criptografia Simétrica (DES)")
    print("2. Criptografia Assimétrica (RSA)")
    print("3. Sair")
    return input("Escolha uma opção: ")

def executar_des():
    opcao = input("Deseja (1) Criptografar ou (2) Descriptografar? ")
    texto = input("Digite o texto: ")
    chave = input("Digite a chave (máximo 8 caracteres): ")
    if opcao == "1":
        resultado = des_criptografar(texto, chave)
        print(f"Texto Criptografado: {resultado}")
    elif opcao == "2":
        resultado = des_descriptografar(texto, chave)
        print(f"Texto Descriptografado: {resultado}")

def executar_rsa():
    print("1. Gerar Chaves RSA")
    print("2. Criptografar Mensagem")
    print("3. Descriptografar Mensagem")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        chave_publica, chave_privada, primos = gerar_chaves_rsa()
        print(f"Chave Pública (e, n): {chave_publica}")
        print(f"Chave Privada (d, n): {chave_privada}")
        print(f"Primos: {primos}")
    elif opcao == "2":
        e = int(input("Digite o valor de e: "))
        n = int(input("Digite o valor de n: "))
        mensagem = input("Digite a mensagem: ")
        resultado = rsa_criptografar(mensagem, (e, n))
        print(f"Mensagem Criptografada: {resultado}")
    elif opcao == "3":
        d = int(input("Digite o valor de d: "))
        n = int(input("Digite o valor de n: "))
        mensagem_cifrada = input("Digite a mensagem cifrada (separada por espaços): ")
        mensagem_cifrada = [int(x) for x in mensagem_cifrada.split()]
        resultado = rsa_descriptografar(mensagem_cifrada, (d, n))
        print(f"Mensagem Descriptografada: {resultado}")

# Execução
while True:
    escolha = menu()
    if escolha == "1":
        executar_des()
    elif escolha == "2":
        executar_rsa()
    elif escolha == "3":
        print("Encerrando...")
        break
    else:
        print("Opção inválida, tente novamente.")
