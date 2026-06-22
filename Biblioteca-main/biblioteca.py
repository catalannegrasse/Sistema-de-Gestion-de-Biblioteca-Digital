
def validar_correo(funcion):
    """Decorador que valida que el correo tenga un formato básico antes de asignarlo."""
    def envoltura(self, correo, *args, **kwargs):
        if "@" not in correo or "." not in correo:
            print(f"El correo '{correo}' no es válido. Operación cancelada.")
            return False
        return funcion(self, correo, *args, **kwargs)
    return envoltura

class MetaPersona(type):
    """Metaclase: controla la CREACIÓN de las clases que la usan.
    Obliga a toda subclase de Persona a implementar mostrar_rol()."""
    def __new__(mcs, nombre_clase, bases, namespace):
        cls = super().__new__(mcs, nombre_clase, bases, namespace)
        if bases and "mostrar_rol" not in namespace:
            raise TypeError(f"La clase '{nombre_clase}' debe implementar el método mostrar_rol().")
        return cls

class Persona(metaclass=MetaPersona):
    def __init__(self, nombre, apellido, dni, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self._correo = None
        self.set_correo(correo)

class Administrador(Persona):
    def __init__(self, nombre, apellido, dni, correo):
        super().__init__(nombre, apellido, dni, correo)

    @validar_correo
    def set_correo(self, correo):
        self._correo = correo

    @property
    def correo(self):
        return self._correo

    def mostrar_rol(self):
        return f"Administrador: {self.nombre} {self.apellido} (Acceso Total al Sistema)"


class Cliente(Persona):
    def __init__(self, nombre, apellido, dni, correo):
        super().__init__(nombre, apellido, dni, correo)

    @validar_correo
    def set_correo(self, correo):
        self._correo = correo

    @property
    def correo(self):
        return self._correo

    def mostrar_rol(self):
        return f"Cliente: {self.nombre} {self.apellido} (Permiso de Lectura y Préstamos)"

class UsuarioFactory:
    """Fábrica centralizada para la creación de usuarios."""
    @staticmethod
    def crear_usuario(tipo, nombre, apellido, dni, correo):
        tipo = tipo.strip().lower()
        if tipo == "cliente":
            return Cliente(nombre, apellido, dni, correo)
        elif tipo == "administrador":
            return Administrador(nombre, apellido, dni, correo)
        else:
            raise ValueError(f"El tipo de usuario '{tipo}' no es válido.")

class Libro:
    def __init__(self, titulo, autor, ISBN, anio_publicacion, cant_paginas):
        self.titulo = titulo
        self.autor = autor
        self.ISBN = ISBN
        self.anio_publicacion = anio_publicacion
        self.cant_paginas = cant_paginas
        self.prestado = False

class Prestamo:
    def __init__(self, cliente, libro, fecha_prestamo):
        self.cliente = cliente
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = None

    def set_fecha_devolucion(self, fecha_devolucion):
        self.fecha_devolucion = fecha_devolucion

class Biblioteca:
    def __init__(self):
        self.libros = []      # Relación de agregacion (Los libros existen fuera de la biblioteca)
        self.clientes = []    # Relación de agregacion
        self.prestamos = []   # Relación de composicion (Los préstamos se crean y manejan aquí adentro)

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def eliminar_libro(self, libro):
        if libro in self.libros:
            self.libros.remove(libro)

    def modificar_libro(self, libro, titulo=None, autor=None, anio_publicacion=None, cant_paginas=None):
        if libro not in self.libros:
            print(f"El libro '{libro.titulo}' no pertenece a esta biblioteca.")
            return
        if titulo:
            libro.titulo = titulo
        if autor:
            libro.autor = autor
        if anio_publicacion:
            libro.anio_publicacion = anio_publicacion
        if cant_paginas:
            libro.cant_paginas = cant_paginas
        print(f"Libro '{libro.titulo}' modificado correctamente.")

    def mostrar_libros(self):
        print("Lista de Libros: ")
        for l in self.libros:
            estado = "Prestado" if l.prestado else "Disponible"
            print(f"Título: {l.titulo} | Autor: {l.autor} | ISBN: {l.ISBN} | Estado: {estado}")

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def eliminar_cliente(self, cliente):
        if cliente in self.clientes:
            self.clientes.remove(cliente)

    def modificar_cliente(self, cliente, nombre=None, apellido=None, correo=None):
        if cliente not in self.clientes:
            print(f"El usuario '{cliente.nombre}' no pertenece a esta biblioteca.")
            return
        if nombre:
            cliente.nombre = nombre
        if apellido:
            cliente.apellido = apellido
        if correo:
            resultado = cliente.set_correo(correo)  # reutiliza el decorador @validar_correo ya existente
            if resultado is False:
                return  # el decorador ya informó el motivo del rechazo
        print(f"Usuario '{cliente.nombre}' modificado correctamente.")

    def mostrar_clientes(self):
        print("Lista de Clientes")
        for c in self.clientes:
            print(f"{c.mostrar_rol()} | DNI: {c.dni} | Correo: {c.correo}")

    def registrar_prestamo(self, cliente, libro, fecha_prestamo):
        if libro.prestado:
            print(f"No se puede prestar '{libro.titulo}'. Ya tiene un préstamo activo.")
            return

        # composicion: El objeto Prestamo nace estrictamente aquí adentro
        nuevo_prestamo = Prestamo(cliente, libro, fecha_prestamo)
        self.prestamos.append(nuevo_prestamo)
        libro.prestado = True
        print(f"Préstamo registrado: '{libro.titulo}' asignado a {cliente.nombre}.")

    def registrar_devolucion(self, libro, fecha_devolucion):
        for prestamo in self.prestamos:
            if prestamo.libro == libro and prestamo.fecha_devolucion is None:
                prestamo.set_fecha_devolucion(fecha_devolucion)
                libro.prestado = False
                print(f"Devolución registrada para el libro: '{libro.titulo}' el dia {fecha_devolucion}.")
                return
        print(f"No se encontró un préstamo activo para el libro '{libro.titulo}'.")

    def mostrar_prestamos_activos(self):
        print("Prestamos activos: ")
        activos = [p for p in self.prestamos if p.fecha_devolucion is None]
        if not activos:
            print("No hay préstamos activos en este momento.")
        for p in activos:
            print(f"Libro: {p.libro.titulo} | Cliente: {p.cliente.nombre} {p.cliente.apellido} | Desde: {p.fecha_prestamo}")


if __name__ == "__main__":
    biblioteca = Biblioteca()

    # crear libros
    deal = Libro("The Deal", "Elle Kennedy", 12345, 2015, 360)
    mistake = Libro ("The Mistake", "Elle Kennedy", 67890, 2015, 283)
    score = Libro("The Score", "Elle Kennedy", 13579, 2016, 384)
    goal = Libro("The Goal", "Elle Kennedy", 24680, 2016, 384)
    biblioteca.agregar_libro(deal)
    biblioteca.agregar_libro(mistake)
    biblioteca.agregar_libro(score)
    biblioteca.agregar_libro(goal)

    # probar decorador
    print("\nProbando el Decorador de Correo")
    cliente_falso = UsuarioFactory.crear_usuario("cliente", "Emma", "Lannegrasse", 67094389, "emmalanne.com")

    # crear usuarios usando Factory Method
    cliente1 = UsuarioFactory.crear_usuario("cliente", "Catalina", "Lannegrasse", 47097607, "catalannegrasse@gmail.com")
    cliente2 = UsuarioFactory.crear_usuario("cliente", "Sebastian", "Lannegrasse", 39532319, "sebaleza@gmail.com")
    admin1 = UsuarioFactory.crear_usuario("administrador", "Paula", "Asensio", 38654982, "pauasensio@biblioteca.com")

    biblioteca.agregar_cliente(cliente1)
    biblioteca.agregar_cliente(cliente2)
    biblioteca.agregar_cliente(admin1)

    print("\n")
    biblioteca.mostrar_clientes()

    print("\nRegistro de prestamos")
    # primer prestamo (funciona)
    biblioteca.registrar_prestamo(cliente1, deal, "19/06")
    biblioteca.registrar_prestamo(cliente1, mistake, "19/06")

    biblioteca.registrar_prestamo(cliente2, score, "19/06")
    biblioteca.registrar_prestamo(cliente2, goal, "19/06")

    # intento de prestar el mismo libro
    biblioteca.registrar_prestamo(cliente2, deal, "19/06")

    print("\n")
    # lista de prestamos activos
    biblioteca.mostrar_prestamos_activos()

    print("\nRegistro de devoluciones")
    # registro de devolucion
    biblioteca.registrar_devolucion(deal, "26/06")
    biblioteca.registrar_devolucion(mistake, "26/06")
    biblioteca.registrar_devolucion(score, "26/06")
    biblioteca.registrar_devolucion(goal, "26/06")

    print("\nProbando modificación de libro y usuario")
    # modificar un libro existente
    biblioteca.modificar_libro(deal, anio_publicacion=2016, cant_paginas=365)
    # modificar un usuario existente
    biblioteca.modificar_cliente(cliente1, correo="catalina.lannegrasse@gmail.com")
    # intento de modificar con un correo inválido (el decorador lo rechaza)
    biblioteca.modificar_cliente(cliente2, correo="sebanuevo-correo.com")

    print("\n")
    # lista de libros
    biblioteca.mostrar_libros()