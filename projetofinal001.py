# Importamos as bibliotecas necessárias
import base64  # Para codificar e decodificar as mensagens em Base64 (no DES)
from Crypto.Util.number import getPrime, inverse, GCD  # Para gerar chaves e realizar cálculos no RSA

# ========================
# Funções para Criptografia DES
# ========================

# Função para criptografar usando DES
def des_criptografar(mensagem, chave):
    # Convertemos a chave para bytes (formato necessário para operar com os dados)
    chave = chave.encode('utf-8')
    
    # Garantimos que a chave tenha exatamente 8 bytes (requisito do DES)
    while len(chave) < 8:
        chave += chave  # Repetimos a chave até atingir 8 bytes
    chave = chave[:8]  # Cortamos qualquer excesso para ficar com exatamente 8 bytes

    # Convertemos a mensagem para bytes
    mensagem_bytes = mensagem.encode('utf-8')
    # Preenchemos a mensagem com '\0' (zeros) para garantir que tenha múltiplos de 8 bytes
    mensagem_bytes = mensagem_bytes.ljust(8, b'\0')

    # Inicializamos o texto cifrado como um byte vazio
    mensagem_cifrada = b''
    for i in range(len(mensagem_bytes)):
        # Aplicamos a operação XOR entre os bytes da mensagem e da chave
        mensagem_cifrada += bytes([mensagem_bytes[i] ^ chave[i % len(chave)]])

    # Codificamos a mensagem cifrada em Base64 para facilitar o transporte
    return base64.b64encode(mensagem_cifrada).decode('utf-8')

# Função para descriptografar usando DES
def des_descriptografar(mensagem_cifrada, chave):
    # Convertemos a chave para bytes, assim como na criptografia
    chave = chave.encode('utf-8')
    while len(chave) < 8:
        chave += chave
    chave = chave[:8]

    # Decodificamos a mensagem cifrada de Base64 para bytes
    mensagem_cifrada = base64.b64decode(mensagem_cifrada)

    # Inicializamos a mensagem original como um byte vazio
    mensagem_original = b''
    for i in range(len(mensagem_cifrada)):
        # Aplicamos novamente a operação XOR para recuperar a mensagem original
        mensagem_original += bytes([mensagem_cifrada[i] ^ chave[i % len(chave)]])

    # Removemos os '\0' adicionados durante o preenchimento e retornamos a mensagem original
    return mensagem_original.decode('utf-8').rstrip('\0')

# ========================
# Funções para Criptografia RSA
# ========================

# Função para gerar chaves RSA
def gerar_chaves_rsa(tamanho_primo=512):
    # Geramos dois números primos grandes
    p = getPrime(tamanho_primo)
    q = getPrime(tamanho_primo)

    # Calculamos n (produto dos dois primos) e φ (função totiente)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Escolhemos o expoente público e (normalmente 65537, um valor comum e eficiente)
    e = 65537
    # Garantimos que e seja coprimo com φ
    while GCD(e, phi) != 1:
        e += 2

    # Calculamos o expoente privado d (inverso modular de e em relação a φ)
    d = inverse(e, phi)

    # Retornamos as chaves pública, privada e os números primos
    return (e, n), (d, n), (p, q)

# Função para criptografar uma mensagem usando RSA
def rsa_criptografar(mensagem, chave_publica):
    e, n = chave_publica  # Obtemos e (expoente público) e n
    # Convertemos cada caractere da mensagem em seu valor numérico (ASCII)
    mensagem_bytes = [ord(c) for c in mensagem]
    # Aplicamos a fórmula de criptografia: m^e mod n
    mensagem_cifrada = [pow(m, e, n) for m in mensagem_bytes]
    return mensagem_cifrada

# Função para descriptografar uma mensagem usando RSA
def rsa_descriptografar(mensagem_cifrada, chave_privada):
    d, n = chave_privada  # Obtemos d (expoente privado) e n
    # Aplicamos a fórmula de descriptografia: c^d mod n e convertemos para caracteres
    mensagem_original = ''.join([chr(pow(c, d, n)) for c in mensagem_cifrada])
    return mensagem_original

# ========================
# Interface do Usuário
# ========================

# Função para exibir o menu principal
def menu():
    print("\n===== Sistema de Criptografia =====")
    print("1. Criptografia Simétrica (DES)")
    print("2. Criptografia Assimétrica (RSA)")
    print("3. Sair\n")
    return input("Escolha uma opção: ")

# Função para executar operações com DES
def executar_des():
    opcao = input("Deseja (1) Criptografar ou (2) Descriptografar? ")
    texto = input("Digite o texto: ")
    chave = input("Digite a chave (máximo 8 caracteres): ")
    if opcao == "1":
        # Chama a função de criptografia DES
        resultado = des_criptografar(texto, chave)
        print(f"Texto Criptografado: {resultado}")
    elif opcao == "2":
        # Chama a função de descriptografia DES
        resultado = des_descriptografar(texto, chave)
        print(f"Texto Descriptografado: {resultado}")

# Função para executar operações com RSA
def executar_rsa():
    print("1. Gerar Chaves RSA")
    print("2. Criptografar Mensagem")
    print("3. Descriptografar Mensagem")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        # Gera as chaves RSA
        chave_publica, chave_privada, primos = gerar_chaves_rsa()
        print(f"Chave Pública (e, n): {chave_publica}")
        print(f"Chave Privada (d, n): {chave_privada}")
        print(f"Primos: {primos}")
    elif opcao == "2":
        # Criptografa uma mensagem com RSA
        e = int(input("Digite o valor de e: "))
        n = int(input("Digite o valor de n: "))
        mensagem = input("Digite a mensagem: ")
        resultado = rsa_criptografar(mensagem, (e, n))
        print(f"Mensagem Criptografada: {resultado}")
    elif opcao == "3":
        # Descriptografa uma mensagem com RSA
        d = int(input("Digite o valor de d: "))
        n = int(input("Digite o valor de n: "))
        mensagem_cifrada = input("Digite a mensagem cifrada (separada por espaços): ")
        mensagem_cifrada = [int(x) for x in mensagem_cifrada.split()]
        resultado = rsa_descriptografar(mensagem_cifrada, (d, n))
        print(f"Mensagem Descriptografada: {resultado}")

# ========================
# Execução do Programa
# ========================

# Loop principal do programa
while True:
    escolha = menu()  # Exibe o menu e coleta a escolha do usuário
    if escolha == "1":
        executar_des()  # Executa funções relacionadas ao DES
    elif escolha == "2":
        executar_rsa()  # Executa funções relacionadas ao RSA
    elif escolha == "3":
        print("Encerrando...")
        break  # Sai do loop e encerra o programa
    else:
        print("Opção inválida, tente novamente.")
