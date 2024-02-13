# HERBERT_BATISTA_DDF_SOLUTIONS_022024


## Item 1 - Sobre Solutions Engineering

## Item  2 - Sobre a Dadosfera
Os dados foram carregados e podem ser acessados no [link](https://app.dadosfera.ai/pt-BR/catalog/data-assets/3081b3aa-f108-4c17-a140-e679d8dd81c6).  
Foram inseridos metadados para descrever as colunas e adicionadas TAGs para facilitar a localização da tabela, conforme as imagens a seguir.  
  
![Tabela no Catálogo](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/860dcd93-269e-4413-81d3-8cd8f3bfe0a1)  
  
![Documentação](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/1cb33782-cd29-467c-91af-b23b304493b8)





## Item 3 - Sobre GenAI e LLMs

Para esta etapa foi utilizado o LLM GPT-3.  
O Script utilizado para gerar as features para os produtos pode ser visto no [link](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/blob/main/Case%20Tecnico%20Dadosfera.ipynb).  
  
Como estratégia para tentar gerar features mais coesas que pudessem ser utilizadas para analisar os produtos, foram utilizados algumas táticas de prompt engineering, como:  
- Dar instruções claras ao modelo;
- Limitar a quantidade de features que seriam geradas;
- Separar as tarefas em etapas.

O comando utilizado para dar instruções ao modelo LLM pode ser visto abaixo:

```
def generate_features(title, text, client):  
    # Fazer a chamada à API GPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # Modelo GPT-3 
        #model="gpt-4-turbo-preview",  # Modelo GPT-4
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """
            You will be provided with a product title and description, and your task is:
            STEP 1: to generate product names. 
            STEP 2: Generate the following features for this product in JSON format: 
                Product Name,
                Generic Product Type, 
                Category, 
                Sub-Category, 
                Material, 
                Main Function, 
                Color, 
                Target Public, 
                Average Price.   
            
            Please observe the following rules. 
            
                - The features need to be composed by a single term.
                
                - Try to summarize the Product Name.
                
                - For the Material, if it is composed by multiple materials, choose what is more present.
                
                - For the Price feature, you must make an inference based on your knowledge and provide a single value
                in US dollars in float format.                
                             
                - The features need to be simple and generic, 
                so we can classify multiple products and create analysis of them.
                
            """},
            {"role": "user", "content": f"Product title: '{title}' and description: '{text}'"}  
        ],        
    )
    # Extrair e retornar a resposta gerada
    return response.choices[0].message.content
```

## Item  4 - Sobre SQL e Python

Para esta etapa foram criadas as seguintes consultas e visualizações.  

A coleção de itens pode ser acessada no [link](https://metabase-treinamentos.dadosfera.ai/collection/339-herbert-batista-022024).  

- ### [Quantidade por categoria](https://metabase-treinamentos.dadosfera.ai/question/674-quantidade-por-categoria)
### SQL  
  
```
select CATEGORY, count(*) as QTD from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
group by CATEGORY
order by count(*) desc
LIMIT 10
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/08006921-5768-49df-a8ec-2c9700837fc5)  

- ### [Top 5 Main Function](https://metabase-treinamentos.dadosfera.ai/question/676-top-5-main-functions)
### SQL  
```
select MAIN_FUNCTION, count(*) as QTD from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
group by MAIN_FUNCTION
order by count(*) desc
LIMIT 5
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/0bb956c2-16f7-4e01-bc00-e21618e56070)  

- ### [Top 5 Target Public](https://metabase-treinamentos.dadosfera.ai/question/677-top-5-target-public)  
### SQL  
```
select TARGET_PUBLIC, count(*) as QTD from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
group by TARGET_PUBLIC
order by count(*) desc
LIMIT 5
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/a41147b0-dbb1-4ef8-ab8e-876c3e31e5d6)  

- ### [Maior Preço Médio por Categoria](https://metabase-treinamentos.dadosfera.ai/question/679-maior-preco-medio-por-categoria)  
### SQL  
```
select CATEGORY, avg(AVERAGE_PRICE) as AVG_PRICE 
from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
WHERE TRY_CAST(AVERAGE_PRICE AS NUMBER) IS NOT NULL
group by CATEGORY
order by avg(AVERAGE_PRICE) desc
LIMIT 10
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/f79c4fb0-87cb-47b4-a44d-d3c78cb4ea5b)  

- ### [Maior Preço Médio por Função Principal](https://metabase-treinamentos.dadosfera.ai/question/682-maior-preco-medio-por-funcao-principal)  
### SQL  
```
select MAIN_FUNCTION, avg(AVERAGE_PRICE) as AVG_PRICE 
from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
WHERE TRY_CAST(AVERAGE_PRICE AS NUMBER) IS NOT NULL
group by MAIN_FUNCTION
order by avg(AVERAGE_PRICE) desc
LIMIT 10
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/ea4d76aa-8218-443e-a086-78ffab27e358)  

- ### [Maior Preço Médio por Público Alvo](https://metabase-treinamentos.dadosfera.ai/question/681-maior-preco-medio-por-publico-alvo)  
### SQL  
```
select TARGET_PUBLIC, avg(AVERAGE_PRICE) as AVG_PRICE 
from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
WHERE TRY_CAST(AVERAGE_PRICE AS NUMBER) IS NOT NULL
group by TARGET_PUBLIC
order by avg(AVERAGE_PRICE) desc
LIMIT 10
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/7cb73a77-5746-45c4-a765-3925f790df08)  

- ### [Materiais mais frequentes por Categoria](https://metabase-treinamentos.dadosfera.ai/question/680-materiais-mais-frequentes-por-categoria)  
### SQL  
```
select CATEGORY, MATERIAL, count(MATERIAL) as AVG_PRICE 
from TB__B69UWW__CORPUS_SIMPLE_WITH_FEATURES
group by CATEGORY, MATERIAL
order by count(MATERIAL) desc
LIMIT 10
```
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/6069a151-552e-4a28-b741-a9e04f8cb251)  


- ### [Dashboard](https://metabase-treinamentos.dadosfera.ai/dashboard/80-analise-de-produtos)
![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/0625364a-87d3-4772-8818-d5ceee55abaa)  



## Item  5 - Sobre Data Apps

O projeto do Data App no módulo Inteligência pode ser acessado no [link](https://app-intelligence-treinamentos.dadosfera.ai/pipeline?project_uuid=6640cc65-0638-4ae2-bc5e-b1074c786670&pipeline_uuid=29050f4d-44a7-46e7-bf25-ec07deac3919&)  

Foram desenvolvidas duas página. A primeira mostra um dropbox para seleção de um produto e a seguir lista os produtos mais similares utilizando a similaridade de cosseno.  

Na parte lateral foram inseridos três sliders que alteram os parâmetros window, vector_size e min_count do modelo word2vec.  

![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/1bcd4448-044d-4464-9c8b-0aab203820da)  

A segunda página mostra os dez produtos mais similares ao produto selecionado utilizando a distância de Jaccard.

![image](https://github.com/herbertab/HERBERT_BATISTA_DDF_SOLUTIONS_022024/assets/17315911/7502fe5e-7a1e-4cf6-a26d-34c34fe103bb)



















