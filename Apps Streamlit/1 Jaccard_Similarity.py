import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

# Função para calcular a similaridade de Jaccard entre dois textos
def jaccard_similarity(text1, text2):
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union if union != 0 else 0

    
# Leitura do arquivo CSV
df = pd.read_csv("corpus-simple_head.csv")
df['text'] = [str(t) for t in df['text']]

# Ordena o DataFrame pelo nome do produto em ordem alfabética
df = df.sort_values(by="Product Name")

# Interface do Streamlit
st.title("App de Similaridade de Produtos")

# Seleção do produto
selected_product = st.selectbox("Escolha um produto:", df["Product Name"])

# Cálculo da similaridade de Jaccard
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])
jaccard_scores = [jaccard_similarity(df["text"].iloc[df[df["Product Name"] == selected_product].index[0]], df["text"].iloc[i]) for i in range(len(df))]

# Obtenção dos produtos mais similares
similar_products = pd.DataFrame({
    "Product Name": df["Product Name"],
    "Similarity Score": jaccard_scores
})
similar_products = similar_products.sort_values(by="Similarity Score", ascending=False).head(10)

# Exibição dos produtos mais similares
st.subheader("Produtos Mais Similares:")
st.table(similar_products[["Product Name", "Similarity Score"]])
