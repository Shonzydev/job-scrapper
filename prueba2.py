class Figura:
    def __init__(self,nombre):
        self.nombre = nombre

    def describir(self):
        return f"{self.nombre} tiene area {self.area()}"

    def area(self):
        return 0

class Cuadrado(Figura):
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado

    def area(self):
        return self.lado * self.lado

class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectangulo")
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura
        


print(Cuadrado(4).describir())          # Cuadrado tiene área 16
print(Rectangulo(3, 5).describir())     # Rectangulo tiene área 15
