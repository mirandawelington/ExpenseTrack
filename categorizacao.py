def categorizar_por_descricao(descricao):
    descricao = str(descricao).lower()
    categorias = {
        'Renda': ['transferência recebida'],
        'Pagamento via Pix': ['transferência enviada pelo pix'],
        'Vestuário': ['midway s/a'],
        'Alimentação': ['dois amores', 'tempero', 'bar', 'queerioca', 'macarrao', 'ifood', 'restaurante', 'spid', 'supermercado'],
        'Transporte': ['uber', '99', 'gasolina', 'combustível'],
        'Lazer': ['cinema', 'netflix', 'spotify'],
        'Moradia': ['aluguel', 'light', 'claro'],
        'Educação': ['antares'],
        'Pagamento Empréstimo': ['empréstimo'],
        'Saúde': ['drogaria'],
        'Cartão de Crédito': ['fatura'],
        'Transferencia para Wilsiane': ['wilsiane'],
        'Gastos com Pet': ['pet'],
        'Vícios': ['tabacaria', 'banca', 'marcello', 'rodrigo', 'samuel'],
        'Dentista *Reembolso': ['ton susy']
    }
    for categoria, palavras in categorias.items():
        for palavra in palavras:
            if palavra in descricao:
                return categoria
    return 'Não mapeado'

def aplicar_categorizacao(df):
    df['Categoria'] = df['Descrição'].apply(categorizar_por_descricao)
    return df