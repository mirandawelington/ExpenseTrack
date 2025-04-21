import pandas as pd

def carregar_arquivos_txt(lista_arquivos, colunas):
    frames = [pd.read_csv(arquivo, sep=';', names=colunas) for arquivo in lista_arquivos]
    return pd.concat(frames, ignore_index=True)

def carregar_arquivos_csv(lista_arquivos):
    frames = [pd.read_csv(arquivo) for arquivo in lista_arquivos]
    df = pd.concat(frames, ignore_index=True)
    return df[['Data', 'Valor', 'Descrição']]
