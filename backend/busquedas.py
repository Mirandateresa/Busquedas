from arbol import Nodo

class Buscador:
    def __init__(self):
        # Conexiones BFS - SIN PESOS (Actualizado con todas las conexiones)
        self.conexiones_bfs = {
            'JILOYORK': ['CELAYA', 'CDMX', 'QUERÉTARO', 'SINALOA'],
            'SONORA': ['ZACATECAS', 'SINALOA'],
            'GUANAJUATO': ['AGUASCALIENTES', 'QUERÉTARO', 'CELAYA'],
            'OAXACA': ['QUERÉTARO'],
            'SINALOA': ['CELAYA', 'SONORA', 'JILOYORK', 'QUERÉTARO'],
            'CELAYA': ['JILOYORK', 'SINALOA', 'GUANAJUATO', 'QUERÉTARO'],
            'ZACATECAS': ['SONORA', 'MONTERREY', 'QUERÉTARO', 'AGUASCALIENTES'],
            'MONTERREY': ['ZACATECAS', 'MONTERREY', 'TAMAULIPAS', 'CDMX', 'QUERÉTARO'],
            'TAMAULIPAS': ['QUERÉTARO', 'MONTERREY', 'CDMX'],
            'CDMX': ['JILOYORK', 'MONTERREY', 'QUERÉTARO', 'TAMAULIPAS'],
            'AGUASCALIENTES': ['GUANAJUATO', 'ZACATECAS', 'QUERÉTARO'],
            'QUERÉTARO': ['TAMAULIPAS', 'ZACATECAS', 'SINALOA', 'JILOYORK', 'OAXACA', 'CDMX', 'CELAYA', 'AGUASCALIENTES', 'GUANAJUATO', 'MONTERREY']
        }
        
        # Conexiones UCS - CON PESOS (Actualizado)
        self.conexiones_ucs = {
            'JILOYORK': {'CDMX': 125, 'QRO': 513, 'SINALOA': 200, 'CELAYA': 150},
            'MORELOS': {'QRO': 425, 'CDMX': 180},
            'CDMX': {'JILOYORK': 125, 'QRO': 423, 'HGO': 491, 'MORELOS': 180, 'PUEBLA': 150, 'TOLUCA': 100, 'MONTERREY': 400, 'TAMAULIPAS': 350},
            'HGO': {'CDMX': 491, 'QRO': 351, 'MEXICALI': 309, 'MTY': 346, 'SLP': 280},
            'QRO': {'SLP': 203, 'MORELOS': 514, 'JILOYORK': 513, 'CDMX': 423, 
                   'MONTERREY': 603, 'SONORA': 437, 'HGO': 356, 'MEXICALI': 313, 
                   'AGS': 599, 'CELAYA': 180, 'TAMAULIPAS': 450, 'ZACATECAS': 350},
            'SLP': {'AGS': 390, 'QRO': 203, 'HGO': 280, 'ZACATECAS': 320},
            'AGS': {'SLP': 390, 'QRO': 599, 'GUANAJUATO': 180, 'ZACATECAS': 250},
            'SONORA': {'QRO': 437, 'MEXICALI': 394, 'SINALOA': 350, 'ZACATECAS': 400},
            'MEXICALI': {'MTY': 296, 'HGO': 309, 'QRO': 313, 'SONORA': 394},
            'MTY': {'MEXICALI': 296, 'QRO': 603, 'HGO': 436, 'ZACATECAS': 250, 'MONTERREY': 0},
            'MONTERREY': {'MTY': 0, 'QRO': 603, 'ZACATECAS': 200, 'CDMX': 400, 'TAMAULIPAS': 300},
            'CELAYA': {'JILOYORK': 150, 'SINALOA': 250, 'QRO': 180, 'GUANAJUATO': 100},
            'SINALOA': {'CELAYA': 250, 'SONORA': 350, 'JILOYORK': 200, 'QUERÉTARO': 300},
            'ZACATECAS': {'SONORA': 400, 'MONTERREY': 200, 'QUERÉTARO': 350, 'SLP': 320, 'AGS': 250},
            'GUANAJUATO': {'AGS': 180, 'CELAYA': 100, 'QUERÉTARO': 200},
            'TAMAULIPAS': {'QRO': 450, 'MONTERREY': 300, 'CDMX': 350},
            'PUEBLA': {'CDMX': 150, 'QRO': 280},
            'TOLUCA': {'CDMX': 100, 'QRO': 220}
        }
    
    def buscar_bfs(self, estado_inicial, solucion):
        solucionado = False
        nodos_visitados = []
        nodos_frontera = []
        nodo_inicial = Nodo(estado_inicial)
        nodos_frontera.append(nodo_inicial)
        
        while (not solucionado) and len(nodos_frontera) != 0:
            nodo = nodos_frontera[0]
            nodos_visitados.append(nodos_frontera.pop(0))
            
            if nodo.get_datos() == solucion:
                solucionado = True
                return nodo
            else:
                dato_nodo = nodo.get_datos()
                lista_hijos = []
                
                for un_hijo in self.conexiones_bfs.get(dato_nodo, []):
                    hijo = Nodo(un_hijo)
                    hijo.set_padre(nodo)
                    lista_hijos.append(hijo)
                    
                    if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                        nodos_frontera.append(hijo)
                
                nodo.set_hijos(lista_hijos)
        
        return None
    
    def buscar_ucs(self, estado_inicial, solucion):
        solucionado = False
        nodos_visitados = []
        nodos_frontera = []
        nodo_inicial = Nodo(estado_inicial)
        nodo_inicial.set_coste(0)
        nodos_frontera.append(nodo_inicial)
        
        while (not solucionado) and len(nodos_frontera) != 0:
            nodos_frontera = sorted(nodos_frontera, key=lambda x: x.get_coste())
            nodo = nodos_frontera[0]
            nodos_visitados.append(nodos_frontera.pop(0))
            
            if nodo.get_datos() == solucion:
                solucionado = True
                return nodo
            else:
                dato_nodo = nodo.get_datos()
                lista_hijos = []
                
                for un_hijo, coste in self.conexiones_ucs.get(dato_nodo, {}).items():
                    hijo = Nodo(un_hijo)
                    hijo.set_coste(nodo.get_coste() + coste)
                    hijo.set_padre(nodo)
                    lista_hijos.append(hijo)
                    
                    if not hijo.en_lista(nodos_visitados):
                        if hijo.en_lista(nodos_frontera):
                            for n in nodos_frontera:
                                if n.igual(hijo) and n.get_coste() > hijo.get_coste():
                                    nodos_frontera.remove(n)
                                    nodos_frontera.append(hijo)
                        else:
                            nodos_frontera.append(hijo)
                
                nodo.set_hijos(lista_hijos)
        
        return None
    
    def dfs_prof_iter(self, estado_inicial, solucion):
        """Búsqueda en profundidad iterativa para vuelos"""
        for limite in range(0, 100):
            visitados = []
            nodo_inicial = Nodo(estado_inicial)
            sol = self.buscar_dfs_rec(nodo_inicial, solucion, visitados, limite)
            if sol is not None:
                return sol
        return None
    
    def buscar_dfs_rec(self, nodo, solucion, visitados, limite):
        """Búsqueda DFS recursiva con límite"""
        if limite > 0:
            visitados.append(nodo)
            if nodo.get_datos() == solucion:
                return nodo
            else:
                dato_nodo = nodo.get_datos()
                lista_hijos = []
                
                for un_hijo in self.conexiones_bfs.get(dato_nodo, []):
                    hijo = Nodo(un_hijo)
                    if not hijo.en_lista(visitados):
                        hijo.set_padre(nodo)
                        lista_hijos.append(hijo)
                
                nodo.set_hijos(lista_hijos)
                
                for nodo_hijo in nodo.get_hijos():
                    if nodo_hijo.get_datos() not in [v.get_datos() for v in visitados]:
                        sol = self.buscar_dfs_rec(nodo_hijo, solucion, visitados, limite - 1)
                        if sol is not None:
                            return sol
        
        return None
    
    def obtener_ruta(self, nodo_solucion, estado_inicial, tipo_busqueda=None):
        if nodo_solucion is None:
            return None, None
        
        resultado = []
        nodo = nodo_solucion
        
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        
        resultado.append(estado_inicial)
        resultado.reverse()
        
        if tipo_busqueda in ['bfs', 'dfs']:
            coste_total = len(resultado) - 1
        else:
            coste_total = nodo_solucion.get_coste() if nodo_solucion.get_coste() > 0 else len(resultado) - 1
        
        return resultado, coste_total