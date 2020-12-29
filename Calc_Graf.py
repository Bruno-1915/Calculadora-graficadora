#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wx
import wx.lib.scrolledpanel
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import os.path
from os import path


class Inicio(wx.Frame):

    def __init__(self):
        w, h = wx.GetDisplaySize()
        super().__init__(parent=None, title='Inicio', size = (int(w/3), int(h/3)))
        panel = wx.Panel(self)

        ## LA VENTANA DE INICIO NO TIENE MENU

        box = wx.BoxSizer(wx.VERTICAL)

        string = wx.StaticText(panel, label = "Bienvenido a mi calculadora y graficadora")
        boton_calc = wx.Button(panel, label='Calculadora')
        boton_graf = wx.Button(panel, label = "Graficadora")
        #AÑADIMOS EL EVENTO AL PRECIONARSE
        boton_calc.Bind(wx.EVT_BUTTON, self.on_press_calc)
        boton_graf.Bind(wx.EVT_BUTTON, self.on_press_graf)

        box.AddStretchSpacer(prop=1)
        box.Add(string, 0, wx.ALL | wx.CENTER, 5)
        box.Add(boton_calc, 0, wx.ALL | wx.CENTER , 5)
        box.Add(boton_graf, 0, wx.ALL | wx.CENTER, 5)
        box.AddStretchSpacer(prop=1)

        string2 = wx.StaticText(panel, label = "Por Bruno Martinez")
        boton_salir = wx.Button(panel, label = "Salir")
        boton_salir.Bind(wx.EVT_BUTTON, self.on_press_salir)

        box.Add(string2, 0, wx.ALL | wx.CENTER)
        box.Add(boton_salir, 0, wx.ALL | wx.CENTER, 5)
        box.AddStretchSpacer(prop=1)

        panel.SetSizer(box)
        self.Centre()
        self.Show(True)

    def on_press_calc(self, event):
        run_calc()
        self.Close()

    def on_press_graf(self, event):
        run_graf()
        self.Close()

    def on_press_salir(self, event):
        self.Close()

    def salir(self, event):
        self.Close()

## INICIO DE LA CLASE Graficadora
class Graficadora(wx.Frame):

    def __init__(self):
        w, h = wx.GetDisplaySize()
        #self.operadores_unarios = ['sqrt', 'exp', 'log', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh']
        self.operadores_unarios, self.operadores_binarios, self.operadores_problematicos = leer_funciones()
        self.rango_x = (-1, 1)
        super().__init__(parent=None, title='Graficadora', size = (int(w/2), int(3*h/4)))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        ## INICIO DEL Menu

        self.menubar = wx.MenuBar()

        self.Menu = wx.Menu()

        self.inicio = wx.MenuItem(self.Menu ,wx.ID_ANY, text = "Inicio",kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_press_inicio, self.inicio)

        self.funciones = wx.Menu()
        ## Boton para ver las funciones existentes
        self.ver_funciones_boton = wx.MenuItem(self.funciones, wx.ID_ANY,
                                                text = "Ver Funciones", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.ver_func, self.ver_funciones_boton)
        self.funciones.Append(self.ver_funciones_boton)

        # Menu para agregar funcion unaria
        self.agregar_funcion = wx.Menu()
        self.nueva_funcion_boton = wx.MenuItem(self.agregar_funcion, wx.ID_ANY, text = "Unaria", kind = wx.ITEM_NORMAL)
        self.agregar_funcion.Append(self.nueva_funcion_boton)
        self.Bind(wx.EVT_MENU, self.nueva_func, self.nueva_funcion_boton)
        self.funciones.Append(wx.ID_ANY, 'Agregar Funcion', self.agregar_funcion)

        # Menu para eliminar funcion unaria
        self.eliminar_funcion = wx.Menu()
        self.quitar_funcion_boton = wx.MenuItem(self.eliminar_funcion, wx.ID_ANY, text = "Unaria", kind = wx.ITEM_NORMAL)
        self.eliminar_funcion.Append(self.quitar_funcion_boton)
        self.Bind(wx.EVT_MENU, self.quitar_func, self.quitar_funcion_boton)
        self.funciones.Append(wx.ID_ANY, 'Eliminar Funcion', self.eliminar_funcion)

        # Boton para reestablecer las funciones
        self.res_funciones = wx.MenuItem(self.funciones, wx.ID_ANY, text = "Reestablecer Funciones", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.reestablecer, self.res_funciones)
        self.funciones.Append(self.res_funciones)

        #self.funciones = wx.MenuItem(self.Menu, wx.ID_ANY, text = "Funciones", kind = wx.ITEM_NORMAL)
        self.menu_salir = wx.MenuItem(self.Menu, wx.ID_ANY, text = "Salir", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.salir, self.menu_salir)

        self.Menu.Append(self.inicio)
        #self.Menu.Append(wx.ID_ANY, 'Nueva Función', self.nueva_funcion)
        self.Menu.Append(wx.ID_ANY, 'Funciones', self.funciones)
        self.Menu.Append(self.menu_salir)

        self.menubar.Append(self.Menu, 'Menu')

        self.Modo = wx.Menu()

        self.calc = wx.MenuItem(self.Modo, wx.ID_ANY, text = "Calculadora", kind = wx.ITEM_NORMAL)
        self.graf = wx.MenuItem(self.Modo, wx.ID_ANY, text = "Graficadora", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_press_calc, self.calc)

        self.Modo.Append(self.calc)
        self.Modo.Append(self.graf)

        self.menubar.Append(self.Modo, "Modo")

        ## FIN DEL MENU

        ## WIDGETS PARA LA ENTRADA
        box1_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.entrada = wx.TextCtrl(panel, size = (int(w/6), 10*4))
        string1 = wx.StaticText(panel, label = "Entrada: ")
        box1_1.Add(string1, 0, wx.LEFT | wx.CENTER, 5)
        box1_1.Add(self.entrada, 0, wx.ALL | wx.EXPAND, 5)

        ## BOX CON LOS ELEMENTOS PARA GRAFICAR
        box1 = wx.BoxSizer(wx.VERTICAL)
        string1_1 = wx.StaticText(panel, label = "Las funciones deben tener el siguiente formato 'y = X' \t")
        string1_2 = wx.StaticText(panel, label = "Se explicito en las multiplicaciones, en vez de usar\n 3X usa 3*X")
        boton_graficar = wx.Button(panel, label = "Graficar")
        boton_graficar.Bind(wx.EVT_BUTTON, self.grafica)
        boton_graficar.SetDefault()
        box1.Add(box1_1)
        box1.Add(string1_1)
        box1.Add(string1_2)
        box1.Add(boton_graficar, wx.ALL)

        ## BOX AUXILIAR PARA LAS ENTRADAS DE LOS RANGOS
        box2_1 = wx.BoxSizer(wx.HORIZONTAL)
        ## WIDGETS PARA EL RANGO EN X
        self.entrada_rango_x = wx.TextCtrl(panel, size = (int(w/22), 10*4))
        string2 = wx.StaticText(panel, label = "Rango en x: ")
        box2_1.Add(string2, 0, wx.LEFT | wx.CENTER, 5)
        box2_1.Add(self.entrada_rango_x, 0, wx.ALL | wx.EXPAND, 5)
        ## WIDGETS PARA EL RANGO EN Y
        self.entrada_rango_y = wx.TextCtrl(panel, size = (int(w/22), 10*4))
        string3 = wx.StaticText(panel, label = "Rango en y: ")
        box2_1.Add(string3, 0, wx.LEFT | wx.CENTER, 5)
        box2_1.Add(self. entrada_rango_y, 0, wx.ALL | wx.EXPAND, 5)

        box2 = wx.BoxSizer(wx.VERTICAL)
        ## BOX PARA LOS BOTONES DE LOS RANGOS
        box2_2 = wx.BoxSizer(wx.HORIZONTAL)
        boton_rango_x = wx.Button(panel, label = "Ingresar rango en x")
        boton_rango_x.Bind(wx.EVT_BUTTON, self.set_rango_x)
        boton_rango_y = wx.Button(panel, label = "Ingresar rango en y")
        boton_rango_y.Bind(wx.EVT_BUTTON, self.set_rango_y)
        box2_2.Add(boton_rango_x, 0, wx.ALL | wx.LEFT)
        box2_2.Add(wx.StaticText(panel, label = "\t"))
        box2_2.Add(boton_rango_y, 0, wx.ALL | wx.RIGHT)

        string2_1 = wx.StaticText(panel, label = "El rango debe ser una tupla\nPor default el rango en x es: (-1,1)\nNota: El rango en y es solo para efectos de\nvisualización")

        ## BOX CON TODOS LOS ELEMENTOS DE LOS RANGOS
        box2.Add(box2_1)
        box2.Add(box2_2)
        box2.Add(string2_1)

        ## BOX CON LOS BOX PARA GRAFICAR Y FIJAR EL RANGO, SE UNEN EN UN RENGLON
        box_entradas = wx.BoxSizer(wx.HORIZONTAL)
        box_entradas.Add(box1, wx.LEFT | wx.ALL)
        box_entradas.Add(box2, wx.RIGHT)

        box.Add(box_entradas)

        ## PARTE DE LA GRÁFICA
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlim(self.rango_x)
        self.axes.grid()
        self.figure.set_figwidth(9)
        self.canvas = FigureCanvas(panel, -1, self.figure)
        box_grafica = wx.BoxSizer(wx.VERTICAL)

        navToolbar = NavigationToolbar2Wx(self.canvas)
        ## AÑADIMOS EL TOOLBAR
        box_grafica.Add(navToolbar)
        ## AÑADIMOS A LA VENTANA EL CANVAS DE LA GRAFICA
        box_grafica.Add(self.canvas, 1, wx.CENTER | wx.TOP)

        ## BOX PARA EL BOTON DE BORRAR
        box.Add(box_grafica, wx.CENTER)
        box_borrar = wx.BoxSizer()
        boton_borrar = wx.Button(panel, label = "Borrar")
        boton_borrar.Bind(wx.EVT_BUTTON, self.borrar)
        box_borrar.Add(boton_borrar, wx.LEFT | wx.ALL)

        box.Add(box_borrar)

        ## AÑADIMOS UN ESPACIO PARA QUE EL BOTON DE SALIR QUEDE HASTA EL FINAL
        box.AddStretchSpacer(prop=1)

        ## BOTON PARA SALIR
        salir = wx.Button(panel, label = "Salir")
        salir.Bind(wx.EVT_BUTTON, self.salir)
        box.Add(salir, 0, wx.BOTTOM | wx.RIGHT | wx.ALL, 5)

        panel.SetSizer(box)
        self.Centre()
        self.SetMenuBar(self.menubar)
        self.Show(True)

    def reestablecer(self, event):
        self.Close()
        reiniciar_funciones()
        run_graf()

    def nueva_func(self, event):
        callPopup_input('agregar')

    def quitar_func(self, event):
        callPopup_input('eliminar')

    def ver_func(self, event):
        callFunciones("Graf")

    def borrar(self, event):
        self.axes.clear()
        self.axes.set_xlim(self.rango_x)
        self.axes.grid()
        self.canvas.draw()

    def grafica(self, event):
        x = self.entrada.GetValue()
        label = x
        if x == '' or x == " ":
            return None

        else:
            x = x[x.find('=')+1:]
            X = [i for i in np.linspace(self.rango_x[0], self.rango_x[1], 5000)]
            Y = [x.replace('X', str(i)) for i in X]
            try:
                Y = [self.evaluar(i) for i in Y]
                self.axes.plot(X,Y, label = label)
                self.axes.legend()
                self.canvas.draw()
            except:
                callPopup("No pude entender tu entrada")


    def set_rango_x(self, event):
        x = self.entrada_rango_x.GetValue()
        x = x.split(',')
        x[0] = float(x[0].replace('(',''))
        x[1] = float(x[1].replace(' ','').replace(')',''))
        self.axes.set_xlim((x[0], x[1]))
        self.rango_x = (x[0], x[1])
        self.canvas.draw()

    def set_rango_y(self, event):
        y = self.entrada_rango_y.GetValue()
        y = y.split(',')
        y[0] = float(y[0].replace('(',''))
        y[1] = float(y[1].replace(' ','').replace(')',''))
        self.axes.set_ylim((y[0], y[1]))
        self.canvas.draw()

    def evaluar(self, x):
        if x == '':
            None
        else:
            ## Si hay la raiz de un número negativo quitamos el signo, obtenemos la
            ## raiz del numero positivo y agregamos la unidad imaginaria
            a = []
            if 'sqrt(-' in x:
                x = x.replace('sqrt(-', '1j*sqrt(')

            ## Algunas funciones comparten caracteres, para evitar errores esas funciones
            ## se convierten en mayúsculas
            for i in self.operadores_problematicos:
                if i in x:
                    a.append((i, i.upper()))
                    x = x.replace(i, i.upper())

            for i in self.operadores_unarios:
                if i in x:
                    x = x.replace(i, "np." + i)
            x = x.replace('^', "**")

            ## Regresamos a minusculas las funciones problematicas
            for i in a:
                x = x.replace(i[1], 'np.' + i[0])

            if self.tipo(eval(x)) == str:
                return None
            else:
                temp = eval(x)
                if temp == 0:
                    return 0
                else:
                    return temp

    def salir(self, event):
        self.Close()

    def tipo(self, x, bandera = False) -> type:
        try:
            int(x)
            return int
        except:
            try:
                float(x)
                return float
            except:
                try:
                    complex(x)
                    if bandera:
                        return complex(x)
                    else:
                        return complex
                except:
                    try:
                        X = x.split('+')
                        x = X[1] + '+' + X[0]
                        complex(x)
                        if bandera:
                            return complex(x)
                        else:
                            return complex
                    except:
                        try:
                            X = x.split('-')
                            x = X[1] + '-' + X[0]
                            complex(x)
                            if bandera:
                                return complex(x)
                            else:
                                return complex
                        except:
                            return str

    def on_press_calc(self, event):
        run_calc()
        self.Close()

    def on_press_inicio(self, event):
        run_inicio()
        self.Close()


## FIN DE LA CLASE Graficadora

## INICIO DE LA CLASE CALCULADORA
class Calculadora(wx.Frame):

    def __init__(self):
        #self.operadores_unarios = ['sqrt', 'exp', 'log', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh']
        #self.operadores_binarios = ['^','*', '/', '+', '-']
        self.operadores_unarios, self.operadores_binarios, self.operadores_problematicos = leer_funciones()
        self.numeros = [['7','8','9'], ['4','5','6'], ['1','2','3'], ['.','0','j']]

        w, h = wx.GetDisplaySize()
        super().__init__(parent=None, title='Calculadora', size = (int(w/3), int(h/3)))
        panel = wx.Panel(self)

        ## INICIO DEL Menu

        self.menubar = wx.MenuBar()

        self.Menu = wx.Menu()

        self.inicio = wx.MenuItem(self.Menu ,wx.ID_ANY, text = "Inicio",kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_press_inicio, self.inicio)

        self.funciones = wx.Menu()
        ## Boton para ver las funciones existentes
        self.ver_funciones_boton = wx.MenuItem(self.funciones, wx.ID_ANY,
                                                text = "Ver funciones", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.ver_func, self.ver_funciones_boton)
        self.funciones.Append(self.ver_funciones_boton)

        # Menu para agregar funcion unaria
        self.agregar_funcion = wx.Menu()
        self.nueva_funcion_boton = wx.MenuItem(self.agregar_funcion, wx.ID_ANY, text = "Unaria", kind = wx.ITEM_NORMAL)
        self.agregar_funcion.Append(self.nueva_funcion_boton)
        self.Bind(wx.EVT_MENU, self.nueva_func, self.nueva_funcion_boton)
        self.funciones.Append(wx.ID_ANY, 'Agregar Funcion', self.agregar_funcion)

        # Menu para eliminar funcion unaria
        self.eliminar_funcion = wx.Menu()
        self.quitar_funcion_boton = wx.MenuItem(self.eliminar_funcion, wx.ID_ANY, text = "Unaria", kind = wx.ITEM_NORMAL)
        self.eliminar_funcion.Append(self.quitar_funcion_boton)
        self.Bind(wx.EVT_MENU, self.quitar_func, self.quitar_funcion_boton)
        self.funciones.Append(wx.ID_ANY, 'Eliminar Funcion', self.eliminar_funcion)

        # Boton para reestablecer las funciones
        self.res_funciones = wx.MenuItem(self.funciones, wx.ID_ANY, text = "Reestablecer Funciones", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.reestablecer, self.res_funciones)
        self.funciones.Append(self.res_funciones)

        #self.funciones = wx.MenuItem(self.Menu, wx.ID_ANY, text = "Funciones", kind = wx.ITEM_NORMAL)
        self.menu_salir = wx.MenuItem(self.Menu, wx.ID_ANY, text = "Salir", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.salir, self.menu_salir)

        self.Menu.Append(self.inicio)
        #self.Menu.Append(wx.ID_ANY, 'Nueva Función', self.nueva_funcion)
        self.Menu.Append(wx.ID_ANY, 'Funciones', self.funciones)
        self.Menu.Append(self.menu_salir)

        self.menubar.Append(self.Menu, 'Menu')

        self.Modo = wx.Menu()

        self.calc = wx.MenuItem(self.Modo, wx.ID_ANY, text = "Calculadora", kind = wx.ITEM_NORMAL)
        self.graf = wx.MenuItem(self.Modo, wx.ID_ANY, text = "Graficadora", kind = wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.on_press_graf, self.graf)

        self.Modo.Append(self.calc)
        self.Modo.Append(self.graf)

        self.menubar.Append(self.Modo, "Modo")

        ## FIN DEL MENU

        box = wx.BoxSizer(wx.VERTICAL)
        self.entrada = wx.TextCtrl(panel)

        box.Add(self.entrada, 0, wx.ALL | wx.EXPAND, 5)

        operadores_lista = self.operadoresBotones()

        ## BOX PARA LOS OPERADORES
        box1 = wx.BoxSizer(wx.VERTICAL)
        for i in operadores_lista:
            temp_box = wx.BoxSizer()
            for j in i:
                boton = wx.Button(panel, label = j)
                boton.Bind(wx.EVT_BUTTON, self.actualizar)
                temp_box.Add(boton, 0, wx.ALL | wx.ALIGN_CENTER, 0)
            box1.Add(temp_box, 0, wx.LEFT, 5)
        ## BOX PARENTHESIS
        boxParenthesis = wx.BoxSizer(wx.HORIZONTAL)
        boton_leftParenthesis = wx.Button(panel, label = '(')
        boton_leftParenthesis.Bind(wx.EVT_BUTTON, self.actualizar)
        boton_rightParenthesis = wx.Button(panel, label = ')')
        boton_rightParenthesis.Bind(wx.EVT_BUTTON, self.actualizar)

        ## BOX PARA LOS NUMEROS
        box2 = wx.BoxSizer(wx.VERTICAL)
        for i in self.numeros:
            temp_box = wx.BoxSizer()
            for j in i:
                boton = wx.Button(panel, label = j)
                boton.Bind(wx.EVT_BUTTON, self.actualizar)
                temp_box.Add(boton, 0, wx.ALL | wx.ALIGN_CENTER, 0)
            box2.Add(temp_box, 0, wx.CENTER, 5)

        ## BOX PARA LOS ULTIMOS BOTONES
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        boton_igual = wx.Button(panel, label = '=')
        boton_igual.Bind(wx.EVT_BUTTON, self.evaluar_calc)
        boton_igual.SetDefault()
        boton_AC = wx.Button(panel, label = "AC")
        boton_AC.Bind(wx.EVT_BUTTON, self.limpiar)
        boton_DEL = wx.Button(panel, label = "DEL")
        boton_DEL.Bind(wx.EVT_BUTTON, self.eliminar)

        box_main = wx.BoxSizer(wx.HORIZONTAL)
        box_main.Add(box1)
        box_main.Add(box2)
        #box_main.Add(box3)
        box_main2 = wx.BoxSizer(wx.HORIZONTAL)
        box_main2.Add(boton_leftParenthesis, wx.ALL, 5)
        box_main2.Add(boton_rightParenthesis, wx.ALL, 5)
        box_main2.Add(boton_igual, wx.ALL, 5)
        box_main2.Add(boton_AC, wx.ALL, 5)
        box_main2.Add(boton_DEL, wx.ALL, 5)

        box.Add(box_main, wx.ALL | wx.EXPAND, wx.CENTER)
        box.Add(box_main2, wx.ALL | wx.EXPAND, wx.CENTER)
        box.AddStretchSpacer(prop=1)

        salir = wx.Button(panel, label = "Salir")
        salir.Bind(wx.EVT_BUTTON, self.salir)
        box.Add(salir, 0, wx.BOTTOM | wx.RIGHT | wx.ALL, 5)

        panel.SetSizer(box)
        self.Centre()
        self.SetMenuBar(self.menubar)
        self.Show(True)

    def reestablecer(self, event):
        self.Close()
        reiniciar_funciones()
        run_calc()

    def nueva_func(self, event):
        callPopup_input('agregar')

    def quitar_func(self, event):
        callPopup_input('eliminar')

    def ver_func(self, event):
        callFunciones("Calc")

    def limpiar(self, event):
        self.entrada.SetValue("")

    def eliminar(self, event):
        actual = self.entrada.GetValue()
        self.entrada.SetValue(actual[:-1])

    def evaluar_calc(self, event):
        x = self.entrada.GetValue()
        if x == '':
            None
        else:
            ## Si hay la raiz de un número negativo quitamos el signo, obtenemos la
            ## raiz del numero positivo y agregamos la unidad imaginaria
            a = []
            if 'sqrt(-' in x:
                x = x.replace('sqrt(-', '1j*sqrt(')

            ## Algunas funciones comparten caracteres, para evitar errores esas funciones
            ## se convierten en mayúsculas
            for i in self.operadores_problematicos:
                if i in x:
                    a.append((i, i.upper()))
                    x = x.replace(i, i.upper())

            for i in self.operadores_unarios:
                if i in x:
                    x = x.replace(i, "np." + i)
            x = x.replace('^', "**")

            ## Regresamos a minusculas las funciones problematicas
            for i in a:
                x = x.replace(i[1], 'np.' + i[0])

            if self.tipo(eval(x)) == str:
                self.entrada.SetValue("Error")
            else:
                temp = eval(x)
                if temp == 0:
                    self.entrada.SetValue("0")
                else:
                    self.entrada.SetValue(str(temp))


    def operadoresBotones(self):
        operadores = self.operadores_binarios + self.operadores_unarios
        l = 0
        lista_completa = []
        a = []
        while l < len(operadores):
            a.append(operadores[l])
            if (l+1)%4 == 0:
                lista_completa.append(a)
                a = []
            l += 1
        lista_completa.append(a)
        return lista_completa

    def actualizar(self, event):
        None
        boton = event.GetEventObject()
        label = boton.GetLabel()
        actual = self.entrada.GetValue()
        self.entrada.SetValue(actual + '' + label)

    def salir(self, event):
        self.Close()

    def tipo(self, x, bandera = False) -> type:
        try:
            int(x)
            return int
        except:
            try:
                float(x)
                return float
            except:
                try:
                    complex(x)
                    if bandera:
                        return complex(x)
                    else:
                        return complex
                except:
                    try:
                        X = x.split('+')
                        x = X[1] + '+' + X[0]
                        complex(x)
                        if bandera:
                            return complex(x)
                        else:
                            return complex
                    except:
                        try:
                            X = x.split('-')
                            x = X[1] + '-' + X[0]
                            complex(x)
                            if bandera:
                                return complex(x)
                            else:
                                return complex
                        except:
                            return str

    def on_press_graf(self, event):
        run_graf()
        self.Close()

    def on_press_inicio(self, event):
        run_inicio()
        self.Close()

## FIN DE LA CLASE CALCULADORA

## INICIO DE LA CLASE POPUP
class Popup(wx.Frame):
    def __init__(self, mensaje):
        super().__init__(parent=None, title='Mensaje', size = (400, 200))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        string1 = wx.StaticText(panel, label = mensaje)
        boton = wx.Button(panel, label = "OK")
        boton.Bind(wx.EVT_BUTTON, self.cerrar)
        boton.SetDefault()

        box.AddStretchSpacer(prop=1)
        box.Add(string1, 0, wx.ALL | wx.CENTER, 5)
        box.Add(boton, 0, wx.ALL | wx.CENTER, 5)
        box.AddStretchSpacer(prop=1)

        panel.SetSizer(box)
        self.Centre()
        self.Show(True)

    def cerrar(self, event):
        self.Close()

## FIN DE LA CLASE POPUP

## INICIO DE LA CLASE POPUP CON ENTRADA
class Popup_input(wx.Frame):
    def __init__(self, accion):
        self.accion = accion
        super().__init__(parent=None, title='Mensaje', size = (300, 200))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        string1 = wx.StaticText(panel, label = 'Ingresa la función')
        self.entrada = wx.TextCtrl(panel)
        box_botones = wx.BoxSizer(wx.HORIZONTAL)
        boton = wx.Button(panel, label = "Listo")
        boton.Bind(wx.EVT_BUTTON, self.Listo)
        boton.SetDefault()
        boton_cancel = wx.Button(panel, label = "Cancelar")
        boton_cancel.Bind(wx.EVT_BUTTON, self.Cancelar)
        box_botones.Add(boton, 0, wx.ALL, 5)
        box_botones.Add(boton_cancel, 0, wx.ALL, 5)

        box.AddStretchSpacer(prop=1)
        box.Add(string1, 0, wx.ALL | wx.CENTER, 5)
        box.Add(self.entrada, 0, wx.ALL | wx.EXPAND, 5)
        box.Add(box_botones, 0, wx.ALL | wx.CENTER, 5)
        box.AddStretchSpacer(prop=1)

        panel.SetSizer(box)
        self.Centre()
        self.Show(True)

    def Listo(self, event):
        actual = self.entrada.GetValue()
        if self.accion == 'agregar':
            agregar_unaria(actual)
        elif self.accion == "eliminar":
            eliminar_unaria(actual)
        self.Close()

    def Cancelar(self, event):
        self.Close()

## FIN DE LA CLASE POPUP CON ENTRADA

## CLASE PARA VER LAS FUNCIONES COMO lISTA

class PopupFunciones(wx.Frame):
    def __init__(self, ventana):
        super().__init__(parent=None, title='Mensaje', size = (300, 400))
        self.ventana = ventana
        panel = wx.Panel(self)
        self.unarias, self.binarias, self.prob = leer_funciones()

        box = wx.BoxSizer(wx.HORIZONTAL)

        self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE)

        lista = wx.ListBox(panel, size = (100, 300), choices = ["Binarias", 'Unarias'], style = wx.LB_SINGLE)

        box.Add(lista, 0, wx.EXPAND)
        box.Add(self.text, 1, wx.EXPAND)

        boton = wx.Button(panel, label = "OK")
        boton.Bind(wx.EVT_BUTTON, self.OK)
        boton.SetDefault()

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(box, 0, wx.ALL | wx.EXPAND, 5)
        main_box.AddStretchSpacer(prop=1)
        main_box.Add(boton, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(main_box)
        panel.Fit()

        self.Centre()
        self.Bind(wx.EVT_LISTBOX, self.desplegar, lista)
        self.Show(True)

    def desplegar(self, event):
        val = event.GetEventObject().GetStringSelection()

        if val == "Binarias":
            self.text.SetValue("")
            for i in self.binarias:
                self.text.AppendText(i + '\n')
        elif val == "Unarias":
            self.text.SetValue("")
            for i in self.unarias:
                self.text.AppendText(i + '\n')

    def OK(self, event):
        self.Close()


## FIN DE LA CLASE PARA VER FUNCIONES

## FUNCION PARA VER LAS FUNCIONES
def callFunciones(ventana):
    frame = PopupFunciones(ventana)

## FUNCION PARA LLAMAR UN POPUP
def callPopup(mensaje):
    frame = Popup(mensaje)

## FUNCION PARA LLAMAR A UN POPUP CON ENTRADA
def callPopup_input(accion):
    frame = Popup_input(accion)

## FUNCION PARA LEER DE UN ARCHIVO LAS FUNCIONES EXISTENTES
def leer_funciones():
    nombre = "funciones.txt"

    if path.exists(nombre):
        f = open(nombre, 'r')
        archivo = f.read()
        f.close()

        linea1 = archivo.split('\n')[0]
        linea2 = archivo.split('\n')[1]
        linea3 = archivo.split('\n')[2]

        unarios = linea1.split('= ')[1].replace(' ','').replace('[','').replace(']','').replace("'",'').split(',')
        binarios = linea2.split('= ')[1].replace(' ','').replace('[','').replace(']','').replace("'",'').split(',')
        problematicos = linea3.split('= ')[1].replace(' ','').replace('[','').replace(']','').replace("'",'').split(',')

    else:
        unarios = ['sqrt', 'exp', 'log', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh']
        binarios = ['^', '*', '/', '+', '-']
        problematicos = ['cosh', 'sinh', 'tanh']

    return unarios, binarios, problematicos

## FUNCION PARA GUARDAR EN UN ARCHIVO LAS FUNCIONES EXISTENTES
def guardar_funciones(unarias, binarias, problematicos):
    nombre = "funciones.txt"

    f = open(nombre, 'w')
    f.write("Unarias = " + str(unarias) + '\n')
    f.write("Binarias = " + str(binarias) + '\n')
    f.write("Problematicos = " + str(problematicos) + '\n')
    f.close()

def agregar_unaria(operador):
    unarios, binarios, problematicos = leer_funciones()
    if operador.isspace() or operador == '':
        callPopup('Ingresa una función valida.')
    elif operador in unarios:
        callPopup("El operador ya se encuentra en mi lista.\nRevisa la lista de funciones en el menu.")
    else:
        unarios.append(operador)
        ## Si el operador nuevo comparte caracteres con alguna función ya existente también
        ## se agrega a la lista de operadores problematicos
        for i in unarios:
            if i in operador:
                problematicos.append(operador)
                break
        guardar_funciones(unarios, binarios, problematicos)

def eliminar_unaria(operador):
    unarios, binarios, problematicos = leer_funciones()
    if operador in unarios:
        unarios.remove(operador)

        if operador in problematicos:
            problematicos.remove(operador)

        guardar_funciones(unarios, binarios, problematicos)

    else:
        callPopup("La función que quieres eliminar no está entre mis funciones")

def reiniciar_funciones():
    unarios = ['sqrt', 'exp', 'log', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh']
    binarios = ['^', '*', '/', '+', '-']
    problematicos = ['cosh', 'sinh', 'tanh']
    guardar_funciones(unarios, binarios, problematicos)

## FUNCION PARA ABRIR LA VENTANA DE INICIO
def run_inicio():
    #app = wx.App()
    frame = Inicio()
    #app.MainLoop()

## FUNCION PARA ABRIR LA VENTANA DE GRAFICAR
def run_graf():
    #app = wx.App()
    frame = Graficadora()
    #app.MainLoop()

## FUNCION PARA ABRIR LA VENTANA DE CALCULADORA
def run_calc():
    #app = wx.App()
    frame = Calculadora()
    #app.MainLoop()

def main():
    try:
        app = wx.App()
        frame = Inicio()
        app.MainLoop()
    except:
        print("El programa ha finalizado")


main()
