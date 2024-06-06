import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados
@st.cache_data
def carregar_dados(caminho):
    try:
        dados = pd.read_csv(caminho)
        
        # Dicionário para renomear colunas
        colunas_traduzidas = {
            'Patient_ID': 'ID_Paciente',
            'Age': 'Idade',
            'Gender': 'Genero',
            'Smoking_History': 'Historico_Fumo',
            'Tumor_Size_mm': 'Tamanho_Tumor_mm',
            'Tumor_Location': 'Localizacao_Tumor',
            'Stage': 'Estagio',
            'Treatment': 'Tratamento',
            'Survival_Months': 'Meses_Sobrevivencia',
            'Ethnicity': 'Etnia',
            'Insurance_Type': 'Tipo_Seguro',
            'Family_History': 'Historico_Familiar',
            'Comorbidity_Diabetes': 'Comorbidade_Diabetes',
            'Comorbidity_Hypertension': 'Comorbidade_Hipertensao'
        }

        # Renomear colunas
        dados.rename(columns=colunas_traduzidas, inplace=True)
        
        # Traduzir valores das colunas específicas
        if 'Historico_Fumo' in dados.columns:
            dados['Historico_Fumo'] = dados['Historico_Fumo'].replace({
                'Current Smoker': 'Fumante Atual',
                'Never Smoked': 'Nunca Fumou',
                'Former Smoker': 'Ex-Fumante'
            })

        if 'Genero' in dados.columns:
            dados['Genero'] = dados['Genero'].replace({
                'Female': 'Feminino',
                'Male': 'Masculino'
            })

        if 'Estagio' in dados.columns:
            dados['Estagio'] = dados['Estagio'].replace({
                'Stage I': 'Estagio I',
                'Stage II': 'Estagio II',
                'Stage III': 'Estagio III',
                'Stage IV': 'Estagio IV'
            })

        if 'Tratamento' in dados.columns:
            dados['Tratamento'] = dados['Tratamento'].replace({
                'Radiation Therapy': 'Terapia de Radiacao',
                'Targeted Therapy': 'Terapia Alvo',
                'Chemotherapy': 'Quimioterapia',
                'Surgery': 'Cirurgia'
            })
        
        if 'Tipo_Seguro' in dados.columns:
            dados['Tipo_Seguro'] = dados['Tipo_Seguro'].replace({
                'Medicaid': 'Medicaid',
                'Other': 'Outro',
                'Medicare': 'Medicare',
                'Private': 'Privado'
            })

        return dados
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# Função para carregar CSS
def carregar_css(caminho_css):
    with open(caminho_css) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Caminho para o arquivo CSS
caminho_css = 'styles.css'
carregar_css(caminho_css)

# Caminho para o arquivo CSV
caminho_dados = 'meu_dashboard/data/lung_cancer_data.csv'  # Atualize o caminho para o seu arquivo

# Carregar dados
df = carregar_dados(caminho_dados)

# Verifica se os dados foram carregados com sucesso
if df is not None:
    # Barra lateral
    st.sidebar.title('Configurações do Painel')
    st.sidebar.write('Nome: Rafael Rodrigues')
    st.sidebar.write('PDITA: 394')
    
    # Opção para escolher o gráfico
    grafico = st.sidebar.selectbox(
        'Selecione o gráfico que deseja visualizar:',
        ['Dados Brutos', 'Estatísticas Descritivas', 'Distribuição de Idade', 'Filtrar por Gênero', 'Filtrar por Histórico de Fumo', 'Distribuição dos Estágios', 'Tamanho do Tumor por Idade', 'Tamanho do Tumor por Idade e Histórico de Fumo']
    )

    # Título da aplicação
    st.title('Análise de Dados de Câncer de Pulmão')

    # Mostrar dados brutos
    if grafico == 'Dados Brutos':
        st.subheader('Dados Brutos')
        st.write(df.head())

    # Estatísticas descritivas
    elif grafico == 'Estatísticas Descritivas':
        st.subheader('Estatísticas Descritivas')
        st.write(df.describe())

    # Distribuição de idade
    elif grafico == 'Distribuição de Idade':
        if 'Idade' in df.columns:
            st.subheader('Distribuição de Idade')
            distribuicao_idade = df['Idade'].value_counts().sort_index()
            st.bar_chart(distribuicao_idade)
        else:
            st.error("A coluna 'Idade' não foi encontrada no DataFrame.")

    # Filtrar por Gênero
    elif grafico == 'Filtrar por Gênero':
        if 'Genero' in df.columns:
            st.subheader('Filtrar por Gênero')
            genero = st.selectbox('Selecione o Gênero', df['Genero'].unique())
            dados_filtrados_genero = df[df['Genero'] == genero]
            st.write(dados_filtrados_genero)
        else:
            st.error("A coluna 'Genero' não foi encontrada no DataFrame.")

    # Filtrar por Histórico de Fumo
    elif grafico == 'Filtrar por Histórico de Fumo':
        if 'Historico_Fumo' in df.columns:
            st.subheader('Filtrar por Histórico de Fumo')
            historico_fumo = st.selectbox('Selecione o Histórico de Fumo', df['Historico_Fumo'].unique())
            dados_filtrados_fumo = df[df['Historico_Fumo'] == historico_fumo]
            st.write(dados_filtrados_fumo)
        else:
            st.error("A coluna 'Historico_Fumo' não foi encontrada no DataFrame.")

    # Distribuição dos Estágios
    elif grafico == 'Distribuição dos Estágios':
        if 'Estagio' in df.columns:
            st.subheader('Distribuição dos Estágios')
            distribuicao_estagios = df['Estagio'].value_counts().sort_index()
            st.bar_chart(distribuicao_estagios)
        else:
            st.error("A coluna 'Estagio' não foi encontrada no DataFrame.")

    # Tamanho do Tumor por Idade
    elif grafico == 'Tamanho do Tumor por Idade':
        if 'Idade' in df.columns and 'Tamanho_Tumor_mm' in df.columns and 'Genero' in df.columns:
            st.subheader('Tamanho do Tumor por Idade')
            fig = px.scatter(df, x='Idade', y='Tamanho_Tumor_mm', color='Genero', title='Tamanho do Tumor por Idade')
            st.plotly_chart(fig)
        else:
            st.error("Colunas necessárias para o gráfico de Tamanho do Tumor por Idade não foram encontradas no DataFrame.")

    # Tamanho do Tumor por Idade e Histórico de Fumo
    elif grafico == 'Tamanho do Tumor por Idade e Histórico de Fumo':
        if 'Idade' in df.columns and 'Tamanho_Tumor_mm' in df.columns and 'Historico_Fumo' in df.columns:
            st.subheader('Tamanho do Tumor por Idade e Histórico de Fumo')
            fig2 = px.scatter(df, x='Idade', y='Tamanho_Tumor_mm', color='Historico_Fumo', title='Tamanho do Tumor por Idade e Histórico de Fumo')
            st.plotly_chart(fig2)
        else:
            st.error("Colunas necessárias para o gráfico de Tamanho do Tumor por Idade e Histórico de Fumo não foram encontradas no DataFrame.")
else:
    st.error('Falha ao carregar os dados.')
