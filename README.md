# Projeto de Comunicação Cliente-Servidor UDP

## Descrição

Este projeto consiste em uma implementação de comunicação Cliente-Servidor utilizando o protocolo UDP. O cliente envia mensagens para o servidor, que responde com base na mensagem recebida. A comunicação envolve um handshake inicial para estabelecer a conexão e uma mensagem de desconexão para finalizar a comunicação.

## Estrutura do Projeto

O projeto é composto por dois scripts principais:

- `cliente.py`: Contém a lógica do cliente que se conecta ao servidor, envia mensagens e recebe respostas.
- `servidor.py`: Contém a lógica do servidor que aceita conexões de clientes, processa mensagens e responde adequadamente.

## Funcionamento

### Cliente

1. Estabelece uma conexão com o servidor através de um handshake.
2. Envia mensagens para o servidor e aguarda respostas.
3. Envia uma mensagem de desconexão para o servidor ao finalizar.

### Servidor

1. Aguarda conexões de clientes.
2. Realiza um handshake com novos clientes e os adiciona à lista de clientes conectados.
3. Processa mensagens recebidas dos clientes e envia respostas apropriadas.
4. Remove clientes da lista de conectados ao receber uma mensagem de desconexão.

## Como Executar

### Requisitos

- Python 3.x

### Passos

1. **Iniciar o Servidor**

   Execute o script do servidor para iniciar o servidor UDP:

   ```sh
   python servidor.py
   ```

2. **Iniciar o Cliente**

   Em outra janela de terminal (ou outro computador conectado via ip), execute o script do cliente:

   ```sh
   python cliente.py
   ```

[Documento do trabalho](https://github.com/leoFagundes/UDP--Project/blob/main/assets/github/ASD%20-%20Volunt%C3%A1ria.docx)
