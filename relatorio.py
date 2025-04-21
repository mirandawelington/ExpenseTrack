import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def gerar_relatorio_pdf(tabela_resumo, labels_legenda, gasto_por_categoria,
                         soma_positivos, soma_negativos, subtotal_positivos,
                         subtotal_negativos, balanco):
    with PdfPages("relatorio_despesas.pdf") as pdf:
        # Gráfico
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        ax1.pie(gasto_por_categoria.values, labels=None, startangle=90)
        ax1.legend(labels=labels_legenda, title="Categorias", bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.set_title('Despesas por Categoria')
        plt.tight_layout()
        pdf.savefig(fig1)
        plt.close()

        # Tabela
        fig2, ax2 = plt.subplots(figsize=(15, len(tabela_resumo) * 0.5 + 1))
        ax2.axis('off')
        ax2.set_title('Resumo das Despesas por Categoria', fontsize=14, fontweight='bold')
        tabela_plotada = ax2.table(cellText=tabela_resumo.values,
                                   colLabels=tabela_resumo.columns,
                                   rowLabels=tabela_resumo.index,
                                   cellLoc='center', loc='center')
        tabela_plotada.auto_set_font_size(False)
        tabela_plotada.set_fontsize(8)
        tabela_plotada.scale(1, 1.5)
        pdf.savefig(fig2)
        plt.close()

        # Texto
        fig3, ax3 = plt.subplots(figsize=(8.27, 11.69))  # A4
        ax3.axis('off')
        texto = f"""
Subtotal positivo: R$ {subtotal_positivos:.2f}
Soma dos valores positivos por mês:
{soma_positivos.to_string()}

Soma dos valores negativos por mês:
{soma_negativos.to_string()}

Subtotal negativo: R$ {subtotal_negativos:.2f}
Balanço patrimonial: R$ {balanco:.2f}
        """
        ax3.text(0.5, 0.5, texto, ha='center', va='center', fontsize=12, wrap=True)
        pdf.savefig(fig3)
        plt.close()

    print("✅ PDF 'relatorio_despesas.pdf' gerado com sucesso!")
