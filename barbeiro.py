import pika
import time
import threading

class Barbeiro:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='barbeiro', durable=True)

    def atender_cliente(self):
        def callback(ch, method, properties, body):
            relogio_cliente, cliente_id, servico = body.decode().split('_')
            print(f"Barbeiro atendendo Cliente {cliente_id} - Serviço: {servico}")
            time.sleep(5 if servico == 'cabelo' else 4 if servico == 'barba' else 3)
            print(f"Barbeiro terminou de atender Cliente {cliente_id} - Serviço: {servico}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='barbeiro', on_message_callback=callback)
        print("Barbeiro 1 esperando por clientes.")
        self.channel.start_consuming()

if __name__ == "__main__":
    barbeiro = Barbeiro()
    barbeiro.atender_cliente()
