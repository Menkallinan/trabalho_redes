import socket

def verificar_vencedor(jogada_jogador1, jogada_jogador2):
    jogadas_ganhadoras = {
        "pedra": ["tesoura", "lagarto"],
        "tesoura": ["papel", "lagarto"],
        "papel": ["pedra", "Spock"],
        "lagarto": ["papel", "Spock"],
        "Spock": ["tesoura", "pedra"]
    }

    if jogada_jogador1 == jogada_jogador2:
        return "Empate"
    elif jogada_jogador2 in jogadas_ganhadoras[jogada_jogador1]:
        return "Jogador 1 venceu"
    else:
        return "Jogador 2 venceu"

def main():
    escutador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    porta = 50000
    ip = '127.0.0.1'
    escutador.bind((ip, porta))
    escutador.listen(1)

    print("Aguardando jogador...")
    socket_jogador, dados_jogador = escutador.accept()
    print("Jogador conectado")

    rodada = 0
    vitorias_servidor = 0
    vitorias_cliente = 0

    while True:
        rodada += 1
        print(f"\nRodada {rodada}")

        # Envie a informação da rodada para o cliente
        socket_jogador.send(f"Rodada {rodada}".encode())

        # Recebe a jogada do Cliente
        jogada_cliente = socket_jogador.recv(1024).decode()

        # Recebe a jogada do Servidor (Jogador 1)
        jogada_servidor = input("Sua jogada (pedra, papel, tesoura, lagarto, Spock): ")
        socket_jogador.send(jogada_servidor.encode())

        # Verifica o vencedor
        resultado = verificar_vencedor(jogada_servidor, jogada_cliente)

        print(f"O adversario jogou ({jogada_cliente})")
        if resultado == "Jogador 1 venceu":
            vitorias_servidor += 1
            print(f"Você venceu essa rodada! O placar está ({vitorias_servidor} - {vitorias_cliente})")
        elif resultado == "Jogador 2 venceu":
            vitorias_cliente += 1
            print(f"Você perdeu essa rodada! O placar está ({vitorias_servidor} - {vitorias_cliente})")
        else:
            print("Essa rodada foi um empate. Vamos jogar novamente.")
            rodada -= 1

        # Envia o resultado para o Cliente
        socket_jogador.send(resultado.encode())

        # Verifica se alguém atingiu 3 vitórias
        if vitorias_servidor == 3 or vitorias_cliente == 3:
            break

    print("\nFim do jogo")

    # Informa o resultado final ao Cliente
    if vitorias_cliente < vitorias_servidor:
        print("BAZINGA")
    else:
        print("Não foi dessa vez")

    socket_jogador.close()
    escutador.close()

if __name__ == '__main__':
    main()

