import os
import json
from tabulate import tabulate

# Nombres de los archivos JSON donde se almacenará la información
ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"

# Categorías disponibles de libros en la biblioteca
CATEGORIAS = [
    "Generalidades", "Filosofía", "Religión", "Ciencias sociales y Política", "Filología y psicología",
    "Matemáticas y Ciencias naturales", "Tecnología y ciencias prácticas", "Arte y literatura", "Historia y Geografía"
]

class Biblioteca:
    def __init__(self):
        # Carga los datos de los archivos JSON al iniciar
        self.libros = self.cargar_datos(ARCHIVO_LIBROS)
        self.usuarios = self.cargar_datos(ARCHIVO_USUARIOS)
        self.prestamos = self.cargar_datos(ARCHIVO_PRESTAMOS, lista=True)

    def cargar_datos(self, archivo, lista=False):
        # Carga los datos desde un archivo JSON, si existe
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as file:
                return json.load(file)
        return {} if not lista else []

    def guardar_datos(self, archivo, datos):
        # Guarda los datos en un archivo JSON
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)

    def agregar_libro(self):
        # Agrega un nuevo libro a la biblioteca
        isbn = input("Ingrese el Código ISBN del libro: ")
        if isbn in self.libros:
            print("Error: ISBN ya registrado.")
            return

        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        # Muestra las categorías disponibles y permite seleccionar una
        print("\n+----------------------------------+")
        print("| Seleccione la categoría del libro: |")
        print("+------------------------------------+")
        for i, categoria in enumerate(CATEGORIAS, 1):
            print(f"{i}. {categoria}")
        categoria = CATEGORIAS[int(input("Seleccione el número de la categoría: ")) - 1]
        
        # Guarda el libro en el diccionario y en el archivo JSON
        self.libros[isbn] = {"Título": titulo, "Autor": autor, "Categoría": categoria, "ISBN": isbn}
        self.guardar_datos(ARCHIVO_LIBROS, self.libros)
        print("Libro añadido con éxito.")

    def eliminar_libro(self):
        # Elimina un libro de la biblioteca
        isbn = input("Ingrese el Código ISBN del libro a eliminar: ")
        if isbn in self.libros:
            del self.libros[isbn]
            self.guardar_datos(ARCHIVO_LIBROS, self.libros)
            print("Libro eliminado con éxito.")
        else:
            print("Error: ISBN no encontrado.")

    def registrar_usuario(self):
        # Registra un nuevo usuario en la biblioteca
        id_usuario = input("Ingrese ID único del usuario: ")
        if id_usuario in self.usuarios:
            print("Error: ID ya registrado.")
            return
        nombre = input("Ingrese el nombre del usuario: ")
        self.usuarios[id_usuario] = {"Nombre": nombre, "ID": id_usuario, "Libros Prestados": []}
        self.guardar_datos(ARCHIVO_USUARIOS, self.usuarios)
        print("Usuario registrado con éxito.")
    
    def dar_baja_usuario(self):
        # Da de baja a un usuario registrado
        id_usuario = input("Ingrese ID del usuario a dar de baja: ")
        if id_usuario in self.usuarios:
            del self.usuarios[id_usuario]
            self.guardar_datos(ARCHIVO_USUARIOS, self.usuarios)
            print("Usuario eliminado con éxito.")
        else:
            print("Error: Usuario no encontrado.")

    def prestar_libro(self):
        id_usuario = input("Ingrese ID del usuario: ")
        if id_usuario not in self.usuarios:
            print("Error: Usuario no registrado.")
            return
        isbn = input("Ingrese el ISBN del libro a prestar: ")
        
        # Verifica si el libro ya está prestado
        if any(prestamo["Libro"]["ISBN"] == isbn for prestamo in self.prestamos):
            print("Error: Libro se encuentra prestado.")
            return
        if isbn not in self.libros:
            print("Error: Libro no encontrado.")
            return
        self.usuarios[id_usuario]["Libros Prestados"].append(self.libros[isbn])
        self.prestamos.append({"Usuario": id_usuario, "Libro": self.libros[isbn]})
        self.guardar_datos(ARCHIVO_USUARIOS, self.usuarios)
        self.guardar_datos(ARCHIVO_PRESTAMOS, self.prestamos)
        print("Libro prestado con éxito.")

    def devolver_libro(self):
        id_usuario = input("Ingrese ID del usuario: ")
        if id_usuario not in self.usuarios:
            print("Error: Usuario no registrado.")
            return
        isbn = input("Ingrese el ISBN del libro a devolver: ")
        prestamos_usuario = self.usuarios[id_usuario]["Libros Prestados"]
        
        for libro in prestamos_usuario:
            if libro["ISBN"] == isbn:
                prestamos_usuario.remove(libro)
                self.prestamos = [p for p in self.prestamos if not (p["Usuario"] == id_usuario and p["Libro"]["ISBN"] == isbn)]
                self.guardar_datos(ARCHIVO_USUARIOS, self.usuarios)
                self.guardar_datos(ARCHIVO_PRESTAMOS, self.prestamos)
                print("Libro devuelto con éxito.")
                return
        print("Error: El usuario no tiene prestado ese libro.")
    
    def buscar_libros(self):
        busqueda = input("Ingrese título, autor o categoría del libro a buscar: ").lower()
        resultados = [libro for libro in self.libros.values() if busqueda in libro["Título"].lower() or busqueda in libro["Autor"].lower() or busqueda in libro["Categoría"].lower()]
        self.mostrar_tabla(resultados)

    def mostrar_todos_libros(self):
        print("\n****************** Libros en la Biblioteca ******************")
        libros_por_categoria = {categoria: [] for categoria in CATEGORIAS}
        
        for libro in self.libros.values():
            libros_por_categoria[libro["Categoría"]].append(libro)
        
        for categoria, libros in libros_por_categoria.items():
            if libros:
                print(f"\nCategoría: {categoria}")
                self.mostrar_tabla(libros)


    def listar_prestamos(self):
        print("\n********************* Libros Prestados *********************")
        prestamos_tabla = [{"Usuario": p["Usuario"], "Título": p["Libro"]["Título"], "Autor": p["Libro"]["Autor"], "ISBN": p["Libro"]["ISBN"]} for p in self.prestamos]
        self.mostrar_tabla(prestamos_tabla)
    
    # Muestra los datos en una tabla con diseño
    def mostrar_tabla(self, datos):
        if datos:
            print(tabulate(datos, headers="keys", tablefmt="fancy_grid"))
        else:
            print("No hay registros disponibles.")

def mostrar_menu():
    biblioteca = Biblioteca()
    # Muestra el menú de opciones del sistema de biblioteca
    while True:
        print("\n" + "=" * 60)
        print("║        Sistema de Gestión de Biblioteca Digital          ║")
        print("║           Universidad Estatal Amazónica UEA              ║")
        print("=" * 60)
        print("1. Añadir libro a la Biblioteca")
        print("2. Quitar libro de la Biblioteca")
        print("3. Registrar usuario")
        print("4. Dar de baja a usuario")
        print("5. Prestar libro")
        print("6. Devolución de libros")
        print("7. Buscar libros")
        print("8. Mostrar todos los libros")
        print("9. Lista de libros prestados")
        print("10. Salir")
        print("=" * 60)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            biblioteca.agregar_libro()
        elif opcion == "2":
            biblioteca.eliminar_libro()
        elif opcion == "3":
            biblioteca.registrar_usuario()
        elif opcion == "4":
            biblioteca.dar_baja_usuario()
        elif opcion == "5":
            biblioteca.prestar_libro()
        elif opcion == "6":
            biblioteca.devolver_libro()
        elif opcion == "7":
            biblioteca.buscar_libros()
        elif opcion == "8":
            biblioteca.mostrar_todos_libros()
        elif opcion == "9":
            biblioteca.listar_prestamos()
        elif opcion == "10":
            print("============ Gracias por usar la Biblioteca Digital de la UEA. ¡Hasta luego! ============")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        input("\nPresione Enter para continuar...")

mostrar_menu()