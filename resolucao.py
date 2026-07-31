import tkinter as tk
import json
import os
import sys

from ttkbootstrap.widgets import LabelFrame, Label, Button

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

class JanelaResolucao:
    
                
    def __init__(self, master, dados):
        
        self.janela = tk.Toplevel(master)
        self.janela.title("Resolução do Chamado")
        self.janela.geometry("515x650")
        
        self.carregar_resolucoes()
        
        #------------ Dados do usuário ------------#
        frame_usario = LabelFrame(
            self.janela,
            text="Dados do Usuário",
            padding=10
        )
        frame_usario.pack(fill="x", padx=20, pady=10)
        
        Label(frame_usario, text=f"Nome:{dados['nome']}").pack(anchor="w")
        Label(frame_usario, text=f"Matricula:{dados['matricula']}").pack(anchor="w")
        Label(frame_usario, text=f"Contato:{dados['contato']}").pack(anchor="w")
        Label(frame_usario, text=f"Assunto:{dados['assunto']}").pack(anchor="w")
        
        #----------- Procedimento-------------------#
        frame_proc = LabelFrame(
            self.janela, 
            text="Procedimento",
            padding=10
        )
        
        self.lbl_procedimento = Label(
            frame_proc,
            text="",
            justify="left",
            wraplength=650
        )
        
        frame_proc.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.lbl_procedimento.pack(anchor="w")
        
        self.carregar_procedimento(dados["assunto"])
        
        Button(
            self.janela,
            text="Fechar",
            bootstyle="danger",
            command=self.janela.destroy
        ).pack(pady=10)
    
    def carregar_resolucoes(self):
        caminho = resource_path("resolucoes.json")
                
        with open(caminho, "r", encoding="utf-8") as f:
            self.resolucoes = json.load(f)
    
    def carregar_procedimento(self, assunto):
        texto = ""
        
        print("Assunto recebido:", repr(assunto))
        print("Chave do JSON:")
        
        for chave in self.resolucoes.keys():
            print(repr(chave))

        if assunto in self.resolucoes:
            dados = self.resolucoes[assunto]
            
            for passo in dados["procedimento"]:
                text += f"{passo}\n"
        else:
            texto = "Nenhum procedimento cadstr"    
        
        #if assunto in self.resolucoes:
            
        #    dados = self.resolucoes[assunto]
            
        #    texto = ""
            
        #    for passo in dados["procedimento"]:
        #        texto += f"{passo}\n"
        #else:
        #    texto = "Nenhum procedimento cadastrado."
            
        self.lbl_procedimento.config(text=texto) 
        
        
        