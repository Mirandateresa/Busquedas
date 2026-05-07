class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
        self.coste = 0
        self.hijos = []
    
    def get_datos(self):
        return self.datos
    
    def get_padre(self):
        return self.padre
    
    def set_padre(self, padre):
        self.padre = padre
    
    def get_coste(self):
        return self.coste
    
    def set_coste(self, coste):
        self.coste = coste
    
    def get_hijos(self):
        return self.hijos
    
    def set_hijos(self, hijos):
        self.hijos = hijos
    
    def en_lista(self, lista):
        for n in lista:
            if n.get_datos() == self.datos:
                return True
        return False
    
    def igual(self, nodo):
        return self.datos == nodo.get_datos()