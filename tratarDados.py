import pandas as pd
import re
import numpy as np

# Carregar o arquivo Excel para um DataFrame
df = pd.read_excel('airbnb_dados.xlsx')

# Função para remover caracteres especiais
def limpar_texto(texto):
    if isinstance(texto, str):
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto
    else:
        return texto

# Função para remover letras e manter apenas números
def limpar_e_converter(texto):
    texto = re.sub(r'[^0-9]', '', str(texto))  # Remove letras e caracteres especiais
    texto = re.sub(r'\s+', '', texto)  # Remove espaços em branco
    if texto:  # Verifica se há texto após a limpeza
        return int(texto)  # Converte para inteiro
    else:
        return np.nan 

# Aplicar as funções de limpeza aos dados do DataFrame
df['titulo'] = df['titulo'].apply(limpar_texto)
df['localizacao'] = df['localizacao'].apply(limpar_texto)
df['valor'] = df['valor'].apply(limpar_e_converter)
df['hospedes'] = df['hospedes'].apply(limpar_e_converter)
df['quartos'] = df['quartos'].apply(limpar_e_converter)
df['camas'] = df['camas'].apply(limpar_e_converter)
df['banheiros'] = df['banheiros'].apply(limpar_e_converter)

# Remover linhas com valores nulos após a limpeza
df = df.dropna()

# Salvar o DataFrame de volta para um arquivo Excel
df.to_excel('dados_tratados.xlsx', index=False)
