import pika
import time
import threading

class Cliente:
    def __init__(self, cliente_id):
        self.cliente_id = cliente_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='barbeiro', durable=True)

    def cortar(self, servico):
        relogio_cliente = time.time()
        self.channel.basic_publish(exchange='', routing_key='barbeiro', body=f"{relogio_cliente}_{self.cliente_id}_{servico}", properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))
        print(f"Cliente {self.cliente_id} chegou para cortar o {servico}.")
        while True:
            method_frame, header_frame, body = self.channel.basic_get(queue='barbeiro')
            if method_frame:
                relogio_cliente, cliente_id, servico = body.decode().split('_')
                time.sleep(1)  # Simula o tempo para fazer o processamento local
                print(f"Cliente {cliente_id} cortou o {servico}.")
                self.channel.basic_ack(method_frame.delivery_tag)
                break

def iniciar_clientes():
    clientes = [Cliente(i) for i in range(5)]
    for i, cliente in enumerate(clientes):
        threading.Thread(target=cliente.cortar, args=(['cabelo', 'barba', 'bigode'][i % 3],)).start()

if __name__ == "__main__":
    iniciar_clientes()
