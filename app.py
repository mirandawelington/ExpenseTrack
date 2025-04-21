import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from PIL import Image

# Seus imports continuam iguais
from leitura_dados import carregar_arquivos_txt, carregar_arquivos_csv
from limpeza_dados import limpar_itau, preparar_dados
from categorizacao import aplicar_categorizacao
from analise import resumo_por_categoria, balanco_mensal
from relatorio import gerar_relatorio_pdf

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RelatorioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatório de Gastos - 2025")
        self.root.geometry("640x420")

        self.itau_files = []
        self.nubank_files = []

        main_frame = ctk.CTkFrame(root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Frame de botões
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=0, column=0, padx=20, pady=20)

        title = ctk.CTkLabel(button_frame, text="Automatizador de Relatório de Gastos", font=("Helvetica", 16))
        title.pack(pady=10)

        btn_nubank = ctk.CTkButton(button_frame, text="Carregar extratos Nubank",
                                   fg_color="#8A05BE", hover_color="#6E0497",
                                   command=self.selecionar_nubank, width=250)
        btn_nubank.pack(pady=5)

        btn_itau = ctk.CTkButton(button_frame, text="Carregar os extratos do banco Itaú",
                                 fg_color="#F27405", hover_color="#D15F03",
                                 command=self.selecionar_itau, width=250)
        btn_itau.pack(pady=5)

        btn_gerar = ctk.CTkButton(button_frame, text="Gerar Relatório",
                                  fg_color="#7F8C8D", hover_color="#626E70",
                                  command=self.gerar_relatorio, width=250)
        btn_gerar.pack(pady=20)

        self.status = ctk.CTkLabel(button_frame, text="", text_color="blue")
        self.status.pack()

        # Frame do usuário (mais largo)
        user_frame = ctk.CTkFrame(main_frame)
        user_frame.grid(row=0, column=1, padx=20, pady=20)
        user_frame.grid_propagate(False)

        user_name = os.getlogin()

       

        # Ícone do usuário (opcional)
        try:
            user_img = ctk.CTkImage(dark_image=Image.open("img/profile_icon.jpeg"), size=(120, 100))
        except:
            user_img = None

        user_label = ctk.CTkLabel(
            user_frame,
            text=f"{user_name}",
            image=user_img,
            compound="top",
            wraplength=360,
            font=("Helvetica", 12),
            justify="center",
            anchor="center"
        )
        user_label.place(relx=0.5, rely=0.75, anchor="center")  # Centralizado na parte inferior
        user_label.pack(pady=10)

    def selecionar_itau(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione arquivos .txt do Itaú",
            filetypes=[("Arquivos TXT", "*.txt")]
        )
        if not arquivos:
            messagebox.showwarning("Atenção", "Nenhum arquivo .txt selecionado!")
            return
        self.itau_files = arquivos
        self.status.configure(text="Arquivos Itaú carregados.")

    def selecionar_nubank(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione arquivos .csv do Nubank",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        if not arquivos:
            messagebox.showwarning("Atenção", "Nenhum arquivo .csv selecionado!")
            return
        self.nubank_files = arquivos
        self.status.configure(text="Arquivos Nubank carregados.")

    def gerar_relatorio(self):
        if not self.itau_files or not self.nubank_files:
            messagebox.showerror("Erro", "Selecione arquivos do Itaú e do Nubank antes de continuar.")
            return

        try:
            colunas = ['Data', 'Descrição', 'Valor']
            df_itau = carregar_arquivos_txt(self.itau_files, colunas)
            df_nubank = carregar_arquivos_csv(self.nubank_files)

            df_itau = limpar_itau(df_itau)
            df_final = pd.concat([df_nubank, df_itau], ignore_index=True)
            df_final = preparar_dados(df_final)
            df_final = aplicar_categorizacao(df_final)

            tabela_resumo, gasto_por_categoria, labels = resumo_por_categoria(df_final)
            soma_pos, soma_neg, sub_pos, sub_neg, balanco = balanco_mensal(df_final)

            gerar_relatorio_pdf(tabela_resumo, labels, gasto_por_categoria, soma_pos, soma_neg, sub_pos, sub_neg, balanco)

            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Algo deu errado:\n{str(e)}")

if __name__ == '__main__':
    root = ctk.CTk()
    app = RelatorioApp(root)
    root.mainloop()


