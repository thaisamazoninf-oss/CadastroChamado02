from pynput import mouse
import pyautogui
import pyperclip
import time


COORDS = {
    "campo_usuario" : (517,314),
    "adicionar_telefone": (889, 314),
    "clique_secao": (407, 428),
    #"selecionar_usuario_anonimo": (593, 369),
    #"clicar_no_campo_nome": (899, 487),
    #"clique_ok": (970, 532),
    #"Confirme_secao": (364, 452),
    #"selecionar_item": (842, 730)
}


cancelar = False

####### Funções criadas ########
#Função colar Texto. 
def colar_texto(texto):
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl","v")
    time.sleep(0.5)

def parar():
    global cancelar
    cancelar = True
    
def iniciar_automacao(dados_assyst):
    global cancelar
    cancelar = False
    
    for passo in range(50):
        if cancelar:
            print("Automação cacelada pelo usuário")
            return # para tudo sem erro
        
        #pyautogui.click(300,400)
        time.sleep(1)

def preencher_assyst(tipo, nome, oab, estado, cpf, email, matricula, assunto_titulo, modo_titulo, maquina_titulo, tipos, assuntos, modos, maquinas, tombo, contato):
    if tipo == "":
        print("Erro: perfil não selecionado.")
        return

################################################################

    ####### Formatação para adicionar no campo usuário ########
    #if tipo == "S":
    if tipo in ["S","V"]:
        usuario_formatado = matricula.strip()
    elif tipo == "AE":
        usuario_formatado = f"{nome.strip().upper()} OAB {estado.strip().upper()} nº:{oab.strip()} - D"
    elif tipo == "E":
        usuario_formatado = f"{nome.strip().upper()} CPF - {cpf.strip()}"
    elif tipo == "Q":
        usuario_formatado = "USUARIO NAO REGISTRADO(Usuário Não Registrado)"
    elif tipo == "A":
        usuario_formatado = f"OAB:{oab.strip()}"

    ####### Analisar Esse trecho ########
    if tipo == "A":
        try:
            pyautogui.alert("Clique em ok e depois selecione a OAB no site de consultas")
            print("\nSelecione as informações OAB")
            time.sleep(5)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.5)
            infoOAB = pyperclip.paste().strip()
            usuario_formatado = infoOAB
        except:
            usuario_formatado = "Erro ao copiar OAB"
    
    ####### Modos de Entrada ########     
    #Entrada de assuntos
    entrada_assunto = [k for k,v in assuntos.items() if v['titulo'] == assunto_titulo][0]
    assunto = assuntos[entrada_assunto]
    
    #Entrada de modo presencial ou teletrabalho
    entrada_modo = [k for k,v in modos.items() if v['tituloModo'] == modo_titulo][0]
    
    #Entrada de máquina corporativa ou pessoal.
    entrada_maquina = [k for k,v in maquinas.items() if v['tituloMaquina'] == maquina_titulo][0]

    #if tipo != "S":
    if tipo not in ["S","V"]:
        modo_titulo = ""
        maquina_titulo = ""
    conteudo = assunto['conteudo']
    resumo = assunto['resumo']
    categoria = assunto['categoria']
    perfil = tipos[tipo]['perfil']
    

    ######## Número de contato ######## 
    if tipo in ["A", "AE", "S","V", "E"]:
        print("\nNúmero de contato")
        microsip = f"{contato}"
    else:
        microsip = "N/A"
        
    ######## Formatação dos textos para descrição ########   
    # Advogados e externos.
    texto = f"{perfil}{nome.strip().title()},{conteudo}\n" if tipo == "E" else f"{perfil}{conteudo}" 
    
    #texto para usuário não identificado
    text6 = f"{conteudo}"
    
    #texto item
    item = f"{assuntos[entrada_assunto]['item']}"


    if tipo in ["A", "E", "AE"]:
        print("\nClicando no campo usuário")
        pyautogui.rightClick(*COORDS["campo_usuario"])
        time.sleep(3)
        
        pyautogui.press("down")
        print("\nAdicionando informação em 5 segundos")
        pyautogui.press("enter")
        pyperclip.copy(usuario_formatado)
        time.sleep(3)
        pyautogui.hotkey("ctrl", "v")
        print("\nClique em ok")
        pyautogui.press("tab")
        pyautogui.press("enter")
        time.sleep(4)
        pyautogui.press("tab")
        print("\nAdicinando telefone")
        pyperclip.copy(microsip)
        pyautogui.hotkey("ctrl", "v")

    else:
        print("\nClicando no campo usuário")
        time.sleep(3)
        pyautogui.click(*COORDS["campo_usuario"])
        pyperclip.copy(usuario_formatado)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.9)
        pyautogui.press("tab")

    if tipo in ["S","V"]:
        for _ in range(5):
            pyautogui.press("tab")
            time.sleep(0.1)
        print("\nCopiando Edificio")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        edificio = pyperclip.paste().strip()
        time.sleep(0.2)
        pyautogui.press("tab")
        print("\nCopiando Sala")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        sala = pyperclip.paste().strip()

        #----------- Casos de copia de localização para servidor ---------------------------#
        
        #Servidor + Presencial + computador corporativo
        text2 = f"{maquina_titulo}\nTombo: {tombo}\n\n{modo_titulo}\nLocal: {edificio} - {sala}\n\nContato: {microsip}\nRamal: {microsip}."
        
        #Servidor + Presencial + computador pessoal
        text3 = f"{maquina_titulo}\n\n{modo_titulo}\nLocal: {edificio} - {sala}\n\nContato: {microsip}\nRamal: {microsip}."
        
        #Servidor + Teletrabalho + computador pessoal   
        text4 = f"{maquina_titulo}\n\n{modo_titulo}\nLotação: {edificio}.\n\nContato: {microsip}"
        
        #Servidor + Teletrabalho + computador corporativo   
        text5 = f"{maquina_titulo}\nTombo: {tombo}\n\n{modo_titulo}\nLotação: {edificio}.\n\nContato: {microsip}"
        time.sleep(3)
        
        #--------- Adicionando contato no Assyst -----------#
        pyautogui.click(*COORDS["adicionar_telefone"])
        print("\nAdicinando telefone")
        pyperclip.copy(microsip)
        pyautogui.write('/')
        pyautogui.hotkey("ctrl", "v")
        
    #------------------ Adicionando Seção ---------------------#
    if tipo in ["A", "AE", "E"]:
        print("\nClicando no campo seção")
        time.sleep(3)
        pyautogui.click(*COORDS["clique_secao"])
        
        if tipo in ["A","AE"]:
            print("\nAdicionando nome advogado")
            time.sleep(2)
            pyautogui.write('Advogado')
            time.sleep(3)
        elif tipo == "E":
            time.sleep(2)
            pyautogui.write('Juris')
            print("\nAdicionando no Jurisdicionado")
            time.sleep(3)
        
        #pyautogui.click(*COORDS["Confirme_secao"])
        pyautogui.press("down")
        pyautogui.press("enter")

    tabs = 4 if tipo in ["A", "AE", "E"] else 7
    for _ in range(tabs):
        pyautogui.press("tab")
        time.sleep(0.1)
        
#------------------ Adicionando Resumo ---------------------#
    print("\nAdicionando resumo")
    pyperclip.copy(resumo)
    pyautogui.hotkey("ctrl", "v")

    time.sleep(0.2)
    pyautogui.press("tab")


#------------------ Adicionando Descrição ---------------------#

    if entrada_assunto in ["2","5", "6","7","9","10","11","15","16","17","18","19", "21","22","25","27","29","32","36","40","42","46","47","48","51","58","60","61","62","63","65","66","70"]:
        if tipo in ["A", "AE", "E"]:
            print("\nAdicionando descrição")
            colar_texto(texto)
            #pyperclip.copy(texto)
            #pyautogui.hotkey("ctrl", "v")
        
        #Usuário não identificado
        elif tipo == "Q":
            print("adicionando descrição")
            colar_texto(text6)
            #pyperclip.copy(text6)
            #pyautogui.hotkey("ctrl","v")    
            
        #Servidor + Presencial + computador corporativo
        elif tipo in ["S", "V"] and modo_titulo == "Servidor(a) está presencial." and maquina_titulo == "Máquina Corporativa.":
            print("\nAdicionando descrição")
            #pyperclip.copy(texto)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(texto)
            #pyperclip.copy(text2)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(text2)
            
        #Servidor + Presencial + computador pessoal
        elif tipo in ["S","V"] and modo_titulo == "Servidor(a) está presencial." and maquina_titulo == "Máquina Pessoal.":
            print("\nAdicionando descrição")
            #pyperclip.copy(texto)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(texto)
            #pyperclip.copy(text3)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(text3)
        
        #Servidor + Teletrabalho + computador pessoal    
        elif tipo in ["S","V"] and modo_titulo == "Servidor(a) está em teletrabalho." and maquina_titulo == "Máquina Pessoal.":
            print("\nAdicionando descrição")
            #pyperclip.copy(texto)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(texto)
            #pyperclip.copy(text4)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(text4)
            
        #Servidor + Teletrabalho + computador corporativo    
        elif tipo in ["S","V"] and modo_titulo == "Servidor(a) está em teletrabalho." and maquina_titulo == "Máquina Corporativa.":
            print("\nAdicionando descrição")
            #pyperclip.copy(texto)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(texto)
            #pyperclip.copy(text5)
            #pyautogui.hotkey("ctrl", "v")
            colar_texto(text5)
            
    elif entrada_assunto in ["8","60"]:
        print("adicionando descrição")
        #pyperclip.copy(text6)
        #pyautogui.hotkey("ctrl","v")    
        colar_texto(text6)
    else:
        print("\nAdicionando descrição")
        #pyperclip.copy(texto)
        #pyautogui.hotkey("ctrl", "v")
        colar_texto(texto)
    
    #-------------item-------------------# 
    # 2x TAb 
    for _ in range(2):
        pyautogui.press("tab")
        time.sleep(0.2)

    #Colar Item
    print("\nAdicionando item")
    pyperclip.copy(item)
    pyautogui.hotkey("ctrl", "v")
            
    #clica em "opção de item"
    print("\nclica no item")
    time.sleep(2)
    pyautogui.press("down")
    time.sleep(0.3)
    pyautogui.press('enter')
    
#-------------Tombo-------------------# 
    if tipo in ["S","V"]:
        #2x TAb 
        for _ in range(2):
            pyautogui.press("tab")
            time.sleep(0.2)
            
        #Colar Item
        print("\nAdicionando tombo")
        pyperclip.copy(tombo)
        pyautogui.hotkey("ctrl", "v")
                
        #clica em "opção de tombo"
        print("\nclica no tombo")
        time.sleep(2)
        pyautogui.press("down")
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(3)

        pyautogui.press("tab")
    else:
        print("Não precisa de tombo")
        
        
#-------------------Preenchimento Categoria --------------------------#
    
    #if tipo != "S":
    if tipo not in ["S","V"]:
        #2x TAb 
        for _ in range(3):
            pyautogui.press("tab")
            time.sleep(0.2)
    else:
        print(" ")
    
    print("\nAdicionando categoria")
    pyperclip.copy(categoria)
    pyautogui.hotkey("ctrl", "v")
    print("\nclica na categoria")
    time.sleep(2)
    pyautogui.press("down")
    time.sleep(0.3)
    pyautogui.press('enter')
    
    #---------- Preenchimento do e-mail --------------#

    if tipo in ["A", "E", "AE"]:
        print("\nPreenchendo e-mail/OAB/CPF")
        time.sleep(4)
        # 3x TAb 
        for _ in range(9):
            pyautogui.press("tab")
            time.sleep(0.2)
            
        pyperclip.copy(email.strip())
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        #pyautogui.press("tab")
        # 3x TAb 
        for _ in range(3):
            pyautogui.press("tab")
            time.sleep(0.2)
        
        pyautogui.press('enter')
        
        time.sleep(0.3)
        pyautogui.press("tab")
        pyperclip.copy(cpf.strip())
        pyautogui.hotkey("ctrl", "v")

        if tipo == "E":
            #time.sleep(2)
            #pyautogui.moveTo(x=1267, y=598, duration=0.5)
            #pyautogui.scroll(950)
            print("concluido com sucesso!")

    if tipo in ["A", "AE"]:
        time.sleep(0.5)
        pyautogui.press("tab")
        pyperclip.copy(oab.strip())
        pyautogui.hotkey("ctrl", "v")
