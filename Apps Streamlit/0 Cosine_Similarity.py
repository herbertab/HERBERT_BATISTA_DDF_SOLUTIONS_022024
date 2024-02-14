import streamlit as st
import pandas as pd
import spacy
import re
import nltk
import string
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("en_core_web_sm")
# Carregar stopwords nltk
nltk.download('stopwords')

# Carregar dados
@st.cache_data 
def load_data():
    file_path = "corpus-simple_head.csv"
    data = pd.read_csv(file_path)
    # Ordena o DataFrame pelo nome do produto em ordem alfabética
    data = data.sort_values(by="Product Name")
    return data

# Pré-processamento e tokenização com spaCy e NLTK
def preprocess_text(text):
    text = str(text)  # Garante que a entrada seja tratada como uma string
    # Pre processing
    text = re.findall(r"\w+(?:'\w+)?|[^\w\s]", text) # pré tokenização
    text = [t.lower() for t in text] # Conversão para texto em minúsculos
    stpw = stopwords.words('english')
    text = [t for t in text if t not in stpw] # Remoção de Stopwords
    text = [re.sub(r"\d", '', t) for t in text] # Remoção de dígitos
    text = [t for t in text if t not in string.punctuation] # Remoção de pontuação
    text = " ".join(text)
    
    # Tokenização    
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if token.is_alpha]
    return tokens

# Aplicar o pré-processamento ao texto
data = load_data()
data['text'] = data['text'].apply(preprocess_text)

# Barra lateral do Streamlit com o slider
window_size = st.sidebar.slider("Window Size (Word2Vec)", min_value=1, max_value=100, value=20)
vector_size = st.sidebar.slider("Vector Size (Word2Vec)", min_value=10, max_value=500, value=200)
min_count = st.sidebar.slider("Min Count (Word2Vec)", min_value=1, max_value=20, value=1)

# Treinamento do modelo Word2Vec
def get_word2vec_model(vec_size, window_size, mincount):
    model = Word2Vec(sentences=data['text'], vector_size=vec_size, window=window_size, min_count=mincount, workers=4)
    return model
model = get_word2vec_model(vector_size, window_size, min_count)

# Calcular a representação vetorial média para cada produto
def text_to_vector(tokens):
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if not vectors:
        return None
    return sum(vectors) / len(vectors)

data['vector_representation'] = data['text'].apply(text_to_vector)

# Calcular a similaridade
def calculate_similarity_vectors(v1, v2):
    if v1 is None or v2 is None:
        return None
    v1 = normalize(v1.reshape(1, -1))
    v2 = normalize(v2.reshape(1, -1))
    return cosine_similarity(v1, v2)[0][0]

# Criar o aplicativo Streamlit
st.title("Top 50 Produtos Mais Similares")

# Selecionar um produto para comparar
selected_product = st.selectbox("Selecione um Produto", data['Product Name'])

# Calcular a similaridade entre o produto selecionado e todos os outros produtos
similarities = []
selected_product_vector = data[data['Product Name'] == selected_product]['vector_representation'].values[0]

for index, row in data.iterrows():
    product_vector = row['vector_representation']
    similarity = calculate_similarity_vectors(selected_product_vector, product_vector)
    similarities.append((row['Product Name'], similarity))

# Ordenar por similaridade em ordem decrescente
similarities.sort(key=lambda x: x[1], reverse=True)

# Exibir os top 10 produtos em um gráfico de barras
#top_products = similarities[:10]
#fig, ax = plt.subplots()
#products, scores = zip(*top_products)
#ax.barh(products, scores)
#ax.set_xlabel("Similaridade de Cosseno")
#ax.set_title(f"Top 10 Produtos Mais Similares a {selected_product}")
#st.pyplot(fig)







    # Exibir os top 50 produtos mais similares
st.write(f"Top 50 Produtos Mais Similares a {selected_product}:")
for i, (product, similarity) in enumerate(similarities[:50], 1):
    st.write(f"{i}. {product} - Similaridade: {similarity}")

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")