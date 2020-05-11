# Programa de algoritmos de búsqueda de Inteligencia Artificial
# Algoritmos: Breadth First Search, Depth First Search, Hill Climbing, Best First Search, A*

from tkinter import *  # Funciones de GUI
from tkinter import filedialog  # Para cargar archivos desde explorador
from tkinter import ttk  # Para poder usar combobox
from tkinter.filedialog import asksaveasfile #Para poder guardar archivos eligiendo ubicación en el explorador
from tkinter import messagebox #Para mostrar mensajes simples al usuario
from collections import * #Para el uso de colas
import time #Para la ejecución paso a paso
from threading import Thread #Para la ejecución paso a paso


thread = Thread()
comeFrom_map = []#Lista que guarda de donde viene cada nodo

realTimeExecFlag = None #Bandera para validar si el usuario quiere o no ejecución a tiempo real

#Los botones para arrancar la búsqueda (con ejecución paso a paso y sin ella) se declaran de manera global
#para que estén disponibles al salir de la función y puedan bloquearse al iniciar cualquier algoritmo
#evitando que se genere un error con el hilo del programa "thread"
b_beginNoRealTime = None
b_beginSearch = None
current_map = []  # Lista de listas de enteros que van guardando los valores del mapa de la siguiente manera
                        # 0 - Vacío
                        # 1 - Obstáculos
                        # 2 - Punto A
                        # 3 - Punto B
chosenAlgorithm = '' #Almacena el algoritmo que se va a ejecutar y se guarda global para poder trabajarlo fuera
                        #de la función en la que se elije y llevarlo a la ventana de ejecución
neighbours = []#Variable que guarda termporalemente los vecinos de una coordenada, es global porque la usan diferentes funciones
everyNeighbour = []#Guarda los vecinos de todas las coordenadas al mismo tiempo
col = 2 #Numer de columnas original del mapa
rows = 2 #Numero de filas original del mapa
btn = None #Será el arreglo de frames de botones que conformal al mapa, es global porque lo usan muchas funciones diferentes

#Coordenadas de los puntos A y B
xA = IntVar
yA = IntVar
xB = IntVar
yB = IntVar
iterations = IntVar

# Estas son las banderas para evitar que se genera mas de un punto A o B
flag_point_A = True
flag_point_B = True

# Inicia la primera capa del programa (ventana principal)---------------------------
def searchProgram():
    global flag_point_A
    global flag_point_B
    # Indicar que no se han elegido puntos A y B por si regresa al menú el usuario una vez elegidos puntos A y B al crear el mapa
    flag_point_A = True
    flag_point_B = True
    # Abrir el mapa precargado-------------------------------------------------------------------------------------------
    def open_map():
        global current_map
        global xA, yA, xB, yB
        closeWelcome()  # Cierra la ventana "PADRE"
        win_displayMap = Tk()
        win_displayMap.title("Current Map")
        win_displayMap.geometry("870x600")
        frames_list = []  # Esta es la lista de frames que guarda los botones

        # Crear los botones para dar la apariencia del mapa leído-------------------
        def createButons_Interface():
            global btn
            global xA, yA, xB, yB
            # Opcion para volver al menú principal----------------------------------
            def backtoMenu():
                win_displayMap.destroy()
                # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
                del current_map[:]
                searchProgram()

            # Define el tamaño de los botones para que encajen en el tamaño de ventana predefinido
            buttons_size = 600 / len(current_map)
            if (len(current_map) < len(current_map[0])):
                buttons_size = 600 / len(current_map[0])

            # Generación del arreglo de botones
            index = 0
            btn = [[0 for a in range(len(current_map))] for b in range(len(current_map[0]))]
            for y in range(len(current_map)):  # Number of rows on the file
                for x in range(len(current_map[0])):  # Number of elements per row
                    # Generación de la lista de frames en la que se mostrará el arreglo de botones
                    # Se guardan en frames para poder definir el tamaño por pixeles en lugar de por caracteres como en un Button
                    frames_list.append(Frame(win_displayMap, width=buttons_size, height=buttons_size))
                    frames_list[index].propagate(False)  # Allows to resize buttons manually
                    frames_list[index].grid(row=y, column=x)  # Defines which variable controls rows and columns

                    # Se ajusta el nuevo botón a uno de los frames creados
                    btn[x][y] = Button(frames_list[index], relief='sunken', state=DISABLED, borderwidth='1',
                                       highlightcolor='black', highlightbackground='black')

                    # Define el color y formato del botón en base a la información
                    # Vacío: Blanco
                    # Obstáculo: Negro
                    # Puntos A & B: Naranja
                    if (current_map[y][x] == 0):
                        btn[x][y].configure(bg='white')
                    elif (current_map[y][x] == 1):
                        btn[x][y].configure(bg='black')
                    elif (current_map[y][x] == 2):
                        xA=x
                        yA=y
                        btn[x][y].configure(bg='orange', text='A', font='Verdana 9',
                                            disabledforeground='black')
                    else:
                        xB=x
                        yB=y
                        btn[x][y].configure(bg='orange', text='B', font='Verdana 9',
                                            disabledforeground='black')

                    # Que cada botón llene el espacio dentro del frame al que se asignó
                    btn[x][y].pack(expand=True, fill=BOTH)

                    x += 1
                    index += 1
                y += 1
            # Abajo del mapa se muestra la notificación de que se contruyó con éxito
            openedMap_title = Label(win_displayMap, text='SUCCESS!', font='Helvetica 22 bold')
            openedMap_title.place(x=660, y=125)
            openedMap_label = Label(win_displayMap, text='The selected file contained', font='Helvetica 13')
            openedMap_label.place(x=635, y=175)
            openedMap_label1 = Label(win_displayMap, text='the displayed map', font='Helvetica 13')
            openedMap_label1.place(x=665, y=195)
            openedMap_label2 = Label(win_displayMap, text='If correct click continue', font='Helvetica 13')
            openedMap_label2.place(x=645, y=215)

            # Junto a la notificación de éxito se encuentran dos botones
            # button_goBack es para regresar al menú principal
            button_goBack = Button(win_displayMap, relief='flat', bg='firebrick2', fg='black',
                                   text='MAIN MENU', font="Helvetica 14 bold", command=backtoMenu)
            button_goBack.place(x=640, y=350, height=70, width=180)
            # button_continue es para direccionarse a elegir el método de búsqueda para ir de A a B
            button_continue = Button(win_displayMap, relief='flat', bg='cyan3', fg='black',
                                     text='CONTINUE', font="Helvetica 14 bold", command = lambda: chooseAlgorithm(win_displayMap))
            button_continue.place(x=640, y=260, height=70, width=180)

            # Bloquea el cambio de tamaño de la ventana por cuestiones de formato
            win_displayMap.resizable(width=False, height=False)

        createButons_Interface()
        win_displayMap.mainloop()

    # Leer desde un txt mapa guardado ----------------------------------------------------------------------------------
    def readfile():
        global current_map
        global flag_point_A
        global flag_point_B
        # Abrir el explorador de archivos
        filename = filedialog.askopenfile(title="Select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        # Es necesario validar que si se haya cargado un archivo (que el usuario no haya cancelado la carga) antes de intentar manipular los datos
        if filename is not None:
            #Se activan las banderas del punto A y B que originalmente están desactivadas para
            # evitar errores en la opción de leer el mapa
            flag_point_B = False
            flag_point_A = False
            # Lee el archivo seleccionado por líneas
            read_map = filename.readlines()  # saves the data from the opened

            # A cada lista que se leyó se le aplica el siguiente procedimiento
            row = 0
            for line in read_map:
                current_map.append([])  # Creamos la "lista de listas" y en cada una de esas listas:
                list_chars = line.split()  # Se separan los caracteres dentro de la lista
                current_map[row].extend(
                    list(map(int, list_chars)))  # Convierte todos los caracteres leídos en la lista a enteros
                # se convierten para facilitar su uso dentro del programa
                row += 1
            if (len(current_map) is len(
                    read_map)):  # cuando todo el mapa leído ha sido convertido y guardado en current_map se manda a mostrar
                open_map()

    # Guardar el mapa que se creo a un archivo de texto
    def savefile():
        global current_map
        global  flag_point_B
        global flag_point_A
        if (flag_point_B and flag_point_A):
            messagebox.showerror('Error', "You can't save a map without points A and B")
        else:
            file = asksaveasfile(mode='w',
                                 defaultextension=".txt")  # Abre el explorador para permitir elegir ubicación para guardar el archivo
                                                                # y lo guarda en un txt
            if (file is not None):
                for row in current_map:
                    for element in row:
                        file.write(str(element) + ' ')  # Guarda valor por valor de una fila separándolo por espacios
                    file.write('\n')  # Cambia de linea
                file.close()  # Deja de escribir en el archivo

    # Salir de todo el programa -----------------------------------------------------------------------------------------
    def exitProgram():
        sys.exit()

    # Cerrar solo la ventana principal ----------------------------------------------------------------------------------
    def closeWelcome():
        win_Welcome.destroy()

    def BFSalgorithm(yA, xA, yB, xB):
        global btn
        global b_beginSearch
        global b_beginNoRealTime
        global current_map
        global everyNeighbour
        global neighbours
        global iterations
        global comeFrom_map
        global realTimeExecFlag

        rows = len(current_map)
        col = len(current_map[0])
        # Se genera una matriz que para guardar los vecinos por coordenada
        comeFrom_map = [0] * int(col)
        for element in range(col):
            comeFrom_map[element] = [0] * int(rows)

        b_beginSearch.configure(state = DISABLED)
        b_beginNoRealTime.configure(state=DISABLED)
        iterNumber = Label(text='0', font='Helvetica 15')
        iterNumber.place(x=740, y=62)
        iterations = 0
        found = False
        vecinos_all()#Primero llama a la función que consigue todos los vecinos
        explored = []#Aqui se van a guardar las coordenadas que ya fueron exploradas
        cola = deque([[yA, xA]])#Se inicializa la cola con las coordenadas del punto A
                                    #La cola va a estar manejando las coordenadas al revés
        while cola and not found:#Mientras haya caminos sin explorar en la cola y no se haya encontrado
            nodo = cola.popleft()#Camino guarda el primer nodo en la cola
            if nodo not in explored:#Si ese nodo no ha sido explorado
                iterations += 1  # Como se explora una nueva casilla aumenta el num de iteración
                iterNumber.configure(text=str(iterations))  # Cambia el label que lleva la cuenta
                #Se extraen las coordenadas del nodo
                y = nodo[0]
                x = nodo[1]
                #Se asigna lo que se guardó previamente en everyNeighbour para este punto a neighbours
                #que son todos los vecinos del nodo
                neighbours = None
                neighbours = everyNeighbour[y][x]
                if (neighbours != 0):  # Valida que no sea un obstáculo
                                    # se valida con neighbours != 0 porque la funcion vecinos_all asigna un 0 al
                                    # espacio en que irían los vecinos de los obstáculos, por lo que si los vecinos
                                    # de nodo resulta 0, nodo es un obstáculo
                    for n in neighbours:#n es cada vecino (representado en coordenadas [x,y])
                        if n not in explored and current_map[n[1]][n[0]] != 1:#Si el vecino no ha sido explorado
                                                                                #y no es un obstáculo
                            comeFrom_map[n[0]][n[1]] = nodo
                            btn[n[0]][n[1]].configure(bg='lightskyblue1')  # marca la casilla nueva a explorar
                            if(realTimeExecFlag):
                                time.sleep(0.05)#Se detiene para poder apreciar la ejecución a tiempo real
                            cola.append(n)#El nodo encontrado se añade a la cola
                            if (n[0] == yB and n[1] == xB):#Si la nueva casilla explorada fue el punto B
                                found = True#Se activa la bandera con True para que el algoritmo detenga la búsqueda
                            if (found):#Si ya se encontro el punto B
                                break#Sale del ciclo for
                explored.append(nodo)#Se agrega el nodo explorado a la lista de los explorados

        if (found):#Terminando el algoritmo se verifica si encontró el punto B
            path_length = 1
            x=n[0]
            y=n[1]
            btn[x][y].configure(bg='brown1')
            while comeFrom_map[x][y] != 0:
                path_length+=1
                node = comeFrom_map[x][y]
                btn[node[0]][node[1]].configure(bg='brown1')
                x=node[0]
                y=node[1]
            lengthLab = Label(text=str(path_length), font='Helvetica 15')
            lengthLab.place(x=740, y=495)
        else:#Si nunca encontró el punto B lanza un mensaje al usuario
            messagebox.showinfo('UNREACHABLE',"There's no available path to reach point B")
            lengthLab = Label(text="NO PATH", font='Helvetica 13 bold')
            lengthLab.place(x=710, y=500)

    def DFSalgorithm(yA, xA, yB, xB):
        global btn
        global b_beginSearch
        global b_beginNoRealTime
        global current_map
        global everyNeighbour
        global neighbours
        global iterations
        global comeFrom_map
        global realTimeExecFlag

        rows = len(current_map)
        col = len(current_map[0])
        # Se genera una matriz que para guardar los vecinos por coordenada
        comeFrom_map = [0] * int(col)
        for element in range(col):
            comeFrom_map[element] = [0] * int(rows)

        b_beginSearch.configure(state=DISABLED)
        b_beginNoRealTime.configure(state=DISABLED)
        iterNumber = Label(text='0', font='Helvetica 15')
        iterNumber.place(x=740, y=62)
        iterations = 0
        found = False
        vecinos_all()#Primero llama a la función que consigue todos los vecinos
        explored = []#Aqui se van a guardar las coordenadas que ya fueron exploradas
        stack = [[yA, xA]]#Se inicializa la pila con las coordenadas del punto A
                                    #La pila va a estar manejando las coordenadas al revés
        while stack and not found:#Mientras haya caminos sin explorar en la pila y no se haya encontrado
            nodo = stack.pop()#Camino guarda el nodo extraído de la pila
            if nodo not in explored:#Si ese nodo no ha sido explorado
                iterations += 1  # Como se explora una nueva casilla aumenta el num de iteración
                iterNumber.configure(text=str(iterations))  # Cambia el label que lleva la cuenta
                #Se extraen las coordenadas del nodo
                y = nodo[0]
                x = nodo[1]
                #Se asigna lo que se guardó previamente en everyNeighbour para este punto a neighbours
                #que son todos los vecinos del nodo
                neighbours = None
                neighbours = everyNeighbour[y][x]
                if (neighbours != 0):  # Valida que no sea un obstáculo
                                    # se valida con neighbours != 0 porque la funcion vecinos_all asigna un 0 al
                                    # espacio en que irían los vecinos de los obstáculos, por lo que si los vecinos
                                    # de nodo resulta 0, nodo es un obstáculo
                    for n in neighbours:#n es cada vecino (representado en coordenadas [x,y])
                        if n not in explored and current_map[n[1]][n[0]] != 1:#Si el vecino no ha sido explorado
                                                                                #y no es un obstáculo
                            comeFrom_map[n[0]][n[1]] = nodo
                            btn[n[0]][n[1]].configure(bg='lightskyblue1')  # marca la casilla nueva a explorar
                            if(realTimeExecFlag):
                                time.sleep(0.05)#Se detiene para poder apreciar la ejecución a tiempo real
                            stack.append(n)#El nodo encontrado se añade a la pila
                            if (n[0] == yB and n[1] == xB):#Si la nueva casilla explorada fue el punto B
                                found = True#Se activa la bandera con True para que el algoritmo detenga la búsqueda
                            if (found):#Si ya se encontro el punto B
                                break#Sale del ciclo for
                explored.append(nodo)#Se agrega el nodo explorado a la lista de los explorados

        if (found):#Terminando el algoritmo se verifica si encontró el punto B
            path_length = 1
            x=n[0]
            y=n[1]
            btn[x][y].configure(bg='brown1')
            while comeFrom_map[x][y] != 0:
                path_length+=1
                node = comeFrom_map[x][y]
                btn[node[0]][node[1]].configure(bg='brown1')
                x=node[0]
                y=node[1]
            lengthLab = Label(text=str(path_length), font='Helvetica 15')
            lengthLab.place(x=740, y=495)
        else:#Si nunca encontró el punto B lanza un mensaje al usuario
            messagebox.showinfo('UNREACHABLE',"There's no available path to reach point B")
            lengthLab = Label(text="NO PATH", font='Helvetica 13 bold')
            lengthLab.place(x=710, y=500)

    def HillClimbingAlgorithm(xA, yA, xB, yB):
        global everyNeighbour
        global b_beginNoRealTime
        global b_beginSearch
        global btn
        global current_map
        global comeFrom_map
        global realTimeExecFlag

        b_beginSearch.configure(state=DISABLED)
        b_beginNoRealTime.configure(state=DISABLED)

        iterNumber = Label(text='0', font='Helvetica 15')
        iterNumber.place(x=740, y=62)

        rows = len(current_map)
        col = len(current_map[0])
        # Se genera una matriz que para guardar los vecinos por coordenada
        comeFrom_map = [0] * int(col)
        for element in range(col):
            comeFrom_map[element] = [0] * int(rows)

        vecinos_all()
        initial_state = [xA, yA]
        goal_state = [xB, yB]
        comeFrom_map[initial_state[0]][initial_state[1]] = 0
        current_state = list(initial_state)
        old_current_state = None
        iterations = 0
        while (current_state != goal_state and old_current_state != current_state):
            old_current_state = current_state
            iterations += 1  # Como se explora una nueva casilla aumenta el num de iteración
            iterNumber.configure(text=str(iterations))  # Cambia el label que lleva la cuenta
            btn[current_state[0]][current_state[1]].configure(bg='lightskyblue1')
            if(realTimeExecFlag):
                time.sleep(0.05)
            successors = everyNeighbour[current_state[0]][current_state[1]]
            current_score = scoring_function(current_state)
            if (successors != 0):  # Valida que no sea un obstáculo
                for successor in successors:  # n es cada vecino (representado en coordenadas [x,y])
                    if current_map[successor[1]][successor[0]] != 1:  # Si el sucesor no es un obstáculo
                        successor_score = scoring_function(successor)
                        if (successor_score < current_score):
                            comeFrom_map[successor[0]][successor[1]] = current_state
                            current_state = successor
                            break
        if(current_state!=goal_state):#Si nunca encontró el punto B lanza un mensaje al usuario
            messagebox.showinfo('UNREACHABLE',"There's no available path to reach point B")
            lengthLab = Label(text="NO PATH", font='Helvetica 13 bold')
            lengthLab.place(x=710, y=500)
        else:
            btn[current_state[0]][current_state[1]].configure(bg='brown1')
            x=current_state[0]
            y=current_state[1]
            path_length=1
            while comeFrom_map[x][y]:
                path_length+=1
                node = comeFrom_map[x][y]
                btn[node[0]][node[1]].configure(bg='brown1')
                x=node[0]
                y=node[1]

    def BestFS (xA, yA, xB, yB):
        global everyNeighbour
        global btn
        global current_map
        global b_beginNoRealTime
        global b_beginSearch
        global comeFrom_map
        global realTimeExecFlag

        rows = len(current_map)
        col = len(current_map[0])
        # Se genera una matriz que para guardar los vecinos por coordenada
        comeFrom_map = [0] * int(col)
        for element in range(col):
            comeFrom_map[element] = [0] * int(rows)

        b_beginSearch.configure(state=DISABLED)
        b_beginNoRealTime.configure(state=DISABLED)
        iterNumber = Label(text='0', font='Helvetica 15')
        iterNumber.place(x=740, y=62)
        iterations = 0
        found = False
        vecinos_all()
        initial_state = [xA, yA]
        scores = []
        explored = []
        agenda = [[xA, yA]]
        scores.append(scoring_function(initial_state))
        while agenda and not found:
            best = agenda.pop(scores.index(min(scores)))  # Dentro del paréntesis de pop se indica el índice en el que
                                                            # se encuentra el "best node" que es la menor distancia
                                                        # guardada en scores, en ese índice se saca el camino de agenda
            scores.pop(scores.index(min(scores)))  # Se saca el score correspondiente para que sigan
                                                         # siendo equitativas ambas listas
            if best not in explored:#Verifica que no haya sido explorado el nodo
                # Se pinta cada nodo que va explorando
                btn[best[0]][best[1]].configure(bg='lightskyblue1')
                iterations+=1
                iterNumber.configure(text=str(iterations))
                if(realTimeExecFlag):
                    time.sleep(0.05)

                if best[0] == xB and best[1] == yB:  # Si ese último nodo es el punto B
                    found = True  # Indica que se encontró
                else:  # Si el nodo no es el punto B
                    successors = everyNeighbour[best[0]][best[1]]  # Successors guarda todos los vecinos del último nodo
                    for successor in successors:  # Por cada vecino encontrado:
                        if (successor != comeFrom_map[successor[0]][successor[1]]#Si el mejor vecino no es del que viene
                                                      and current_map[successor[1]][successor[0]] != 1#Y no es un obstáculo
                                                        and successor not in explored):  #Y no ha sido explorado
                            comeFrom_map[successor[0]][successor[1]] = best #Guardamos de dónde viene el nodo
                            scores.append(scoring_function(successor))  # Se agrega el score del nuevo nodo a "scores"
                            # Y en la misma posición se guardará el camino al que se agrega dicho vecino a la agenda:
                            agenda.append(successor)
                explored.append(best)#Va guardando los explorados para que no se repita la búsqueda
        if found:#Si sí encontró el punto B
            #Toma las coordenadas de succesor que ahorita se encuentran en el punto B
            x = best[0]
            y = best[1]
            btn[x][y].configure(bg='brown1')
            path_length = 1
            #Y va pintando hacia atrás
            while comeFrom_map[x][y] != 0:
                path_length+=1
                node = comeFrom_map[x][y]#¿De dónde viene?
                btn[node[0]][node[1]].configure(bg='brown1')
                x = node[0]
                y = node[1]
            lengthLab = Label(text=str(path_length), font='Helvetica 15')
            lengthLab.place(x=740, y=495)
        else:
            messagebox.showinfo('UNREACHABLE', "There's no available path to reach point B")
            lengthLab = Label(text="NO PATH", font='Helvetica 13 bold')
            lengthLab.place(x=710, y=500)

    def Aestrella (xA, yA, xB, yB):
        global everyNeighbour
        global btn
        global current_map
        global comeFrom_map
        global b_beginNoRealTime
        global b_beginSearch
        global realTimeExecFlag

        b_beginSearch.configure(state=DISABLED)
        b_beginNoRealTime.configure(state=DISABLED)

        rows = len(current_map)
        col = len(current_map[0])

        cost_map = []
        cost_map = [0] * int(col)
        for element in range(col):
            cost_map[element] = [0] * int(rows)
        def cost_function (prev_node, current_node):
            cost_map[current_node[0]][current_node[1]] = cost_map[prev_node[0]][prev_node[1]] + 1
            return cost_map[current_node[0]][current_node[1]]

        # Se genera una matriz que para guardar los vecinos por coordenada
        comeFrom_map = [0] * int(col)
        for element in range(col):
            comeFrom_map[element] = [0] * int(rows)

        b_beginSearch.configure(state=DISABLED)
        iterNumber = Label(text='0', font='Helvetica 15')
        iterNumber.place(x=740, y=62)
        iterations = 0
        found = False
        vecinos_all()
        initial_state = [xA, yA]
        scores = []
        explored = []
        agenda = [[xA, yA]]
        scores.append(scoring_function(initial_state))
        while agenda and not found:
            best = agenda.pop(scores.index(min(scores)))  # Dentro del paréntesis de pop se indica el índice en el que
                                                            # se encuentra el "best node" que es la menor distancia
                                                        # guardada en scores, en ese índice se saca el camino de agenda
            scores.pop(scores.index(min(scores)))  # Se saca el score correspondiente para que sigan
                                                         # siendo equitativas ambas listas
            if best not in explored:#Verifica que no haya sido explorado el nodo
                # Se pinta cada nodo que va explorando
                btn[best[0]][best[1]].configure(bg='lightskyblue1')
                iterations+=1
                iterNumber.configure(text=str(iterations))
                if (realTimeExecFlag):
                    time.sleep(0.05)

                if best[0] == xB and best[1] == yB:  # Si ese último nodo es el punto B
                    found = True  # Indica que se encontró
                else:  # Si el nodo no es el punto B
                    successors = everyNeighbour[best[0]][best[1]]  # Successors guarda todos los vecinos del último nodo
                    for successor in successors:  # Por cada vecino encontrado:
                        if (successor != comeFrom_map[successor[0]][successor[1]]#Si el mejor vecino no es del que viene
                                                      and current_map[successor[1]][successor[0]] != 1#Y no es un obstáculo
                                                        and successor not in explored):  #Y no ha sido explorado
                            comeFrom_map[successor[0]][successor[1]] = best #Guardamos de dónde viene el nodo
                            scores.append(scoring_function(successor)+cost_function(best,successor))  # Se agrega el score del nuevo nodo a "scores"
                            # Y en la misma posición se guardará el camino al que se agrega dicho vecino a la agenda:
                            agenda.append(successor)
                explored.append(best)#Va guardando los explorados para que no se repita la búsqueda
        if found:#Si sí encontró el punto B
            #Toma las coordenadas de succesor que ahorita se encuentran en el punto B
            x = best[0]
            y = best[1]
            btn[x][y].configure(bg='brown1')
            path_length = 1
            #Y va pintando hacia atrás
            while comeFrom_map[x][y] != 0:
                path_length+=1
                node = comeFrom_map[x][y]#¿De dónde viene?
                btn[node[0]][node[1]].configure(bg='brown1')
                x = node[0]
                y = node[1]
            lengthLab = Label(text=str(path_length), font='Helvetica 15')
            lengthLab.place(x=740, y=495)
        else:
            messagebox.showinfo('UNREACHABLE', "There's no available path to reach point B")
            lengthLab = Label(text="NO PATH", font='Helvetica 13 bold')
            lengthLab.place(x=710, y=500)

    def scoring_function(node):
        global xB, yB
        global current_map
        score = abs(yB-node[1]) + abs(xB-node[0])
        return score


    def detenccion_vecinos(x, y, rows, col):
        global neighbours
        global current_map
        if(neighbours!=0):
            del neighbours[:]
        neighbours = []
        # Identifica los "vecinos" del cuadro considerando los casos en los que el cuadro e encuentra en bordes o esquinas
        if (x == 0 and y == 0):
            neighbours = [0] * 2
            neighbours[0] = [x + 1, y]
            neighbours[1] = [x, y + 1]
        elif (x == 0 and y == rows - 1):
            neighbours = [0] * 2
            neighbours[0] = [x, y - 1]
            neighbours[1] = [x + 1, y]
        elif (x == col - 1 and y == 0):
            neighbours = [0] * 2
            neighbours[0] = [x - 1, y]
            neighbours[1] = [x, y + 1]
        elif (x == col - 1 and y == rows - 1):
            neighbours = [0] * 2
            neighbours[0] = [x - 1, y]
            neighbours[1] = [x, y - 1]
        elif (x == 0 and y != 0):
            neighbours = [0] * 3
            neighbours[0] = [x + 1, y]
            neighbours[1] = [x, y - 1]
            neighbours[2] = [x, y + 1]
        elif (x != 0 and y == 0):
            neighbours = [0] * 3
            neighbours[0] = [x, y + 1]
            neighbours[1] = [x - 1, y]
            neighbours[2] = [x + 1, y]
        elif (x == col - 1 and y != rows - 1):
            neighbours = [0] * 3
            neighbours[0] = [x, y - 1]
            neighbours[1] = [x - 1, y]
            neighbours[2] = [x, y + 1]
        elif (x != col - 1 and y == rows - 1):
            neighbours = [0] * 3
            neighbours[0] = [x - 1, y]
            neighbours[1] = [x, y - 1]
            neighbours[2] = [x + 1, y]
        else:
            neighbours = [0] * 4
            neighbours[0] = [x - 1, y]
            neighbours[1] = [x + 1, y]
            neighbours[2] = [x, y - 1]
            neighbours[3] = [x, y + 1]

    # Esta funcion buscara los vecinos de todos los botones usando deteccion_vecinos para ir uno por uno
    def vecinos_all():
        global neighbours
        global everyNeighbour
        global current_map
        rows = len(current_map)
        col = len(current_map[0])
        # Se genera una matriz que para guardar los vecinos por coordenada
        everyNeighbour = [0] * int(col)
        for element in range(col):
            everyNeighbour[element] = [0] * int(rows)

        # Se manda a llamar la función deteccion_vecinos para cada elemento del mapa que no sea un obstáculo o el punto B
        for y in range(rows):
            for x in range(col):
                if (current_map[y][x] != 1 and current_map[y][x] != 3):
                    detenccion_vecinos(x, y, rows, col)
                    everyNeighbour[x][y] = list(neighbours)

    def searchAlgorithms(win_search):
        global chosenAlgorithm
        global btn
        global current_map
        global neighbours
        global xA, yA, xB, yB
        global everyNeighbour
        global thread
        rows = len(current_map)
        col = len (current_map[0])
        algorLabel = Label(win_search)
        lenLab = Label(text="Path's length: ", font="Helvetica 12").place(x=610, y=500)
        lengthLab = Label(text="0", font='Helvetica 15')
        lengthLab.place(x=740, y=495)
        if (chosenAlgorithm == 'Breadth First Search'):
            algorLabel.configure(text = '"Breadth First\nSearch" algorithm...', font= 'Helvetica 12 bold')
            algorLabel.place(x=620, y=10)
            #Fijamos al algoritmo Breadth First Search como el objetivo del hilo que permite ejecucion a tiempo real
            thread = Thread(target=lambda: BFSalgorithm(xA, yA, xB, yB))
        elif (chosenAlgorithm == "Depth First Search"):
            algorLabel.configure(text='"Depth First\nSearch" algorithm...', font='Helvetica 12 bold')
            algorLabel.place(x=625, y=10)
            thread = Thread(target=lambda: DFSalgorithm(xA, yA, xB, yB))
        elif(chosenAlgorithm == "Hill Climbing"):
            algorLabel.configure(text = '"Hill Climbing"\nalgorithm...', font= 'Helvetica 12 bold')
            algorLabel.place(x=615, y=10)
            thread = Thread(target=lambda: HillClimbingAlgorithm(xA, yA, xB, yB))
        elif(chosenAlgorithm == "Best First Search"):
            algorLabel.configure(text = '"Best First\nSearch" algorithm...', font= 'Helvetica 12 bold')
            algorLabel.place(x=625, y=10)
            thread = Thread(target=lambda: BestFS(xA, yA, xB, yB))
        else:
            algorLabel.configure(text = '"A*"\nalgorithm...', font= 'Helvetica 12 bold')
            algorLabel.place(x=655, y=10)
            thread = Thread(target=lambda: Aestrella(xA, yA, xB, yB))

    def searchWindow (prevWin, chosenAlg):
        global chosenAlgorithm
        global current_map
        global btn
        global thread
        global b_beginSearch
        global b_beginNoRealTime
        global realTimeExecFlag
        chosenAlgorithm = chosenAlg
        prevWin.destroy()
        win_search = Tk()
        win_search.title("Seach Window")
        win_search.geometry('800x600')
        win_search.resizable(width=False, height=False)
        searchAlgorithms(win_search)

        def backtoMenu():#Vuelta al menú principal
            win_search.destroy()
            # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
            del current_map[:]
            searchProgram()

        def changeAlgorithm():#Cambiar el algoritmo de búsqueda para el mismo mapa
            chooseAlgorithm(win_search)

        def showMap():
            global current_map
            global btn
            frames_list = []#Aquí se van guardando los botones.

            # Define el tamaño de los botones para que encajen en el tamaño de ventana predefinido
            buttons_size = 600 / len(current_map)
            if (len(current_map) < len(current_map[0])):
                buttons_size = 600 / len(current_map[0])

            # Generación del arreglo de botones
            index = 0
            btn = [[0 for a in range(len(current_map))] for b in range(len(current_map[0]))]
            #Para generar todos los botones que se necesitan:
            for y in range(len(current_map)):  # Number of rows on the file
                for x in range(len(current_map[0])):  # Number of elements per row
                    # Generación de la lista de frames en la que se mostrará el arreglo de botones
                    # Se guardan en frames para poder definir el tamaño por pixeles en lugar de por caracteres como en un Button
                    frames_list.append(Frame(win_search, width=buttons_size, height=buttons_size))
                    frames_list[index].propagate(False)  # Allows to resize buttons manually
                    frames_list[index].grid(row=y, column=x)  # Defines which variable controls rows and columns

                    # Se ajusta el nuevo botón a uno de los frames creados
                    btn[x][y] = Button(frames_list[index], relief='sunken', state=DISABLED, borderwidth='1',
                                       highlightcolor='black', highlightbackground='black')

                    # Define el color y formato del botón en base a la información
                    # Vacío: Blanco
                    # Obstáculo: Negro
                    # Puntos A & B: Naranja
                    if (current_map[y][x] == 0):
                        btn[x][y].configure(bg='white')
                    elif (current_map[y][x] == 1):
                        btn[x][y].configure(bg='black')
                    elif (current_map[y][x] == 2):
                        btn[x][y].configure(bg='orange', text='A', font='Verdana 9',
                                            disabledforeground='black')
                    else:
                        btn[x][y].configure(bg='orange', text='B', font='Verdana 9',
                                            disabledforeground='black')

                    # Que cada botón llene el espacio dentro del frame al que se asignó
                    btn[x][y].pack(expand=True, fill=BOTH)

                    x += 1
                    index += 1
                y += 1

        def startRealTime():#Acción del botón b_beginSearch, activa la bandera de ejeución a tiempo real
            global realTimeExecFlag
            realTimeExecFlag = True
            thread.start()

        def startNoRealTime ():#Acción del boton b_beginNoRealTime, desactiva la bandera de ejecución a tiempo real
            global realTimeExecFlag
            realTimeExecFlag = False
            thread.start()


        showMap()
        lbl1 = Label(text="Explored nodes: ", font='Helvetica 11')
        lbl1.place(x=615,y=65)

        b_beginSearch = Button(win_search, text='BEGIN REAL\nTIME SEARCH', font='Helvetica 13 bold', relief='flat',
                               bg='cadetblue3', fg='black', command=startRealTime)
        b_beginSearch.place(x=615, y=100, height=65, width=170)

        b_beginNoRealTime = Button(win_search, text='BEGIN\nSEARCH', font='Helvetica 13 bold', relief='flat',
                               bg='cadetblue3', fg='black', command=startNoRealTime)
        b_beginNoRealTime.place(x=615, y=180, height=65, width=170)

        b_changeAlg = Button(win_search, text = 'CHANGE\nALGORITHM', font = 'Helvetica 13 bold', relief = 'flat',
                               bg = 'cadetblue3', fg='black', command = changeAlgorithm)
        b_changeAlg.place(x=615, y= 260, height = 65, width = 170)
        b_mainMenu = Button(win_search, text = 'MAIN\nMENU', font = 'Helvetica 13 bold', relief = 'flat',
                               bg = 'cadetblue3', fg='black', command = backtoMenu)
        b_mainMenu.place(x=615, y= 340, height = 65, width = 170)
        b_exitProgram = Button(win_search, text='EXIT\nPROGRAM', font='Helvetica 13 bold', relief='flat',
                            bg='cadetblue3', fg='black', command = exitProgram)
        b_exitProgram.place(x=615, y= 420, height = 65, width = 170)
        win_search.mainloop()

    def chooseAlgorithm (previousWind):
        global current_map
        global chosenAlgorithm
        global flag_point_A
        global flag_point_B
        chosenAlgorithm = ''
        if(flag_point_A or flag_point_B):
            messagebox.showerror('Error', "You can't proceed without marking point A and B")
        else:
            previousWind.destroy()
            win_searchChoices = Tk()
            win_searchChoices.title("Search Algorithms' Options")
            win_searchChoices.geometry('410x180')
            lbl1 = Label(text = 'Search Algorithms', font = 'Helvetica 20 bold').place(x=80, y=15)
            lbl2 = Label(text ='Pick the algorithm you want to use', font = 'Helvetica 12').place(x=90, y=55)
            lbl3 = Label(text = 'to find a way between A and B', font = 'Helvetica 12').place(x=100, y=80)
            algOptions = ttk.Combobox(win_searchChoices, values=['Breadth First Search', 'Depth First Search',
                                                                 'Hill Climbing', 'Best First Search', 'A*'],
                                       font='Helvetica 11', width=17, state='readonly')
            algOptions.place(x=30, y=130)
            algOptions.current(0)

            searchButton = Button(bg = 'brown1', relief = 'flat', text ='SEARCH', font = 'Helvetica 16 bold',
                                  command = lambda: searchWindow(win_searchChoices, algOptions.get()))
            searchButton.place(x=220, y=120, width=150, height=45)

    # Crear el mapa -----------------------------------------------------------------------------------------------------
    def createMap():
        global xA,yA,xB,yB
        closeWelcome()

        # Ventana el la que el usuario puede crear el mapa:
        def defineMapElements():
            global current_map
            global btn
            # Maracar las celdas si es osbtáculo, punto A o punto B
            def markcells(x, y):
                # En esta funcion se van a utilizar las variables globales para evitar mas puntos A-B
                global btn
                global flag_point_A
                global flag_point_B
                global xA, yA, xB, yB
                # Current map es la matriz donde se guarda el mapa de forma numerica
                global current_map

                # La funcion .get() nos da el valor del COMBOBOX
                valorObtenido = markOptions.get()

                # En esta parte es una seleccion de que color se va a poner el boton
                if valorObtenido == 'Obstacle':
                    btn[x][y].configure(bg='black', state=DISABLED)
                    current_map[y][x] = 1
                elif valorObtenido == 'Point A' and flag_point_A == True:
                    btn[x][y].configure(text='A', font='Verdana 9', bg='orange', state=DISABLED,
                                        disabledforeground='black')
                    # Aqui se pone falsa la variable para que no haya mas puntos A y se guarda en matriz
                    flag_point_A = False
                    current_map[y][x] = 2
                    xA=x
                    yA=y
                elif valorObtenido == 'Point B' and flag_point_B == True:
                    btn[x][y].configure(text='B', font='Verdana 9', bg='orange', state=DISABLED,
                                        disabledforeground='black')
                    # Aqui se pone falsa la variable para que no haya mas puntos B y se guarda en matriz
                    flag_point_B = False
                    current_map[y][x] = 3
                    xB=x
                    yB=y

            # Permite al usuario volver al menú principal.
            def backToMainMenu():
                # Aqui volvemos a mandar a llamar estas variables para dejarlas en true
                # y en caso de que se vuelva a crear mapa vuelvan a usarse
                global flag_point_A
                global flag_point_B
                flag_point_A = True
                flag_point_B = True
                win_createMap.destroy()
                # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
                del current_map[:]
                searchProgram()

            def clearAll(rows, col):
                global btn
                global current_map
                global flag_point_A
                global flag_point_B
                flag_point_A = True
                flag_point_B = True
                del current_map[:]
                current_map = [0] * int(rows)
                for element in range(rows):
                    current_map[element] = [0] * int(col)
                for y in range(rows):
                    for x in range(col):
                        btn[x][y].configure(text='', bg='white',state=NORMAL)

            # Recuperamos los valores ingresados por el usuario en el spinbox
            rows = int(spin_rows.get())
            col = int(spin_col.get())

            # Destruimos la ventana vieja para seguir trabajando con la nueva ventana "Create Map"
            win_askMeasurements.destroy()
            win_createMap = Tk()
            win_createMap.title("Create Map")
            win_createMap.geometry("870x600")
            frames_list = []

            # Define el tamaño de los botones para que encajen en el tamaño de ventana predefinido
            buttons_size = 600 / rows
            if (rows < col):
                buttons_size = 600 / col

            # Generación del arreglo de botones
            index = 0
            flag_point_A = True
            flag_point_B = True
            btn = [[0 for a in range(rows)] for b in range(col)]
            for y in range(rows):  # Número de filas
                for x in range(col):  # Número de columnas
                    # Generación de la lista de frames en la que se mostrará el arreglo de botones
                    # Se guardan en frames para poder definir el tamaño por pixeles en lugar de por caracteres como en un Button
                    frames_list.append(Frame(win_createMap, width=buttons_size, height=buttons_size))
                    frames_list[index].propagate(False)  # Allows to resize buttons manually
                    frames_list[index].grid(row=y, column=x)  # Defines which variable controls rows and columns

                    # Se ajusta el nuevo botón a uno de los frames creados
                    btn[x][y] = Button(frames_list[index], relief='sunken', borderwidth='1',
                                       highlightcolor='black', highlightbackground='black', bg='white',
                                       command=lambda x1=x, y1=y: markcells(x1, y1))

                    # Da el tamaño a current_map, quien va guardando el valor numérico de cada botón
                    # para tener mismo número de filas y columnas que hay de botones
                    current_map = [0] * rows
                    for element in range(rows):
                        current_map[element] = [0] * col

                    # Que cada botón llene el espacio dentro del frame al que se asignó
                    btn[x][y].pack(expand=True, fill=BOTH)
                    x += 1
                    index += 1
                y += 1

            # Instrucciones, botones  y combobox --------------------------------------------------------------------
            inst1 = Label(text='BUILD IT!', font='Helvetica 24 bold').place(x=660, y=20)
            inst2 = Label(text='You must choose the kind', font='Helvetica 13').place(x=630, y=75)
            inst3 = Label(text='of object you want to', font='Helvetica 13').place(x=650, y=95)
            inst4 = Label(text='add to the map and then', font='Helvetica 13').place(x=635, y=115)
            inst5 = Label(text='just click on it.', font='Helvetica 13').place(x=680, y=135)
            inst6 = Label(text="If you made a mistake", font='Helvetica 13 italic').place(x=647, y=160)
            inst7 = Label(text="you can restart the map", font='Helvetica 13 italic').place(x=641, y=181)
            inst8 = Label(text='by clicking "CLEAR ALL"', font='Helvetica 13 italic').place(x=638, y=203)
            # El combobox da las opciones para marcar el mapa
            markOptions = ttk.Combobox(win_createMap, values=['Obstacle', 'Point A', 'Point B'],
                                       font='Helvetica 14', width=17, state='readonly')
            markOptions.place(x=634, y=250)
            markOptions.current(0)

            # Para guardar el mapa creado en un txt
            # Este botón debe estar bloqueado hasta que se hayan puesto el punto A y B
            savemap_b = Button(text='SAVE MAP', font='Helvetica 13 bold', bg='darkgoldenrod2', height=2, width=20,
                               relief='flat', command = savefile).place(x=634, y=316)
            # Botón para limpiar el mapa, limpia "current_map" y devuelve los botones al formato original
            restart_b = Button(text='CLEAR ALL', font='Helvetica 13 bold', bg='darkslategray2', height=2,
                               relief='flat', width=20, command=lambda r1=rows, c1=col: clearAll(r1, c1)).place(x=634, y=376)
            # Para continuar a la selección de algoritmos

            continue_b = Button(text='CONTINUE', font='Helvetica 13 bold', bg='greenyellow', height=2, width=20,
                                relief='flat', command = lambda : chooseAlgorithm(win_createMap)).place(x=634, y=436)

            # Para permitir al usuario volver al menú principal
            return_b = Button(text='MAIN MENU', font='Helvetica 13 bold', bg='indianred1', height=2, width=20,
                              relief='flat', command=backToMainMenu).place(x=634, y=496)

            # define_obstacles()
            # Bloquea el cambio de tamaño de la ventana por cuestiones de formato
            win_createMap.resizable(width=False, height=False)
            win_createMap.mainloop()

        def backtoMenu():
            win_askMeasurements.destroy()
            # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
            del current_map[:]
            searchProgram()

        # Primero se necesita una ventana para solicitar las dimensiones del mapa a crear
        win_askMeasurements = Tk()
        win_askMeasurements.title("Map measurements")
        win_askMeasurements.geometry('500x200')

        spin_rows = Spinbox(win_askMeasurements, from_=2, to=30, width=4, relief='flat', buttondownrelief='flat',
                            buttonuprelief='flat',
                            state='readonly', justify=CENTER, font='Helvetica 12', buttonbackground='lightskyblue1')
        spin_col = Spinbox(win_askMeasurements, from_=2, to=30, width=4, relief='flat', buttondownrelief='flat',
                           buttonuprelief='flat',
                           state='readonly', justify=CENTER, font='Helvetica 12', buttonbackground='lightskyblue1')

        spin_rows.place(x=150, y=101)
        spin_col.place(x=400, y=101)

        Label(win_askMeasurements, text='In order to create the map you must', font='Helvetica 14 bold').place(x=80,
                                                                                                               y=15)
        Label(win_askMeasurements, text='provide the desired measurements.', font='Helvetica 14 bold').place(x=83, y=40)
        Label(win_askMeasurements, text='*Please make sure you use values between 2 and 30*',
              font='Helvetica 12').place(x=65, y=68)
        Label(win_askMeasurements, text="Enter Rows: ", font='Helvetica 12').place(x=50, y=100)
        Label(win_askMeasurements, text="Enter Columns:", font='Helvetica 12').place(x=270, y=100)

        continue_b = Button(win_askMeasurements, text="CONTINUE", width=15, height=2, font='Helvetica 12 bold',
                            relief='flat', bg='orange', command=defineMapElements)
        continue_b.place(x=270, y=135)

        goback_b = Button(win_askMeasurements, text="BACK TO MENU", width=15, height=2, font='Helvetica 12 bold',
                          relief='flat', bg='orange', command=backtoMenu).place(x=90, y=135)

        win_askMeasurements.mainloop()  # al final del programa (mantiene la ventana )

    # Interfaz principal del programa -----------------------------------------------------------------------------------
    win_Welcome = Tk()
    win_Welcome.title("Search Algorithms")
    image1 = PhotoImage(file="main_pict.gif")

    # Ajustar el tamaño de la ventana al tamaño de la imagen que tiene el diseño de la interfaz principal
    w = image1.width()
    h = image1.height()
    win_Welcome.geometry("%dx%d+0+0" % (w, h))

    # Ahora se hace un Label en el que se muestre la imagen y se configura para llenar la ventana
    back_Image = Label(win_Welcome, image=image1)
    back_Image.pack(side='top', fill='both', expand='yes')

    # Genera los tres botones: Crear mapa, Cargar mapa y Salir del programa
    b_Create = Button(back_Image, text='CREATE MAP', relief='flat', font='Verdana 20 bold', bg="chartreuse3",
                      fg='black', activebackground='darkgreen', activeforeground='black', command=createMap)
    b_Create.place(x=585, y=160, width=442, height=118)
    b_Load = Button(back_Image, text='LOAD MAP', relief='flat', font='Verdana 20 bold', bg='darkorange', fg='black',
                    activebackground='darkorange4', activeforeground='black', command=readfile)
    b_Load.place(x=585, y=288, width=280, height=118)
    b_Exit = Button(back_Image, text='EXIT', relief='flat', font='Verdana 20 bold', bg='deepskyblue1', fg='black',
                    activebackground='dodgerblue4', activeforeground='black', command=exitProgram)
    b_Exit.place(x=875, y=288, width=150, height=118)

    # Almacena la imagen
    back_Image.image = image1

    # No permite redimiensionar la ventana por cuestiones de formato
    win_Welcome.resizable(width=False, height=False)

    win_Welcome.mainloop()


# Para que el programa inicie
searchProgram()
