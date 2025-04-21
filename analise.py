import pandas as pd

def resumo_por_categoria(df):
    despesas = df[df['Tipo'] == 'Despesa']
    gasto_por_categoria = despesas.groupby('Categoria')['Valor'].sum().abs()
    total = gasto_por_categoria.sum()
    labels = [f"{categoria} - ({valor / total:.1%})" for categoria, valor in gasto_por_categoria.items()]
    tabela = pd.DataFrame({
        'Valor Total (R$)': gasto_por_categoria,
        '% do Total': (gasto_por_categoria / total * 100).round(1).astype(str) + '%'
    })
    tabela['Valor Total (R$)'] = tabela['Valor Total (R$)'].map(
        lambda x: f"R$ {x:,.2f}".replace('.', ',').replace(',', 'v', 1).replace('.', ',').replace('v', '.'))
    return tabela, gasto_por_categoria, labels

def balanco_mensal(df):
    positivos = df[df['Valor'] > 0]
    negativos = df[df['Valor'] < 0]
    soma_positivos = positivos.groupby('Mes')['Valor'].sum()
    soma_negativos = negativos.groupby('Mes')['Valor'].sum()
    subtotal_positivos = soma_positivos.sum()
    subtotal_negativos = soma_negativos.sum()
    balanco = subtotal_positivos + subtotal_negativos
    return soma_positivos, soma_negativos, subtotal_positivos, subtotal_negativos, balanco
