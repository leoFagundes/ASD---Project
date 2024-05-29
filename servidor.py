import socket
import threading
import datetime

from decimal import *
getcontext().prec = 28

limit = 1000000

def log(text: str = '', showTime: bool = True) -> None:
    """
    Exibe um log na tela, opcionalmente mostrando o horário atual.

    Args:
        text (str, optional): Texto a ser exibido no log. Padrão é ''.
        showTime (bool, optional): Indica se o horário atual deve ser exibido junto com o texto. Padrão é True.
    """
    if text:
        print(f'{datetime.datetime.now().strftime("%H:%M:%S"):^10}: {text}') if showTime else print(text)
    else:
        print()

def show_connected_clients(clients: set) -> None:
    """
    Exibe na tela os clientes conectados.

    Args:
        clients (set): Conjunto de tuplas contendo endereço IP e porta dos clientes conectados.
    """
    if clients:
        log(f"|  {'Clientes conectados':^30}   |", showTime=False)
        log(f"| {'Client_IP':^15} | {'Client_PORT':^15} |", showTime=False)
        for client in clients:
            ip, port = client
            log(f"| {ip:^15} | {port:^15} |", showTime=False)
        log()
    else:
        log("Nenhum cliente conectado no momento.")

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
    log(f"[handshake] Cliente {address} conectado.\n")

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
        log(f"[disconnect] Cliente {address} desconectado.\n")
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
    clientIP = f"IP: {client_ip} | Port: {client_port}"
    clientMsg = f"Mensagem do Cliente: {message.decode()}\n"
    log(clientIP)
    log(clientMsg)
    
    if message.decode() == "AA":
        response = "Resposta correta!"
    else:
        response = "Resposta incorreta!"

    UDPServerSocket.sendto(str.encode(response), address)

def handle_client_monte_carlo(UDPServerSocket: socket.socket, message: bytes, address: tuple):

    client_ip, client_port = address
    clientIP = f"IP: {client_ip} | Port: {client_port}"
    clientMsg = f"Tupla do Cliente: {message.decode()}\n"
    log(clientIP)
    log(clientMsg)
    tupla = message.decode().split(",")

    total_points = 0
    points_in_circle = 0

    while total_points < limit:
        points_in_circle += Decimal(tupla[0])
        total_points += Decimal(tupla[1])
        print("Pontos dentro do circulo: ", points_in_circle, " | ", "Total de pontos: ", total_points, " | ", "Valor de pi: ", round(Decimal(4*(points_in_circle / total_points)), 20), "\n")
        response = "Dados adicionados"
    else:
        response = "Limite de pontos alcancado"

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

    handle_client_monte_carlo(UDPServerSocket, message, address)

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
    log("Servidor UDP ativo e ouvindo...\n")

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
