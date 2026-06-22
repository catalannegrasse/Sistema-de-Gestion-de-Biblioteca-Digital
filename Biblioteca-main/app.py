from flask import Flask, render_template, request, redirect, url_for, flash
from biblioteca import Biblioteca, Libro, UsuarioFactory

app = Flask(__name__)
app.secret_key = "dev-secret"

biblioteca = Biblioteca()

# Datos iniciales (pueden modificarse desde la UI)
deal = Libro("The Deal", "Elle Kennedy", 12345, 2015, 360)
mistake = Libro("The Mistake", "Elle Kennedy", 67890, 2015, 283)
score = Libro("The Score", "Elle Kennedy", 13579, 2016, 384)
goal = Libro("The Goal", "Elle Kennedy", 24680, 2016, 384)
for l in (deal, mistake, score, goal):
    biblioteca.agregar_libro(l)

cliente1 = UsuarioFactory.crear_usuario("cliente", "Catalina", "Lannegrasse", 47097607, "catalannegrasse@gmail.com")
cliente2 = UsuarioFactory.crear_usuario("cliente", "Sebastian", "Lannegrasse", 39532319, "sebaleza@gmail.com")
admin1 = UsuarioFactory.crear_usuario("administrador", "Paula", "Asensio", 38654982, "pauasensio@biblioteca.com")
for c in (cliente1, cliente2, admin1):
    biblioteca.agregar_cliente(c)


def find_book_by_isbn(isbn):
    for b in biblioteca.libros:
        if str(b.ISBN) == str(isbn):
            return b
    return None


def find_cliente_by_dni(dni):
    for c in biblioteca.clientes:
        if str(c.dni) == str(dni):
            return c
    return None


@app.route("/")
def index():
    return render_template("index.html", biblioteca=biblioteca)


@app.route("/prestamo", methods=["POST"])
def prestamo():
    dni = request.form.get("cliente_dni")
    isbn = request.form.get("book_isbn")
    fecha = request.form.get("fecha") or "hoy"
    cliente = find_cliente_by_dni(dni)
    libro = find_book_by_isbn(isbn)
    if not cliente:
        flash("Cliente no encontrado.", "error")
    elif not libro:
        flash("Libro no encontrado.", "error")
    elif libro.prestado:
        flash("El libro ya está prestado.", "error")
    else:
        biblioteca.registrar_prestamo(cliente, libro, fecha)
        flash(f"Préstamo registrado: {libro.titulo} -> {cliente.nombre}", "success")
    return redirect(url_for("index"))


@app.route("/devolucion", methods=["POST"])
def devolucion():
    isbn = request.form.get("return_isbn")
    fecha = request.form.get("fecha_devolucion") or "hoy"
    libro = find_book_by_isbn(isbn)
    if not libro:
        flash("Libro no encontrado.", "error")
    else:
        # intentar devolver
        biblioteca.registrar_devolucion(libro, fecha)
        flash(f"Solicitud de devolución procesada para {libro.titulo}", "success")
    return redirect(url_for("index"))


@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente():
    tipo = request.form.get("tipo") or "cliente"
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    dni = request.form.get("dni")
    correo = request.form.get("correo")
    try:
        usuario = UsuarioFactory.crear_usuario(tipo, nombre, apellido, dni, correo)
        biblioteca.agregar_cliente(usuario)
        flash(f"Usuario {nombre} {apellido} agregado.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/agregar_libro", methods=["POST"])
def agregar_libro():
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    isbn = request.form.get("isbn")
    anio = request.form.get("anio")
    paginas = request.form.get("paginas")
    try:
        libro = Libro(titulo, autor, isbn, anio, paginas)
        biblioteca.agregar_libro(libro)
        flash(f"Libro '{titulo}' agregado.", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
