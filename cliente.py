import socket

def main():
    socket_jogador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    porta_servidor = 50000
    ip_servidor = '127.0.0.1'

    socket_jogador.connect((ip_servidor, porta_servidor))
    print("Conectado ao servidor")

    vitorias_cliente = 0
    vitorias_servidor = 0

    while True:
        # Recebe a informação da rodada do servidor
        info_rodada = socket_jogador.recv(1024).decode()
        print("\n")
        print(info_rodada)

        # Faz a própria jogada
        jogada_cliente = input("Sua jogada (pedra, papel, tesoura, lagarto, Spock): ")
        socket_jogador.send(jogada_cliente.encode())

        # Recebe a jogada do Servidor (Jogador 1)
        jogada_servidor = socket_jogador.recv(1024).decode()

        # Recebe o resultado da rodada
        resultado = socket_jogador.recv(1024).decode()
        print(f"O adversario jogou ({jogada_servidor})")

        # Verifica o resultado final
        if "Jogador 2 venceu" in resultado:
            vitorias_cliente += 1
            print(f"Você venceu essa rodada! O placar está ({vitorias_cliente} - {vitorias_servidor})")
        elif "Jogador 1 venceu" in resultado:
            vitorias_servidor += 1
            print(f"Você perdeu essa rodada! O placar está ({vitorias_cliente} - {vitorias_servidor})")
        else:
            print("Essa rodada foi um empate. Vamos jogar novamente.")

        # Verifica o resultado final
        if vitorias_servidor == 3 or vitorias_cliente == 3:
            break

    print("\nFim do jogo")
    
    if vitorias_cliente > vitorias_servidor:
        print("BAZINGA")
    else:
        print("Não foi dessa vez")

    socket_jogador.close()

if __name__ == '__main__':
    main()

