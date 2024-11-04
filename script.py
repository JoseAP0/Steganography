from PIL import Image
import numpy as np
import hashlib
from cryptography.fernet import Fernet

# Função para gerar uma chave e retornar o objeto Fernet
def gerar_chave():
    chave = Fernet.generate_key()
    return chave, Fernet(chave)

# Função para embutir texto em uma imagem
def embutir_texto(imagem, texto):
    img = Image.open(imagem)
    img = img.convert("RGB")
    data = np.array(img)

    binario_texto = ''.join(format(ord(i), '08b') for i in texto) + '1111111111111110'  # marcador de fim
    tamanho_texto = len(binario_texto)

    data_flat = data.flatten()
    for i in range(tamanho_texto):
        if data_flat[i] % 2 == 0:
            data_flat[i] += 1
        data_flat[i] = int(binario_texto[i])

    data = data_flat.reshape(img.size[1], img.size[0], 3)
    nova_imagem = Image.fromarray(data.astype('uint8'))
    nova_imagem.save("imagem_embutida.png")

# Função para recuperar texto da imagem
def recuperar_texto(imagem):
    img = Image.open(imagem)
    data = np.array(img)
    data_flat = data.flatten()

    binario_texto = ''
    for i in range(len(data_flat)):
        binario_texto += str(data_flat[i] % 2)

    texto = ''
    for i in range(0, len(binario_texto), 8):
        byte = binario_texto[i:i + 8]
        if byte == '11111111':  
            break
        texto += chr(int(byte, 2))
    
    return texto

# Função para gerar o hash da imagem
def gerar_hash(imagem):
    with open(imagem, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Função para encriptar texto
def encriptar_texto(texto, chave):
    return chave.encrypt(texto.encode())

# Função para decriptar texto
def decriptar_texto(texto_encriptado, chave):
    return chave.decrypt(texto_encriptado).decode()

# Menu de opções
def menu():
    chave, fernet = gerar_chave()
    while True:
        print("\nMenu de opções:")
        print("(1) Embutir texto em uma imagem")
        print("(2) Recuperar texto de uma imagem")
        print("(3) Gerar hash da imagem")
        print("(4) Encriptar mensagem")
        print("(5) Decriptar mensagem")
        print("(S ou s) Sair")

        opcao = input("Escolha uma opção: ")

        if opcao in ['S', 's']:
            break
        elif opcao == '1':
            texto = input("Digite o texto a ser embutido: ")
            embutir_texto("imagem_original.png", texto)
            print("Texto embutido na imagem.")
        elif opcao == '2':
            texto_recuperado = recuperar_texto("imagem_embutida.png")
            print("Texto recuperado:", texto_recuperado)
        elif opcao == '3':
            hash_original = gerar_hash("imagem_original.png")
            hash_modificada = gerar_hash("imagem_embutida.png")
            print("Hash da imagem original:", hash_original)
            print("Hash da imagem alterada:", hash_modificada)
        elif opcao == '4':
            mensagem = input("Digite a mensagem a ser encriptada: ")
            texto_encriptado = encriptar_texto(mensagem, fernet)
            print("Texto encriptado:", texto_encriptado)
        elif opcao == '5':
            texto_decriptado = decriptar_texto(texto_encriptado, fernet)
            print("Texto decriptado:", texto_decriptado)
        else:
            print("Opção inválida. Tente novamente.")

# Executar o menu
if __name__ == "__main__":
    menu()
