import json


class Palabra:
    def __init__(self, id_nombre, diccionario=None):
        self.id_nombre = id_nombre
        self.diccionario = diccionario if diccionario is not None else {}

    def agregar_entrada(self, indice_3_digitos, lista_indices_10_digitos):
        # Verificar que el índice tenga 3 dígitos y la lista contenga índices de 10 dígitos
        if len(str(indice_3_digitos)) == 3 and all(len(str(i)) == 10 for i in lista_indices_10_digitos):
            if indice_3_digitos in self.diccionario:
                self.diccionario[indice_3_digitos].extend(lista_indices_10_digitos)
            else:
                self.diccionario[indice_3_digitos] = lista_indices_10_digitos
        else:
            raise ValueError("El índice debe tener 3 dígitos y los valores deben ser listas de índices de 10 dígitos.")

    def obtener_diccionario(self):
        return self.diccionario

    def __str__(self):
        # Crear una representación en cadena del diccionario y del id_nombre
        resultado = f"Palabra: {self.id_nombre}\nDiccionario:\n"
        for clave, valores in self.diccionario.items():
            valores_str = ', '.join(map(str, valores))
            resultado += f"  {clave}: [{valores_str}]\n"
        return resultado

    def to_dict(self):
        """Convertir el objeto a un diccionario para serialización JSON."""
        return {
            'id_nombre': self.id_nombre,
            'diccionario': self.diccionario
        }

    @staticmethod
    def from_dict(data):
        """Crear un objeto Palabra a partir de un diccionario."""
        return Palabra(
            id_nombre=data['id_nombre'],
            diccionario=data['diccionario']
        )
