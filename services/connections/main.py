import os
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase, exceptions
from dotenv import load_dotenv
from pydantic import BaseModel
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração da Aplicação FastAPI ---
app = FastAPI()

# Adicione este bloco para configurar o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], # Permite a origem do nosso frontend
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# --- Configuração do Driver do Neo4j ---
URI = os.getenv("NEO4J_URI")
# Lê a variável NEO4J_AUTH do .env e a divide em usuário e senha
raw_auth = os.getenv("NEO4J_AUTH", "neo4j/password").split("/")
AUTH = (raw_auth[0], raw_auth[1])

driver = GraphDatabase.driver(URI, auth=AUTH)

# --- Configuração do Kafka Producer ---
producer = None
while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka-broker:29092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except NoBrokersAvailable:
        print("Broker do Kafka não disponível. Tentando novamente em 5 segundos...")
        time.sleep(5)

print("Producer conectado ao Kafka com sucesso!")

# --- Modelos de Dados (Pydantic) ---
class FollowRequest(BaseModel):
    follower_id: int
    followed_id: int

# --- Funções de Lógica ---
def criar_relacao_seguir(tx, follower_id, followed_id):
    query = (
        # Garante que o nó do seguidor exista (cria se não existir)
        "MERGE (follower:Usuario {id: $follower_id}) "
        # Garante que o nó de quem é seguido exista
        "MERGE (followed:Usuario {id: $followed_id}) "
        # Cria o relacionamento :SEGUE entre eles (se já não existir)
        "MERGE (follower)-[:SEGUE]->(followed)"
    )
    tx.run(query, follower_id=follower_id, followed_id=followed_id)

# --- Endpoints da API ---
@app.post("/follow/")
def seguir_usuario(request: FollowRequest):
    if request.follower_id == request.followed_id:
        raise HTTPException(status_code=400, detail="Um usuário não pode seguir a si mesmo.")

    try:
        # Escreve no Neo4j
        with driver.session() as session:
            session.write_transaction(criar_relacao_seguir, request.follower_id, request.followed_id)

        # **NOVO: Publica evento no Kafka**
        topic = 'novos_seguidores' # Nome do tópico, como no documento do projeto [cite: 454]
        message = {
            "seguidorld": request.follower_id,
            "seguidold": request.followed_id,
            "timestamp": "2025-08-17T21:35:00Z" # Timestamp de exemplo [cite: 455]
        }
        producer.send(topic, message)
        producer.flush() # Garante que a mensagem seja enviada

        return {"status": "sucesso", "detalhe": f"Usuário {request.follower_id} agora segue {request.followed_id}"}
    except exceptions.ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Não foi possível conectar ao banco de dados de grafos.")

@app.get("/{user_id}/following/")
def get_seguindo(user_id: int):
    query = """
    MATCH (u:Usuario {id: $user_id})-[:SEGUE]->(seguindo:Usuario)
    RETURN seguindo.id AS id
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        return {"following": [record["id"] for record in result]}

@app.get("/{user_id}/followers/")
def get_seguidores(user_id: int):
    query = """
    MATCH (seguidor:Usuario)-[:SEGUE]->(u:Usuario {id: $user_id})
    RETURN seguidor.id AS id
    """
    with driver.session() as session:
        result = session.run(query, user_id=user_id)
        return {"followers": [record["id"] for record in result]}

@app.on_event("shutdown")
def fechar_conexao_driver():
    driver.close()