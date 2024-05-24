import socket
import threading

def show_connected_clients(clients: set) -> None:
    """
    Exibe na tela os clientes conectados.

    Args:
        clients (set): Conjunto de tuplas contendo endereço IP e porta dos clientes conectados.
    """
    if clients:
        print(f"|  {'Clientes conectados':^30}   |")
        print(f"| {'Client_IP':^15} | {'Client_PORT':^15} |")
        for client in clients:
            ip, port = client
            print(f"| {ip:^15} | {port:^15} |")
        print()
    else:
        print("Nenhum cliente conectado no momento.")

def handle_handshake(UDPServerSocket: socket.socket, address: tuple, connected_clients: set) -> None:
    """
    Realiza o handshake com um novo cliente e o adiciona à lista de clientes conectados.

    Args:
        UDPServerSocket (socket.socket): Socket do servidor UDP.
        address (tuple): Tupla contendo endereço IP e porta do cliente.
        connected_clients (set): Conjunto de tuplas contendo endereço IP e porta dos clientes conectados.
    """
    handshakeAck = "Handshake ACK"
    UDPServerSocket.sendto(str.encode(handshakeAck), address)
    connected_clients.add(address)
    print(f"\nhandshake: Cliente {address} conectado.\n")

def handle_disconnect(UDPServerSocket: socket.socket, address: tuple, connected_clients: set) -> None:
    """
    Desconecta um cliente e o remove da lista de clientes conectados.

    Args:
        UDPServerSocket (socket.socket): Socket do servidor UDP.
        address (tuple): Tupla contendo endereço IP e porta do cliente.
        connected_clients (set): Conjunto de tuplas contendo endereço IP e porta dos clientes conectados.
    """
    if address in connected_clients:
        connected_clients.remove(address)
        print(f"\ndisconnect: Cliente {address} desconectado.\n")
        show_connected_clients(list(connected_clients))

def handle_client_message(UDPServerSocket: socket.socket, message: bytes, address: tuple) -> None:
    """
    Processa a mensagem recebida de um cliente e envia uma resposta.

    Args:
        UDPServerSocket (socket.socket): Socket do servidor UDP.
        message (bytes): Mensagem recebida do cliente.
        address (tuple): Tupla contendo endereço IP e porta do cliente.
    """
    client_ip, client_port = address
    clientIP = f"\nIP: {client_ip} | Port: {client_port}"
    clientMsg = f"Mensagem do Cliente: {message.decode()}"
    print(clientIP)
    print(clientMsg)
    
    if message.decode() == "AA":
        response = "Resposta correta!"
    else:
        response = "Resposta incorreta!"

    UDPServerSocket.sendto(str.encode(response), address)

def client_thread(UDPServerSocket: socket.socket, message: bytes, address: tuple, connected_clients: set) -> None:
    """
    Thread para lidar com as mensagens de um cliente.

    Args:
        UDPServerSocket (socket.socket): Socket do servidor UDP.
        message (bytes): Mensagem recebida do cliente.
        address (tuple): Tupla contendo endereço IP e porta do cliente.
        connected_clients (set): Conjunto de tuplas contendo endereço IP e porta dos clientes conectados.
    """
    if address not in connected_clients:
        if message.decode() == "handshake":
            handle_handshake(UDPServerSocket, address, connected_clients)
            show_connected_clients(list(connected_clients))
        return

    if message.decode() == "disconnect":
        handle_disconnect(UDPServerSocket, address, connected_clients)
        return

    handle_client_message(UDPServerSocket, message, address)

def run_server(localIP: str, localPort: int, bufferSize: int) -> None:
    """
    Inicia o servidor UDP e aguarda conexões de clientes.

    Args:
        localIP (str): Endereço IP local do servidor.
        localPort (int): Porta local do servidor.
        bufferSize (int): Tamanho do buffer para recebimento de mensagens.
    """
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("Servidor UDP ativo e ouvindo...\n")

    connected_clients = set()

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        thread = threading.Thread(target=client_thread, args=(UDPServerSocket, message, address, connected_clients))
        thread.start()

if __name__ == "__main__":
    LOCAL_IP = "10.6.0.40"
    LOCAL_PORT = 20001
    BUFFER_SIZE = 1024

    run_server(LOCAL_IP, LOCAL_PORT, BUFFER_SIZE)
