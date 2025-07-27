# Dockerfile

# Usa uma imagem slim do Python para manter o tamanho final pequeno
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala as dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o contêiner
# Isso inclui as pastas 'config', 'prompts', 'scripts', e 'tools'
COPY . .

# Cria um espaço de trabalho padrão para o agente usar se nenhum volume for montado
RUN mkdir -p /app/workspace

# Expõe a porta 8000, que é a porta padrão do nosso servidor FastAPI/Uvicorn
EXPOSE 8000

# O comando que será executado quando o contêiner iniciar.
# Inicia o servidor web Uvicorn, apontando para o objeto 'app' dentro do arquivo 'api_main.py'.
CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
