import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Configurando a chave de API do OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

# Carregando dados do arquivo CSV
df = pd.read_csv("corpus-simple_head.csv")
df = df.sort_values(by="Product Name")

# Lista de produtos em inglês
products = df["Product Name"].tolist()

# Criando um aplicativo Streamlit
st.title("Geração de Imagem com OpenAI DALL-E")

# Selecionando um produto usando um menu suspenso
selected_product = st.selectbox("Select a product:", products)

# Prompt com o nome do produto
prompt = f"An image of the product: {selected_product}"

# Botão para gerar a imagem
if st.button("Generate Image"):
    # Chamada à API para gerar a imagem
    response = openai.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="512x512",
        quality="standard",
        n=1,
    )

    # Obtendo a URL da imagem gerada
    image_url = response.data[0].url

    # Exibindo a imagem
    st.image(image_url, caption="Generated Image", use_column_width=True)

    # Exibindo a URL da imagem
    st.write("Image URL:", image_url)