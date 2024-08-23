from nodos import *


from abc import abstractmethod
from abc import ABCMeta
from cubo import *

#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):  
        pass



#Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
#Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()]=hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None


class BusquedaProfundidad(Busqueda):
    
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(-1)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys() and hijo.cubo.visualizar() not in abiertos:
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()]=hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaProfundidadIterativa(Busqueda):
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        profundidad_maxima_actual = 0
        
        while not solucion:
            cerrados = dict()
            profundidad_maxima_actual +=1
            abiertos.append(NodoProfundidad(inicial, None, None, 0))
            cerrados[inicial.cubo.visualizar()] = inicial

            while not solucion and len(abiertos) > 0:
                nodoActual = abiertos.pop()
                actual = nodoActual.estado
                if actual.esFinal():
                    solucion = True
                
                else:
                    cerrados[actual.cubo.visualizar()] = actual
                    if nodoActual.profundidad < profundidad_maxima_actual:
                        for operador in actual.operadoresAplicables():
                            hijo = actual.aplicarOperador(operador)
                            abiertos.append(NodoProfundidad(hijo, nodoActual, operador, nodoActual.profundidad + 1))
                            cerrados[hijo.cubo.visualizar()] = hijo
                

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
            
                            

class BusquedaVoraz(Busqueda):
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial
        while not solucion and len(abiertos) > 0:
            abiertos.sort(key=lambda x: Cubo.HeuristicaManhattan(x.estado.cubo))
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None: 
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        


class BusquedaAStar(Busqueda):
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAStar(inicial, None, None, 0))  
        cerrados[inicial.cubo.visualizar()] = NodoAStar(inicial, None, None, 0)  
        while not solucion and len(abiertos) > 0:
            abiertos.sort(key=lambda x: x.costo + Cubo.HeuristicaManhattan(x.estado.cubo))  
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    g_nuevo = nodoActual.costo + 1 
                    h_estimada = Cubo.HeuristicaManhattan(hijo.cubo)  
                    if hijo.cubo.visualizar() not in cerrados.keys() or g_nuevo + h_estimada < cerrados[hijo.cubo.visualizar()].costo:
                        abiertos.append(NodoAStar(hijo, nodoActual, operador, g_nuevo))
                        cerrados[hijo.cubo.visualizar()] = NodoAStar(hijo, nodoActual, operador, g_nuevo)  
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None:  
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        
class BusquedaIDAStar(Busqueda):
    def buscarSolucion(self, inicial):
        NUEVA_COTA = Cubo.Heuristica_Distancia_Comparación(inicial.cubo)
        Solucion = False
        while not Solucion:
            COTA = NUEVA_COTA
            NUEVA_COTA = float('inf')
            ABIERTOS = []
            ABIERTOS.append(NodoAStar(inicial, None, None, 0))  
            while ABIERTOS and not Solucion:
                ABIERTOS.sort(key=lambda x:Cubo.HeuristicaManhattan(x.estado.cubo))
                ACTUAL = ABIERTOS.pop(0)
                actual = ACTUAL.estado
                if actual.esFinal():
                    Solucion = True
                else:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        g = ACTUAL.costo + 1 
                        f = g + Cubo.HeuristicaManhattan(hijo.cubo)
                        if f <= COTA:
                            ABIERTOS.append(NodoAStar(hijo, ACTUAL, operador, g))
                        else:
                            NUEVA_COTA = min(NUEVA_COTA, f)
        if Solucion:
            lista = []
            nodo = ACTUAL
            while nodo.padre is not None:  
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        

    


   




