import numpy as np

# Tabela S-box para substituição de bytes
S_BOX = [
    [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
    [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
    [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
    [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
    [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
    [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
    [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
    [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
    [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
    [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
    [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
    [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
    [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
    [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
    [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
    [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22],
]

# Função para substituir bytes usando a S-box
def sub_bytes(state):
    return [[S_BOX[b // 16][b % 16] for b in row] for row in state]

# Rotação de linhas (ShiftRows)
def shift_rows(state):
    return [
        state[0],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3],
    ]

# Operação XOR com a chave de rodada
def add_round_key(state, round_key):
    return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]

# Exemplo de uso
def aes_encrypt_block(block, key):
    # Converte o bloco e a chave para matrizes 4x4
    state = [list(block[i:i+4]) for i in range(0, 16, 4)]
    round_key = [list(key[i:i+4]) for i in range(0, 16, 4)]
    
    # Adição inicial da chave
    state = add_round_key(state, round_key)
    
    # Apenas uma rodada para simplificar (AES real tem várias rodadas)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_key)
    
    # Converte de volta para uma lista linear
    return [byte for row in state for byte in row]

# Bloco de exemplo (16 bytes) e chave (16 bytes)
block = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0xcf, 0x8f, 0x4e, 0xa7, 0x11, 0x1c]

# Encriptação
encrypted_block = aes_encrypt_block(block, key)
print("Encrypted block:", encrypted_block)
