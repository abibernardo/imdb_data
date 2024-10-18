import polars as pl
import streamlit as st
import numpy as np
import statsmodels.api as sm
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


secs = ["Análise de séries", "Melhores da década"]
tickers = secs
ticker = st.sidebar.selectbox("Seções", tickers)
if ticker == "Análise de séries":

    # Título da aplicação
    st.title("ME315: Análise de dados do IMDB")

    # Entrada do usuário
    show = st.text_input("Qual a série que deseja analisar?")

    if show:
        try:
            col1, col2 = st.columns(2)
            with col1:
                st.title(show)
            if show in ["Hacks", "The Marvelous Mrs. Maisel", "The Bear", "Ted Lasso", "Veep", "Schitt's Creek", "The White Lotus","Fleabag", "Modern Family", "30 Rock", "Everybody Loves Raymond", "Friends", "Arrested Development", "Sex and the City", "Succession", "The Crown", "Game of Thrones", "The Handmaid’s Tale", "Breaking Bad", "Homeland", "Mad Men", "The Sopranos", "Lost"]:
                with col2:
                    st.image(
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHY7JoOc1OQ7ouCNPAozO8_jN_cJ98zQBt0Q&s",
                    width=50
                )
            elif show in ["Twin Peaks"]:
                st.image(
                    "https://www.vishows.com.br/wp-content/uploads/2017/05/welcome-to-twin-peaks-1200x628-facebook.jpg",
                    width=300
                )

            serie = periodo_serie.filter(pl.col('originalTitle') == show)
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
else:

    st.title("Quais foram as séries mais populares de cada década?")
    decada = st.radio(
        "Quer ver o top 15 de qual década?",
        ["anos 70", "anos 80", "anos 90", "anos 2000", "anos 2010", "todos os tempos"], key='2')
    if decada == "anos 70":
        anos = pop_series.filter((pl.col('startYear') > 1969) & (pl.col('startYear') < 1980) & (pl.col('endYear') < 1990))
        anos = anos.sort("numVotes", descending=True)
    elif decada == "anos 80":
        anos = pop_series.filter((pl.col('startYear') > 1979) & (pl.col('startYear') < 1990) & (pl.col('endYear') < 2000))
        anos = anos.sort("numVotes", descending=True)
    elif decada == "anos 90":
        anos = pop_series.filter((pl.col('startYear') > 1989) & (pl.col('startYear') < 2000) & (pl.col('endYear') < 2010))
        anos = anos.sort("numVotes", descending=True)
    elif decada == "anos 2000":
        anos = pop_series.filter((pl.col('startYear') > 1999) & (pl.col('startYear') < 2010) & (pl.col('endYear') < 2020))
        anos = anos.sort("numVotes", descending=True)
    elif decada == "anos 2010":
        anos = pop_series.filter((pl.col('startYear') > 2009) & (pl.col('startYear') < 2020))
        anos = anos.sort("numVotes", descending=True)
    else:
        anos = pop_series.sort("numVotes", descending=True)

    popularidade = anos.select([
        pl.col("originalTitle").alias("série"),
        pl.col("numVotes").alias("total de avaliações"),
        pl.col("averageRating").alias("nota média"),
        pl.col("startYear").alias("início"),
        pl.col("endYear").alias("fim")
    ]).limit(15)
    st.dataframe(popularidade, use_container_width=True)
    st.divider()
    st.title("Quais foram as temporadas mais populares de cada década?")
    decada = st.radio(
        "Quer ver o top 30 de qual década?",
        ["anos 70", "anos 80", "anos 90", "anos 2000", "anos 2010", "todos os tempos"])
    if decada == "anos 70":
        anos = dados_temporadas.filter((pl.col('ano_temporada') > 1969) & (pl.col('ano_temporada') < 1980))
        anos = anos.sort("total_votos_temporada", descending=True)
    elif decada == "anos 80":
        anos = dados_temporadas.filter((pl.col('ano_temporada') > 1979) & (pl.col('ano_temporada') < 1990))
        anos = anos.sort("total_votos_temporada", descending=True)
    elif decada == "anos 90":
        anos = dados_temporadas.filter((pl.col('ano_temporada') > 1989) & (pl.col('ano_temporada') < 2000))
        anos = anos.sort("total_votos_temporada", descending=True)
    elif decada == "anos 2000":
        anos = dados_temporadas.filter((pl.col('ano_temporada') > 1999) & (pl.col('ano_temporada') < 2010))
        anos = anos.sort("total_votos_temporada", descending=True)
    elif decada == "anos 2010":
        anos = dados_temporadas.filter((pl.col('ano_temporada') > 2009) & (pl.col('ano_temporada') < 2020))
        anos = anos.sort("total_votos_temporada", descending=True)
    else:
        anos = dados_temporadas.sort("total_votos_temporada", descending=True)


    # Selecionar e renomear as colunas desejadas
    popularidade_70 = anos.select([
        pl.col("nome_da_serie").alias("série"),
        pl.col("temporada"),
        pl.col("total_votos_temporada").alias("total de avaliações"),
        pl.col("media_nota_temporada").alias("nota média"),
        pl.col("ano_temporada").alias("ano")
    ]).limit(30)
    st.dataframe(popularidade_70, use_container_width=True)
    st.divider()
    st.title("Quais foram os episódios mais populares de cada década?")
    decada = st.radio(
        "Quer ver o top 30 de qual década?",
        ["anos 70", "anos 80", "anos 90", "anos 2000", "anos 2010", "todos os tempos"], key='3')
    if decada == "anos 70":
        anos = dados_eps_ano.filter((pl.col('ano_ep') > 1969) & (pl.col('ano_ep') < 1980))
        anos = anos.sort("votos_ep", descending=True)
    elif decada == "anos 80":
        anos = dados_eps_ano.filter((pl.col('ano_ep') > 1979) & (pl.col('ano_ep') < 1990))
        anos = anos.sort("votos_ep", descending=True)
    elif decada == "anos 90":
        anos = dados_eps_ano.filter((pl.col('ano_ep') > 1989) & (pl.col('ano_ep') < 2000))
        anos = anos.sort("votos_ep", descending=True)
    elif decada == "anos 2000":
        anos = dados_eps_ano.filter((pl.col('ano_ep') > 1999) & (pl.col('ano_ep') < 2010))
        anos = anos.sort("votos_ep", descending=True)
    elif decada == "anos 2010":
        anos = dados_eps_ano.filter((pl.col('ano_ep') > 2009) & (pl.col('ano_ep') < 2020))
        anos = anos.sort("votos_ep", descending=True)
    else:
        anos = dados_eps_ano.sort("votos_ep", descending=True)

    # Selecionar e renomear as colunas desejadas
    popularidade_70 = anos.select([
        pl.col("titulo_ep").alias("episódio"),
        pl.col("titulo_serie").alias("série"),
        pl.col("votos_ep").alias("total de avaliações"),
        pl.col("rating_ep").round(2).alias("nota"),
        pl.col("temporada"),
        pl.col("ano_ep").alias("ano")
    ]).limit(30)
    st.dataframe(popularidade_70, use_container_width=True)
    st.divider()
