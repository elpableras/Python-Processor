'''
Created on 12/11/2013

@author: Pablo
'''

from Tkinter import* #Para crear una ventana
import tkMessageBox
from PIL import* # para imagenes
import Image, ImageTk
ventana = Tk()
ventana.config(bg="white")
ventana.geometry("500x500")

pilaElementosProcesados = []#Crear la pila
pilaElementosProcesados.append(ventana)# Apilar
id_elementosGraficos = {} #Acceder a los elementos graficos por id

'''
Procesar Elemntos Graficos
'''
def procesarElementoGrafico(nodo):
    print "Elemento, " + nodo.nodeName + " Padre: " + str(pilaElementosProcesados[-1])
    elementoGrafico = ""    
    
    if(nodo.nodeName == "lws"):
        elementoGrafico = Frame(pilaElementosProcesados[-1], bg="blue")
    if(nodo.nodeName == "bloque"):
        elementoGrafico = Frame(pilaElementosProcesados[-1], bg="#00FF00")
    if(nodo.nodeName == "texto"):
        var = StringVar()
        elementoGrafico = Label(pilaElementosProcesados[-1], textvariable=var)
        var.set(str(nodo.firstChild.nodeValue))
    if(nodo.nodeName == "encabezado"):
        var = StringVar()
        elementoGrafico = Label(pilaElementosProcesados[-1], textvariable=var, font=("Helvetica", 16))
        var.set(str(nodo.firstChild.nodeValue))
    if(nodo.nodeName == "input"):
        var = StringVar()                
        elementoGrafico = Button(pilaElementosProcesados[-1], textvariable=var, command=lambda:clicked(str(nodo.attributes["mensaje"].value)))
        var.set(str(nodo.firstChild.nodeValue)) 
    if(nodo.nodeName == "imagen"):   
        image = Image.open(str(nodo.attributes["ruta"].value))
        photo = ImageTk.PhotoImage(image)     
        elementoGrafico = Label(pilaElementosProcesados[-1], image=photo)
        elementoGrafico.image = photo                        
    if(nodo.nodeName == "rboton"):
        var = StringVar() 
        elementoGrafico = Radiobutton(pilaElementosProcesados[-1], textvariable=var, variable="v", value=2)
        var.set(str(nodo.firstChild.nodeValue))   
    if(nodo.nodeName == "combo"):
        var = StringVar() 
        puntuacion = ['0', '5', '10'] 
        elementoGrafico = OptionMenu(pilaElementosProcesados[-1], var, *puntuacion)
        var.set(str(nodo.firstChild.nodeValue)) 
    if(nodo.nodeName == "enlace"):# Crear boton enlace
        print "enlace" + str(nodo.attributes["ruta"].value)
        elementoGrafico = Button(pilaElementosProcesados[-1],
                                 text=str(nodo.firstChild.nodeValue),
                                 command = lambda:cargarPagina(str(nodo.attributes["ruta"].value)))
        
    pilaElementosProcesados.append(elementoGrafico)
    
    if(elementoGrafico != ""):
        elementoGrafico.pack()
        
    if("id" in nodo.attributes.keys()):#coleciion con las claves del nodo
        id_elementosGraficos[nodo.attributes["id"].value] = elementoGrafico #introducir primero la clave y luego el valor


'''
cARGAR Elemntos
'''
def cargarElementosLWS(nombre):
    from xml.dom import minidom
    import os
    '''
directorio actual
'''
    directorio = os.getcwd()+"\\"+nombre
    dom = minidom.parse(directorio)
    recorrerArbol(dom.childNodes[0]) # Recorrer el arbol
    
def recorrerArbol(nodo):
    procesarElementoGrafico(nodo)
    #print "Nombre:" + nodo.nodeName + " Valor: " + str(nodo.nodeValue)
    for hijo in nodo.childNodes: # REcorrer demas hijos del arbol
        if(hijo.childNodes.length > 0):# No recorrer hijos vacios
            recorrerArbol(hijo)
    pilaElementosProcesados.pop()#DEsapilar


'''
pROCESAR sENTECIAS ESTILO
'''
def procesarSentenciasEstilo(sentencia):
    tokens = sentencia.split(":")
    idElemento = tokens[0]
    keyPropiedad = tokens[1]
    valorPropiedad = tokens[2].rstrip()# Quitra saltos de linea y espacios
    
    if(idElemento in id_elementosGraficos):        
        elementoActual = id_elementosGraficos[idElemento]
        print "ESTILO" + idElemento + ", propiedad:" + keyPropiedad + " valor:" + valorPropiedad
            
        if(keyPropiedad == "fuente"):
            if(re.match("[a-zA-Z]+", valorPropiedad)):
                elementoActual.config(font=str(valorPropiedad))
                
        if(keyPropiedad == "colorfondo"):
            if(re.match("[a-zA-Z]+", valorPropiedad)):
                elementoActual.config(bg=str(valorPropiedad))
                
        if(keyPropiedad == "color"):
            if(re.match("[a-zA-Z]+", valorPropiedad)):
                elementoActual.config(fg=str(valorPropiedad))                    
        
        if(keyPropiedad == "borde"):
            if(re.match("[0-9]+", valorPropiedad)):
                borde = str(valorPropiedad)
                elementoActual.config(bd=borde)                
        
        if(keyPropiedad == "padding"):            
            if(re.match("[0-9]+,[0-9]+", valorPropiedad)):
                padding = valorPropiedad.split(",")            
                elementoActual.pack(padx=padding[0])            
                elementoActual.pack(pady=padding[1])  
                
        if(keyPropiedad == "justificacion"):                    
            if(re.match("izquierda", valorPropiedad)):
                elementoActual.config(justify=LEFT)
            if(re.match("derecha", valorPropiedad)):
                elementoActual.config(justify=RIGHT)
            if(re.match("centro", valorPropiedad)):
                elementoActual.config(justify=CENTER)                                            
            
        if(keyPropiedad == "dimensiones"):
            if(re.match("[0-9]+,[0-9]+", valorPropiedad)):
                dimensiones = valorPropiedad.split(",")
                elementoActual.config(height=dimensiones[0],width=dimensiones[1])
                elementoActual.pack_propagate(0)
            
        if(keyPropiedad == "alineacion"):
            if(re.match("izquierda", valorPropiedad)):
                elementoActual.pack(side=LEFT)
            if(re.match("derecha", valorPropiedad)):
                elementoActual.pack(side=RIGHT)
            if(re.match("arriba", valorPropiedad)):
                elementoActual.pack(side=TOP)
            if(re.match("abajo", valorPropiedad)):
                elementoActual.pack(side=BOTTOM)            
            

'''
cARGAR Estilo
'''    
def cargarEstilo(nombre):
    import os
    directorio = os.getcwd()+"\\"+nombre
    if(os.path.isfile(directorio)):
        print "TIENE ESTILO"
        fichero = open(directorio)
        lineas = fichero.readlines()
        for linea in lineas:
            procesarSentenciasEstilo(linea)
    else:
        print "NO TIENE ESTILO"  

def clicked(text): 
    tkMessageBox.showinfo('Pablo Gonzalez Jimenez',text) 


'''
cARGAR paGINA
'''
def cargarPagina(nombre):
    for elemento in ventana.slaves():#Recorremos elementos de la ventana
        elemento.pack_forget()#Borrar elemtos de la pagina
    
    id_elementosGraficos.clear()#Vacias tabla Hash
    
    cargarElementosLWS(nombre)
    
    if(nombre == "index2.lws"):
        cargarEstilo(nombre.split(".")[0]+".estilo")#cargar estilo
    if(nombre == "personal.lws"):
        cargarEstilo(nombre.split(".")[0]+".estilo")#cargar estilo
    
cargarPagina("index2.lws")
ventana.mainloop()# mostrar ventana
