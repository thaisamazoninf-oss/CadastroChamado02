import os
import sys
import tkinter as tk
from tkinter import messagebox, PhotoImage
from ttkbootstrap import Style
from PIL import Image, ImageTk
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Radiobutton, Combobox, LabelFrame
import action2
import threading
import json

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

class Aplicacao:

######################### INIT #############################################
    def __init__(self, parent):
        self.root = parent

        self.style = Style("flatly")

        self.tipo_var = tk.StringVar()
        self.oab_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.contato_var = tk.StringVar()
        self.cpf_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.matricula_var = tk.StringVar()
        self.assunto_titulo_var = tk.StringVar()
        self.modo_titulo_var = tk.StringVar()
        self.maquina_titulo_var = tk.StringVar()
        self.usuario_formatado = ""
        self.tombo_var= tk.StringVar()

        self.carregar_dados()
        self.criar_interface()


################## Limpar campos ######################
    def limpar_campos(self):
        self.oab_var.set("")
        self.nome_var.set("")
        self.email_var.set("")
        self.contato_var.set("")
        self.cpf_var.set("")
        self.estado_var.set("")
        self.matricula_var.set("")
        self.tombo_var.set("")


################## Iniciar Operação #######################
    def iniciar_operacao(self):
        dados = self.carregar_dados()
        if not dados:
            messagebox.showerror("Erro","Dados invalidos")
            return
            
        threading.Thread(
            target=action2.iniciar_automacao,
            args=(dados,),
            daemon=True
        ).start()
        
    ################## Cancela operação #########################
    def cancelar_operacao(self):
        action2.parar()
            
    ######################### CARREGAR DADOS #############################################

    def carregar_dados(self):
        caminho = resource_path("dados_assyst.json")
        
        with open(caminho,'r', encoding='utf-8') as f:
            dados_assyst = json.load(f)

            #--------- Roda em Theread para não travar a interface
            
            threading.Thread (
                target=action2.iniciar_automacao,
                args=(dados_assyst,),
                daemon=True
            ).start()
            
            #---------- Ordenar lista de assuntos ----------#. 
            assuntos_dict = dados_assyst['assuntos']
            
            assuntos_ordenados= dict(
                sorted(
                    assuntos_dict.items(),
                    key=lambda item: item[1]['titulo'].lower()
                    
                )
            )
            
            self.assuntos = assuntos_ordenados
            self.tipos = dados_assyst['tipos']
            self.modos = dados_assyst['modos']
            self.maquinas = dados_assyst['tipo_maquina']

######################### CRIAR INTERFACE #############################################
    def criar_interface(self):

#---------------------------------- Perfil do Usuário -------------------------------------#

        perfil_frame = LabelFrame(self.root, text="Perfil do Usuário", padding=10)
        perfil_frame.pack(fill='x', padx=20, pady=5)

        for chave, info in self.tipos.items():
            Radiobutton(perfil_frame, text=info['perfil'],
                        variable=self.tipo_var, value=chave,
                        command=self.atualizar_campos).pack(anchor="w", padx=5, pady=2)

#--------------------------------- Dados do Usuário ------------------------------------#

        self.frame_campos = LabelFrame(self.root, text="Dados do Usuário", padding=10)
        self.frame_campos.pack(fill='x', padx=20, pady=5)

        self.entry_widgets = {
            "Nome completo:": (self.nome_var,),
            "E-mail:": (self.email_var,),
            "Número da OAB:": (self.oab_var,),
            "Estado (UF):": (self.estado_var,),
            "CPF:": (self.cpf_var,),
            "Contato:": (self.contato_var,),
            "Matrícula:": (self.matricula_var,),
            "Tombo:": (self.tombo_var,)
        }

        self.labels_entries = {}
        for texto, (var,) in self.entry_widgets.items():
            lbl = Label(self.frame_campos, text=texto)
        
        #------ Aumenta a largura só do campo "Nome completo" e "E-mail"--------#
            if texto in ["Nome completo:", "E-mail:", "Número da OAB:", "Estado (UF):", "CPF:", "Matrícula:","Contato:"]:
                ent = Entry(self.frame_campos, textvariable=var, width=40)
            else:
                ent = Entry(self.frame_campos, textvariable=var)

            
            self.labels_entries[texto] = (lbl, ent)
        
        #------------------ Assunto ----------------------#

        assunto_frame = LabelFrame(self.root, text="Assunto", padding=10)
        assunto_frame.pack(fill='x', padx=20, pady=10)

        self.assunto_por_titulo = {
            info['titulo']: chave for chave, info in self.assuntos.items()
        }
        titulos_assuntos = list(self.assunto_por_titulo.keys())
        self.assunto_titulo_var.set(titulos_assuntos[0])
        self.menu_assunto = Combobox(assunto_frame, values=titulos_assuntos,
                                    textvariable=self.assunto_titulo_var, state="readonly")
        self.menu_assunto.pack(fill='x', padx=5, pady=5)

        #--------------------- Campo Modo presencial ou teletrabalho ------------------------------#
        self.modo_frame = LabelFrame(self.root, text="Modo", padding=10)
        self.modo_por_titulo = {
            info['tituloModo']: chave for chave, info in self.modos.items()
        }
        titulos_modos = list(self.modo_por_titulo.keys())
        self.modo_titulo_var.set(titulos_modos[0])
        self.menu_modo = Combobox(self.modo_frame, values=titulos_modos,
                                textvariable=self.modo_titulo_var, state="readonly")
        self.menu_modo.pack(fill='x', padx=5, pady=5)
        
        #--------------------- Campo Tipo de máquina------------------------------#
        self.maquina_frame = LabelFrame(self.root, text="Maquina", padding=10)
        self.maquina_por_titulo = {
            info['tituloMaquina']: chave for chave, info in self.maquinas.items()
        }
        titulos_maquinas = list(self.maquina_por_titulo.keys())
        self.maquina_titulo_var.set(titulos_maquinas[0])
        self.menu_maquina = Combobox(self.maquina_frame, values=titulos_maquinas,
                                textvariable=self.maquina_titulo_var, state="readonly")
        self.menu_maquina.pack(fill='x', padx=5, pady=5)

        #-------------------- Frame Tombo (inicialmente escondido) -----------------------------#
        self.tombo_frame = LabelFrame(self.root, text="Tombo", padding=10)
        self.tombo_label = Label(self.tombo_frame, text="Tombo:")
        self.tombo_entry = Entry(self.tombo_frame, textvariable=self.tombo_var)
        self.tombo_label.pack(side="left", padx=5, pady=5)
        self.tombo_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)


        # -------------------- Frame dos botões ----------------#
        self.btn_frame = Frame(self.root)
        self.btn_frame.pack(fill='x', padx=20, pady=(10, 20))

        # Botão confirmar
        self.botao_confirmar = Button(
            self.btn_frame,
            text="Confirmar e Iniciar",
            bootstyle="success",
            width=25,
            command=self.confirmar_dados
        )
        self.botao_confirmar.pack(side="left", padx=5)

        # Botão limpar
        self.botao_limpar = Button(
            self.btn_frame,
            text="Limpar Campos",
            bootstyle="warning",
            width=20,
            command=self.limpar_campos
        )
        self.botao_limpar.pack(side="left", padx=5)

        # Botão cancelar
        self.botao_cancelar = Button(
            self.btn_frame,
            text="Cancelar",
            bootstyle="danger",
            width=20,
            command=self.cancelar_operacao
        )
        self.botao_cancelar.pack(side="left", padx=5)


        
######################### ATUALIZAR ASSUNTOS #############################################

    def atualizar_assuntos(self):
        tipo = self.tipo_var.get()
        assuntos_filtrados = list(self.assunto_por_titulo.keys())


        #------------------------- Filtro e assuntos -------------------------------#
        if tipo == "Q":
            # Mostrar só "Queda de ligação"
            assuntos_filtrados = ["Queda de ligação","Engano de chamada","Ligação muda"]
        elif tipo in ["A", "AE", "E"]:
            # Remove os assuntos que não quer mostrar para Advogados  e publico em geral.
            remover = ["Computador - Não liga", "Zoom - Sem acesso","Queda de ligação", "Audiência - Zoom - Sem acesso","VPN - instalação", "Ramal - Não funciona", "TrtCloud Drive - Sem Acesso","SISCONDJ - Erro de procedimento","VPN - Instalação","Ramal - Não está recebendo chamadas", "Chamado de Audiência","Intranet - Sem acesso", "Impressora - Não Imprime", "Malote Digital - Sem acesso", "Mozilla Firefox - Instalação de Extensão", "Ramal - Redirecionamento de ramal", "TrtCloud Gmail - Sem Acesso Codigo segurança", "Computador - Lentidão", "Windows 11 - atualização", "Autenticador TRT2 - Intranet - Reset", "Certificado Digital - Instalação", "Certificado Digital - Reset/Desbloqueio de Token", "Computador - Solicitação de equipamento", "Corisco ChatJT - Instalação", "Intranet - Reset/Desbloqueio", "Monitor - Não liga", "Monitor - Solicitação de equipamento", "Notebook - Solicitação de equipamento", "Ponto Eletrônico (Serviço) - Erro ao registrar", "TrtCloud Drive - Sem Acesso", "TrtCloud Gmail - Reset/Desbloqueio Senha","Engano de chamada","Chamado de Audiência - Sem acesso a pasta de audiência","Computador - Falha na Migração de Dominio","Computador - Implantação de novo dominio de rede" ]
            assuntos_filtrados = [a for a in assuntos_filtrados if a not in remover]
        elif tipo in ["S","V"]:
            # Remove os assuntos que não quer mostrar para S
            remover = ["Queda de ligação","Engano de chamada"]
            assuntos_filtrados = [a for a in assuntos_filtrados if a not in remover]
        
        self.menu_assunto['values'] = assuntos_filtrados
        if assuntos_filtrados:
            self.assunto_titulo_var.set(assuntos_filtrados[0])
        #-------------------------------------------------------------------------#

######################### ATUALIZAR CAMPOS #############################################
    def atualizar_campos(self):
        tipo = self.tipo_var.get()
    
        # Atualiza combo de assuntos conforme o tipo
        self.atualizar_assuntos()
        
        # Mostrar ou esconder botão e frame de dados conforme tipo
        if tipo == "Q":
            self.frame_campos.pack_forget()
            self.modo_frame.pack_forget()
            self.maquina_frame.pack_forget()
        else:
            self.frame_campos.pack(fill='x', padx=20, pady=10)
        
        # Mostrar ou ocultar os campos "Modo" e "Tombo" conforme o tipo
        if tipo in ["S","V"]:
            self.modo_frame.pack(fill='x', padx=20, pady=10)
            self.maquina_frame.pack(fill='x', padx=20, pady=10)
            self.tombo_frame.pack(fill='x', padx=20, pady=10)
        else:
            self.modo_frame.pack_forget()
            self.maquina_frame.pack_forget()
            self.tombo_frame.pack_forget()
                
        #--------------------------------------------------------
        # Código que mostra/esconde campos específicos:
        for widget in self.frame_campos.winfo_children():
            widget.pack_forget()

        #tipo = self.tipo_var.get()
        # Ordem fixa e personalizada
        campos_em_ordem = [
            "Número da OAB:",
            "Nome completo:",
            "E-mail:",
            "CPF:",
            "Contato:",
            "Estado (UF):",
            "Matrícula:"
        ]

        # Exibe campos conforme o tipo
        tipo = self.tipo_var.get()

        for campo in campos_em_ordem:
            if campo == "Número da OAB:" and tipo in ["A", "AE"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "E-mail:" and tipo in ["A", "E", "AE"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "Nome completo:" and tipo in ["E", "AE"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "Contato:" and tipo in ["A","E", "AE","S","V"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "Estado (UF):" and tipo == "AE":
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "CPF:" and tipo in ["A", "E", "AE"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()
            elif campo == "Matrícula:" and tipo in ["S","V"]:
                self.labels_entries[campo][0].pack()
                self.labels_entries[campo][1].pack()

        
        # Botão fique sempre no final
        self.btn_frame.pack_forget()
        self.btn_frame.pack(fill='x', padx=20, pady=(10, 20))
        
################## Cancelar operação ######################
    def cancelar_operacao(self):
        action2.parar()

######################### CONFIRMAR DADOS #############################################
    def confirmar_dados(self):
        try:
            import action2
            action2.preencher_assyst(
                tipo=self.tipo_var.get(),
                nome=self.nome_var.get(),
                oab=self.oab_var.get(),
                estado=self.estado_var.get(),
                cpf=self.cpf_var.get(),
                email=self.email_var.get(),
                matricula=self.matricula_var.get(),
                tombo=self.tombo_var.get(),
                contato=self.contato_var.get(),
                assunto_titulo=self.assunto_titulo_var.get(),
                modo_titulo=self.modo_titulo_var.get(),
                maquina_titulo=self.maquina_titulo_var.get(),
                tipos=self.tipos,
                assuntos=self.assuntos,
                modos=self.modos,
                maquinas=self.maquinas
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na automação: {e}")

def main():
    root = tk.Tk()
    root.title("Cadastro de Usuário Assyst")
    root.geometry("515x750")

    # Frame principal
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Canvas 
    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    # Barra de rolagem
    #scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    #scrollbar.pack(side="right", fill="y")

    #canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno
    frame_principal = tk.Frame(canvas)

    # Adiciona frame ao canvas
    canvas_window = canvas.create_window(
        (0, 0),
        window=frame_principal,
        anchor="nw"
    )

    # Atualiza região do scroll
    #def atualizar_scroll(event):
    #    canvas.configure(scrollregion=canvas.bbox("all"))

    #frame_principal.bind("<Configure>", atualizar_scroll)

    # Ajusta largura automaticamente
    def resize_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_frame)

    # Scroll com mouse
    #canvas.bind_all(
    #    "<MouseWheel>",
    #    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    #)

    # Inicia aplicação
    app = Aplicacao(frame_principal)

    root.mainloop()


if __name__ == "__main__":
    main()
