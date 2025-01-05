import polars as pl
import streamlit as st
import numpy as np
import plotly.express as px

@st.cache_data
def load_eps_rating():
    url = "https://raw.githubusercontent.com/abibernardo/imdb_data/refs/heads/main/diretores_ep.csv"
    return pl.read_csv(
        url,
        null_values=["\\N"],
        dtypes={
            "rating_ep": pl.Float64,
            "numero_ep": pl.Int32,
            "temporada": pl.Utf8,
            "titulo_serie": pl.Utf8
        }
    )

@st.cache_data
def load_periodo_serie():
    url = "https://raw.githubusercontent.com/abibernardo/imdb_data/refs/heads/main/inicio_termino_imdb.csv"
    return pl.read_csv(
        url,
        null_values=["\\N"],
        dtypes={
            "startYear": pl.Utf8,
            "endYear": pl.Utf8,
            "originalTitle": pl.Utf8
        }
    )

@st.cache_data
def load_dados_temporadas():
    url = "https://raw.githubusercontent.com/abibernardo/imdb_data/refs/heads/main/dados_por_temporada_anual_imdb.csv"
    return pl.read_csv(
        url,
        null_values=["\\N"],
        dtypes={
            "ano_temporada": pl.Int32,
            "total_votos_temporada": pl.Int32,
            "media_nota_temporada": pl.Float64
        }
    )

@st.cache_data
def load_dados_eps_ano():
    url = "https://raw.githubusercontent.com/abibernardo/imdb_data/refs/heads/main/nota_pop_eps_imdb.csv"
    return pl.read_csv(
        url,
        null_values=["\\N"],
        dtypes={
            "ano_ep": pl.Int32,
            "votos_ep": pl.Int32,
            "rating_ep": pl.Float64
        }
    )

@st.cache_data
def load_pop_series():
    url = "https://raw.githubusercontent.com/abibernardo/imdb_data/refs/heads/main/inicio_termino_imdb.csv"
    return pl.read_csv(
        url,
        null_values=["\\N"],
        dtypes={
            "startYear": pl.Int32,
            "endYear": pl.Int32,
            "numVotes": pl.Int32,
            "averageRating": pl.Float64
        }
    )
# Carregue os dados
eps_rating = load_eps_rating()
periodo_serie = load_periodo_serie()
dados_temporadas = load_dados_temporadas()
dados_eps_ano = load_dados_eps_ano()
pop_series = load_pop_series()
periodo_serie = periodo_serie.with_columns(pl.col("originalTitle").str.to_lowercase().alias("originalTitle"))
eps_rating = eps_rating.with_columns(pl.col("titulo_serie").str.to_lowercase().alias("titulo_serie"))


st.title("Análise de dados do IMDB")
st.write("**atualizado em 10/2024**")

show = st.text_input("Qual a série que deseja analisar?")
show = show.lower()

if show:
    try:
        col1, col2 = st.columns(2)
        with col1:
            st.title(show)
        if show in ["Hacks", "The Marvelous Mrs. Maisel", "The Bear", "Ted Lasso", "Veep", "Schitt's Creek", "The White Lotus","Fleabag", "Modern Family", "30 Rock", "Everybody Loves Raymond", "Friends", "Arrested Development", "Sex and the City", "Succession", "The Crown", "Game of Thrones", "The Handmaid’s Tale", "Breaking Bad", "Homeland", "Mad Men", "The Sopranos", "Lost"]:
            with col2:
                st.image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHY7JoOc1OQ7ouCNPAozO8_jN_cJ98zQBt0Q&s",
                width=50)
        elif show in ["Twin Peaks"]:
            st.image(
                "https://www.vishows.com.br/wp-content/uploads/2017/05/welcome-to-twin-peaks-1200x628-facebook.jpg",
                width=300)




        serie = periodo_serie.filter(pl.col('originalTitle') == show)
        filtered_eps_rating = eps_rating.filter(pl.col("titulo_serie") == show)
        df_serie = eps_rating.filter(pl.col("titulo_serie") == show)



        ano_inicio = serie['startYear'][0]
        ano_fim = serie['endYear'][0]
        if ano_fim == None:
            st.write(f'## {ano_inicio} - atual')
        else:
            st.write(f'## {ano_inicio} - {ano_fim}')
        # Filtrar os dados da série desejada
        filtered_eps_rating = eps_rating.filter(pl.col("titulo_serie") == show)
        df_serie = eps_rating.filter(pl.col("titulo_serie") == show)
        filtered_eps_rating = filtered_eps_rating.sort("rating_ep", descending=True)
        st.divider()
        ep1 = filtered_eps_rating['titulo_ep'][0]
        ep2 = filtered_eps_rating['titulo_ep'][1]
        ep3 = filtered_eps_rating['titulo_ep'][2]
        ep4 = filtered_eps_rating['titulo_ep'][3]
        ep5 = filtered_eps_rating['titulo_ep'][4]
        nota1 = filtered_eps_rating['rating_ep'][0]
        nota2 = filtered_eps_rating['rating_ep'][1]
        nota3 = filtered_eps_rating['rating_ep'][2]
        nota4 = filtered_eps_rating['rating_ep'][3]
        nota5 = filtered_eps_rating['rating_ep'][4]
        diretor_ep1 = filtered_eps_rating['diretor'][0]
        diretor_ep2 = filtered_eps_rating['diretor'][1]
        diretor_ep3 = filtered_eps_rating['diretor'][2]
        diretor_ep4 = filtered_eps_rating['diretor'][3]
        diretor_ep5 = filtered_eps_rating['diretor'][4]

        st.write("## Melhores episódios")
        st.write(f'**"{ep1}"**, nota {nota1} - dirigido por {diretor_ep1}')
        st.write(f'**"{ep2}"**, nota {nota2} - dirigido por {diretor_ep2}')
        st.write(f'**"{ep3}"**, nota {nota3} - dirigido por {diretor_ep3}')
        st.write(f'**"{ep4}"**, nota {nota4} - dirigido por {diretor_ep4}')
        st.write(f'**"{ep5}"**, nota {nota5} - dirigido por {diretor_ep5}')

        st.divider()
        por_temporada = df_serie.group_by("temporada").agg([pl.col("rating_ep").mean().alias("media_rating_ep"),pl.col("num_votos").mean().alias("media_num_rating")])

        # Convertendo para Pandas para usar no Streamlit
        por_temporada = por_temporada.to_pandas()
        if df_serie.height > 0:
            st.write(f'### O que quer visualizar sobre {show}?')
            visualisar = st.radio(
                " ",
                ["Análise de avaliação", "Análise de popularidade"])
            if visualisar == "Análise de avaliação":
                st.divider()
                st.subheader("Nota dos episódios")
                st.line_chart(df_serie['rating_ep'].to_pandas(), x_label="Episódios", y_label="Avaliação Média", color="#ffaa00")
                st.divider()
                fig = px.box(df_serie.to_pandas(), x="temporada", y="rating_ep", title="Notas por temporada")
                st.plotly_chart(fig)
                st.line_chart(df_serie.to_pandas(), x="numero_ep", y="rating_ep", color="temporada")
            if visualisar == "Análise de popularidade":
                st.divider()
                st.subheader("Popularidade dos episódios")
                st.line_chart(df_serie['num_votos'].to_pandas(), x_label="Episódios", y_label="Quantidade de avaliações", color="#ff0000")
                st.divider()
                fig = px.box(df_serie.to_pandas(), x="temporada", y="num_votos", title="Popularidade por temporada")
                st.plotly_chart(fig)
                st.line_chart(df_serie.to_pandas(), x="numero_ep", y="num_votos", color="temporada")
    except Exception as e:
        st.write("**Nenhum resultado. Use exatamente o título original, incluindo as letras maiúsculas**")
st.write(" ")
st.divider()
st.write(" ")
