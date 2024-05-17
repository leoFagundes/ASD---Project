# UDP Client-Server Application

Este repositório contém uma aplicação cliente-servidor que se comunica utilizando o protocolo UDP. O servidor pode lidar com múltiplos clientes e responde a mensagens específicas dos clientes.

## Estrutura do Projeto

- `server.py`: Contém o código do servidor UDP.
- `client.py`: Contém o código do cliente UDP.

## Funcionalidades

- **Servidor**

  - Aceita conexões de clientes através de um handshake inicial.
  - Mantém uma lista de clientes conectados.
  - Responde a mensagens dos clientes, verificando se a mensagem é "AA" e respondendo adequadamente.
  - Exibe a lista de clientes conectados.

- **Cliente**
  - Envia uma mensagem de handshake ao servidor para estabelecer conexão.
  - Permite ao usuário enviar mensagens ao servidor e receber respostas.
  - Encerra a conexão ao digitar "sair".
