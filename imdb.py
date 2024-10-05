import polars as pl
import streamlit as st
import numpy as np
import plotly.express as px

eps_rating = pl.read_csv(
    "C:\\Users\\Usuário\\Downloads\\rating_eps (1).csv",
    null_values=["\\N"],
    dtypes={
        "rating_ep": pl.Float64,
        "numero_ep": pl.Int32,
        "temporada": pl.Utf8,
        "titulo_serie": pl.Utf8
    }
)

# Título da aplicação
st.title("ME315: Análise de dados do IMDB")

# Entrada do usuário
show = st.text_input("Qual a série que deseja analisar?")

if show:
    # Filtrar os dados da série desejada
    filtered_eps_rating = eps_rating.filter(pl.col("titulo_serie") == show)
    por_temporada = filtered_eps_rating.group_by("temporada").agg([pl.col("rating_ep").mean().alias("media_rating_ep"),pl.col("num_rating").mean().alias("media_num_rating")])

    # Convertendo para Pandas para usar no Streamlit
    por_temporada = por_temporada.to_pandas()
    if filtered_eps_rating.height > 0:
        st.write(f'### O que quer visualizar sobre {show}?')
        visualisar = st.radio(
            " ",
            ["Análise de avaliação", "Análise de popularidade"])
        if visualisar == "Análise de avaliação":
            st.divider()
            st.subheader("Nota dos episódios")
            st.line_chart(filtered_eps_rating['rating_ep'].to_pandas(), x_label="Episódios", y_label="Avaliação Média", color="#ffaa00")
            st.divider()
            fig = px.box(filtered_eps_rating.to_pandas(), x="temporada", y="rating_ep", title="Notas por temporada")
            st.plotly_chart(fig)
            st.line_chart(filtered_eps_rating.to_pandas(), x="numero_ep", y="rating_ep", color="temporada")
        if visualisar == "Análise de popularidade":
            st.divider()
            st.subheader("Popularidade dos episódios")
            st.line_chart(filtered_eps_rating['num_rating'].to_pandas(), x_label="Episódios", y_label="Quantidade de avaliações", color="#ff0000")
            st.divider()
            fig = px.box(filtered_eps_rating.to_pandas(), x="temporada", y="num_rating", title="Popularidade por temporada")
            st.plotly_chart(fig)
            st.line_chart(filtered_eps_rating.to_pandas(), x="numero_ep", y="num_rating", color="temporada")
    else:
        st.write("Use exatamente o título original, incluindo as letras maiúsculas")
