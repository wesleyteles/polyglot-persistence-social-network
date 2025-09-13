<h1> Polyglot Persistence Social Network </h1>

Bem-vindo ao repositório do projeto Rede Social Simplificada, um sistema desenvolvido para explorar e demonstrar o poder da persistência poliglota e de arquiteturas orientadas a eventos em um ambiente de microsserviços.

Este projeto não é apenas sobre criar mais uma rede social, mas sim sobre construir uma fundação robusta, escalável e resiliente, pronta para os desafios da era do Big Data e da interação em tempo real.

É uma jornada pela arte de escolher a ferramenta certa para cada trabalho.

<h1> Sobre o Projeto </h1> 
Este projeto nasceu como um trabalho prático para o Curso de Especialização em Gerência de Projetos de Software na Era de Dados de Sensores e IA da Universidade Federal de Juiz de Fora (UFJF). 

O objetivo era projetar e prototipar a arquitetura de dados para uma rede social, aplicando três modelos de armazenamento distintos para resolver diferentes desafios do sistema.

<h1>A Arquitetura: O Poder da Escolha Certa </h1>

A abordagem central é a persistência poliglota, onde cada tipo de dado é armazenado na tecnologia mais adequada para ele, resultando em um sistema mais performático e escalável.

🛡️ Dados Relacionais (Django + PostgreSQL): O núcleo do sistema, responsável pela identidade e segurança dos usuários. Garante a consistência e a integridade dos dados mestres, como perfis e credenciais, que são a base de tudo

🕸️ Dados em Grafo (FastAPI + Neo4j): O coração da rede, mapeando o "grafo social". Modela com extrema eficiência as conexões (quem segue quem) e interações complexas, permitindo consultas de relacionamento (ex: sugestão de amigos) que seriam proibitivas em um modelo relacional.

⚡ Stream de Eventos (Python + Kafka): O sistema nervoso central, permitindo comunicação assíncrona e em tempo real entre os serviços. Cada ação, como um "seguir", torna-se um evento que flui pela plataforma, habilitando funcionalidades como notificações instantâneas e análises em tempo real de forma desacoplada e resiliente.

<h1> Tecnologias Utilizadas </h1>>
Categoria	Tecnologia:

Backend	Django: (API de Usuários), FastAPI (API de Conexões), Python (Consumidor Kafka)

Frontend:	HTML5, Tailwind CSS, Flowbite JS

Bancos de Dados:	PostgreSQL (Relacional), Neo4j (Grafo), Apache Kafka (Stream/Log de Eventos)

Infraestrutura:	Docker, Docker Compose, Nginx

<h1>Começando: Instruções de Uso </h1>
Para rodar este projeto em sua máquina local, você precisará ter o Git, Docker e Docker Compose instalados.

1. Clonando o Repositório
Bash
git clone https://github.com/wesleyteles/polyglot-persistence-social-network.git
cd polyglot-persistence-social-network

2. Configurando as Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto. Você pode copiar o arquivo de exemplo env.example (se existir) ou usar o template abaixo. Lembre-se de usar senhas seguras!

Snippet de código
# Configurações do PostgreSQL
POSTGRES_DB=social_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=senha_super_segura_aqui

# Configurações do Neo4j (formato: usuario/senha)
NEO4J_AUTH=neo4j/outra_senha_segura_aqui
NEO4J_URI=neo4j://neo4j-db:7687

# Chave secreta do Django
DJANGO_SECRET_KEY=sua-chave-secreta-pode-ser-qualquer-coisa-longa
3. Subindo os Contêineres
Com o Docker em execução, execute o seguinte comando na raiz do projeto. Ele irá construir as imagens, baixar as dependências e iniciar todos os serviços.

Bash
docker-compose up --build
A primeira inicialização pode levar alguns minutos.

4. Interagindo com a Aplicação
Com os serviços no ar, você pode acessar as diferentes partes do sistema:

🌐 Frontend da Rede Social:
URL: http://localhost:8080
Aqui você pode se registrar (crie alguns usuários para testar!), fazer login e seguir outros usuários.

🔐 Django Admin (Gestão de Dados):
URL: http://localhost:8000/admin/
Para acessar, primeiro crie um superusuário. Abra um novo terminal e rode:
Bash
docker-compose run --rm django-app python manage.py createsuperuser

Siga as instruções para criar seu usuário administrador e depois faça o login na URL acima.

📊 Neo4j Browser (Visualização do Grafo):
URL: http://localhost:7474
Use o usuário neo4j e a senha que você definiu em NEO4J_AUTH para fazer o login.
Para ver os nós e relacionamentos criados, execute a query Cypher: MATCH (n) RETURN n

Testando o Fluxo Completo
Acesse http://localhost:8080 e crie dois ou mais usuários através da API de registro (via curl ou Postman, se a UI de registro não estiver implementada).

Faça login com um dos usuários na interface.

A lista de outros usuários aparecerá. Clique no botão "Seguir".

Observe o terminal onde o docker-compose up está rodando. Você verá uma mensagem do notifications-app confirmando que o evento de "seguir" foi recebido e processado em tempo real!

<h1> Detalhes Acadêmicos </h1>
Este projeto é um resultado prático do conhecimento adquirido na Pós-Graduação da UFJF.

Universidade: Universidade Federal de Juiz de Fora (UFJF)

Curso: Especialização em Gerência de Projetos de Software na Era de Dados de Sensores e IA 

Disciplina: Gerência de Dados

Autor: Wesley de Sá Teles 

Professor: Prof. Victor Ströele 

Sinta-se à vontade para explorar, modificar e aprender com este projeto!
