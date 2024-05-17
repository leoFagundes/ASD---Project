import socket

def send_handshake(UDPClientSocket, serverAddressPort, bufferSize):
    handshake_message = "handshake"
    UDPClientSocket.sendto(str.encode(handshake_message), serverAddressPort)
    msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
    return msgFromServer.decode() == "Handshake ACK"

def send_message(UDPClientSocket, serverAddressPort, message, bufferSize):
    UDPClientSocket.sendto(str.encode(message), serverAddressPort)
    msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
    return msgFromServer.decode()

def run_client(serverAddressPort, bufferSize):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    if send_handshake(UDPClientSocket, serverAddressPort, bufferSize):
        print("Conexão estabelecida com o servidor.\n")

        while True:
            user_input = input("Digite uma mensagem ('sair' para encerrar): ")
            if user_input.lower() == "sair":
                break
            response = send_message(UDPClientSocket, serverAddressPort, user_input, bufferSize)
            print(f"Mensagem do Servidor: {response}\n")
    else:
        print("Falha ao estabelecer conexão com o servidor.")

    UDPClientSocket.close()

if __name__ == "__main__":
    SERVER_ADDRESS_PORT = ("127.0.0.1", 20001)
    BUFFER_SIZE = 1024

    run_client(SERVER_ADDRESS_PORT, BUFFER_SIZE)
