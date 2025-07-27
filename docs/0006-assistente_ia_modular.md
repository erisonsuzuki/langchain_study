# Assistente de Desenvolvimento de IA (AIaaS)

[](https://github.com)
[](https://opensource.org/licenses/MIT)

Este projeto implementa um "Assistente de IA como um Serviço" Dockerizado. Ele expõe várias capacidades de automação de desenvolvimento (análise de código, geração de documentação, planejamento de features, etc.) através de uma API RESTful, utilizando FastAPI.

O sistema foi projetado para ser **agnóstico ao provedor de LLM**, permitindo o uso de modelos locais via **Ollama** ou provedores de nuvem como **OpenAI**, **Google Gemini** e **Anthropic** através de um sistema de configuração flexível e hierárquico.

## Arquitetura e Conceitos Chave

A arquitetura foi desenhada para ser modular, configurável e extensível, baseada nos seguintes pilares:

  * **API-First com FastAPI:** O núcleo do projeto é um servidor web que expõe todas as funcionalidades através de uma API RESTful, permitindo que qualquer serviço, script ou ferramenta interaja com o assistente.
  * **Contêinerização com Docker:** A aplicação inteira é empacotada em uma imagem Docker, garantindo um ambiente de execução consistente e portátil, eliminando problemas de dependência entre máquinas.
  * **LLM Factory Agóstica:** Uma camada de abstração (`config/settings.py`) permite que a aplicação solicite uma instância de LLM sem se preocupar com qual provedor (Ollama, OpenAI, etc.) está sendo usado. A seleção é feita dinamicamente com base em arquivos de configuração.
  * **Configuração Externalizada:**
      * **`.env`**: Gerencia segredos (chaves de API) e a seleção do provedor/modelo padrão.
      * **`prompts/`**: Todos os prompts são mantidos como arquivos `.md` individuais, permitindo fácil edição por qualquer pessoa da equipe, sem tocar no código.
      * **`config/llm_settings.yaml`**: Controla os parâmetros finos dos LLMs (como `temperature`) para cada tipo de tarefa.
  * **Interface de Comando com `Makefile`**: Um `Makefile` na raiz do projeto serve como um "painel de controle", oferecendo comandos simples e memoráveis para tarefas complexas como construir a imagem Docker, iniciar o servidor e interagir com a API.

## Estrutura do Projeto

```
/assistente_ia_final
├── Makefile              # Painel de controle com comandos simples (make start, make plan)
├── Dockerfile            # Receita para construir a imagem Docker do servidor da API
├── .env.example          # Arquivo de exemplo para configuração de ambiente
├── .gitignore            # Especifica arquivos a serem ignorados pelo Git
├── .pre-commit-config.yaml # Configuração para hooks de Git (qualidade de código)
├── README.md             # Esta documentação
├── requirements.txt      # Lista de dependências Python do projeto
├── api_main.py           # O servidor FastAPI, ponto de entrada da API
├── config/                 # Módulo de configuração central
│   ├── llm_settings.yaml # Parâmetros dos LLMs (temperature, etc.)
│   └── settings.py       # Lógica para carregar configs, prompts e criar instâncias de LLMs
├── prompts/                # Diretório contendo todos os prompts
│   ├── analysis.md       # Prompt para a tarefa de análise de código
│   ├── documentation.md  # Prompt para a tarefa de geração de documentação
│   └── planning.md       # Prompt para a tarefa de planejamento de features
└── scripts/
    └── api_client.py     # Cliente de linha de comando para interagir com a API
```

## Instalação e Execução

Siga estes passos para colocar o assistente no ar.

### Pré-requisitos

1.  **Docker** instalado e em execução.
2.  **Ollama** instalado localmente (se for usar modelos locais).
3.  **Git** para clonar o repositório.

### 1\. Configuração do Ambiente

Primeiro, clone o repositório e configure seu ambiente local.

```bash
# Clone o projeto (se aplicável)
# git clone ...
# cd assistente_ia_final

# 1. Crie seu arquivo de ambiente a partir do exemplo
cp .env.example .env

# 2. Edite o .env para adicionar suas chaves de API e configurar os modelos padrão
nano .env
```

### 2\. Iniciando o Servidor com Ollama (se aplicável)

Se for usar modelos locais, abra um terminal **separado** e inicie o serviço do Ollama para que ele aceite conexões de rede.

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

### 3\. Construindo e Iniciando o Assistente de IA

Com o `Makefile`, este processo é muito simples.

```bash
# Construa a imagem Docker. Isso só precisa ser feito uma vez ou quando o código mudar.
make build

# Inicie o servidor em segundo plano (modo "detached")
make start-d

# Verifique os logs para garantir que tudo iniciou corretamente
make logs
```

Seu "Assistente de IA como um Serviço" agora está rodando e acessível em `http://localhost:8000`.

## Como Usar as Funcionalidades

A maneira mais fácil de interagir com o projeto é através dos comandos `make`. Para ver todos os comandos disponíveis, execute:

```bash
make help
```

### Exemplos de Comandos

#### Planejar uma Nova Feature

```bash
make plan desc="Adicionar um sistema de notificações por email para novos pedidos"
```

Este comando envia a descrição para o endpoint `/plan-feature` da sua API, que usará o modelo configurado para planejamento e retornará um plano técnico detalhado.

#### Gerar Documentação de um Projeto

Para usar esta funcionalidade, você precisa rodar o contêiner montando o volume do projeto que deseja documentar. O `Makefile` pode ser adaptado para isso, mas uma chamada direta ao `docker` ilustra o conceito:

```bash
# Pare o servidor atual se estiver rodando
make stop

# Inicie o servidor montando o projeto alvo na pasta /target_project
docker run -d --rm -p 8000:8000 --env-file ./.env \
  -v "/caminho/completo/para/seu/outro/projeto:/target_project" \
  --name ai_assistant_server \
  assistente-ia:latest

# Agora, chame o comando 'make'
make docs path="/target_project"
```

#### Parar o Servidor

```bash
make stop
```

## Configuração Avançada

A flexibilidade do assistente vem da sua capacidade de configuração externa.

  * **`prompts/*.md`**: Para mudar o comportamento de uma tarefa, simplesmente edite o arquivo de prompt correspondente. Por exemplo, para fazer o planejador de features mais ou menos detalhado, edite o `prompts/planning.md`. Não é necessário reiniciar o servidor.
  * **`config/llm_settings.yaml`**: Para ajustar a "criatividade" (temperatura) ou outros parâmetros de um modelo para uma tarefa específica, edite este arquivo.
  * **`.env`**: Este arquivo controla tudo. Você pode mudar o provedor padrão de `OLLAMA` para `OPENAI` alterando a variável `DEFAULT_PROVIDER`. Você pode forçar uma tarefa específica a usar um modelo diferente definindo, por exemplo, `DOCS_MODEL_IDENTIFIER=GEMINI:gemini-1.5-pro`. O sistema aplicará as mudanças na próxima vez que o contêiner for iniciado.
