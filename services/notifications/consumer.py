import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

print("Iniciando o consumidor de notificações...")

# Tenta conectar ao Kafka com retentativas
consumer = None
while consumer is None:
    try:
        consumer = KafkaConsumer(
            'novos_seguidores', # O tópico que queremos "escutar" [cite: 459]
            bootstrap_servers='kafka-broker:29092',
            auto_offset_reset='earliest', # Começa a ler do início do tópico se for um novo consumidor
            group_id='notification-consumers', # Identificador do grupo de consumidores
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    except NoBrokersAvailable:
        print("Broker do Kafka não disponível. Tentando novamente em 5 segundos...")
        time.sleep(5)

print("Consumidor conectado ao Kafka. Aguardando mensagens...")

# Loop infinito para processar mensagens
for message in consumer:
    # message.value é o payload JSON que enviamos do produtor
    notification_data = message.value

    # Simula o processamento da notificação [cite: 461]
    print(f"--- NOVA NOTIFICAÇÃO ---")
    print(f"Tópico: {message.topic}")
    print(f"Usuário a ser notificado: {notification_data['seguidold']}")
    print(f"Mensagem: O usuário {notification_data['seguidorld']} começou a te seguir!")
    print(f"Dados completos: {notification_data}")
    print("------------------------\n")