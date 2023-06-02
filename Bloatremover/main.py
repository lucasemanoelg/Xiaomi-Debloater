from AppRemover import BloatHandler

handler = BloatHandler()
if __name__ == '__main__':
    print("Instalar/Desinstalar aplicativos Google e Xiaomi")
    print("1 - Instalar aplicativos")
    print("2 - Desinstalar aplicativos")
    n = int(input("O que deseja fazer? Pressione a opção desejada: "))

    if n == 1:
        handler.run(action = 'install')
    elif n == 2:
        handler.run(action = 'remove')
    else:
        print("Opção não existe... Saindo...")
        exit()
