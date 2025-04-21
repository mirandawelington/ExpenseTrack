import pandas as pd

def limpar_itau(df):
    df['Valor'] = df['Valor'].str.replace(',', '.', regex=False).astype(float)
    return df

def preparar_dados(df):
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    df['Mes'] = df['Data'].dt.to_period('M').astype(str)
    df['Tipo'] = df['Valor'].apply(lambda x: 'Receita' if x > 0 else 'Despesa')
    return df