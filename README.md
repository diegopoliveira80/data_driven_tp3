# Aplicação Arquitetura de LangChain

## Problema: 
Durante a pandemia e em períodos de surto de doenças infecciosas como a COVID-19, muitas pessoas buscam informações confiáveis e rápidas sobre o vírus, seus sintomas e possíveis orientações de saúde. No entanto, a sobrecarga de informações e a dificuldade de interpretar sintomas podem gerar confusão e decisões inadequadas. Há uma necessidade de uma solução que combine precisão, acessibilidade e personalização na orientação sobre a COVID-19.

## Vatangens: 
A aplicação configurada com agent facilita a busca de informações e rapidas pelo usuario, sem a necessidade de buscar informações em sites que nao seja confiaveis.

## Principais Funcionalidades Planejadas

    Respostas sobre perguntas sobre a COVID-19:
        tools : 
        1. Cobertura de tópicos como sintomas, medidas preventivas, vacinação, tratamentos e restrições.
            https://api.python.langchain.com/en/latest/community/utilities/langchain_community.utilities.google_serper.GoogleSerperAPIWrapper.html#langchain_community.utilities.google_serper.GoogleSerperAPIWrapper
        2. Analisa os sintomas informados pelo usuário (ex.: febre, tosse, falta de ar)
            https://python.langchain.com/docs/integrations/tools/you/
    


    Prompt específico para cada funcionalidade:
        1. Um prompt para a ferramenta de busca de informações gerais.
        2. Outro prompt para a triagem de sintomas, orientando o modelo a interpretar e oferecer a resposta mais adequada.


    Histórico de interação:
        Registro das perguntas e respostas para personalizar as interações e evitar redundância.


## Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.8 ou superior**
- arquivo requirements.txt

## Execultar aplicacao
### 1° Clone o repositório
### 2° Crie e ative um ambiente virtual
### 3° Instale as dependências requirements.txt
### 4° import as chaves API necessarias para o sistema 
    (gemini.google.com, https://api.you.com., https://serper.dev)
### 4° Inicie Streamlit
    streamlit run main.py
### 5° Utilizar a ferramenta com perguntas a IA

