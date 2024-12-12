from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from faker import Faker
import sqlite3
import random

# Inicializar Faker para generación de datos
fake = Faker()

# Conectarse a la base de datos existente
conn = sqlite3.connect('C:\\Users\\MegaTecnologia\\Documents\\programacion_1\\backend\\DB\\biblioteca.db')
cur = conn.cursor()

# Crear un archivo de log para registrar los datos
log_file = 'db.log'
with open(log_file, 'w') as log:
    log.write(f'LOG DE DATOS INSERTADOS - {datetime.now()}\n\n')

    # Generar datos para la tabla "usuarios"
    datos_usuarios = []
    datos_usuarios.append((32, "pedro", "perez", generate_password_hash("auto"), "admin@email.com", "123456789", "admin"))
    log.write(f'ID: {1}, Nombre: {"pedro"}, Apellido: {"perez"}, psk: {"auto"}, Email: {"admin@email.com"}, Telefono: {"123456789"}, Rol: {"admin"}\n')
    log.write('\n')
    for i in range(1, 31):
        usuarioID = i
        usuario_nombre = fake.first_name()
        usuario_apellido = fake.last_name()
        usuario_contrasena = fake.password()
        usuario_email = fake.email()
        usuario_telefono = fake.phone_number()
        rol = fake.random_element(elements=('admin', 'user', 'librarian'))
        datos_usuarios.append((usuarioID, usuario_nombre, usuario_apellido, generate_password_hash(usuario_contrasena), usuario_email, usuario_telefono, rol))
        log.write(f'ID: {usuarioID}, Nombre: {usuario_nombre}, Apellido: {usuario_apellido}, psk: {usuario_contrasena}, Email: {usuario_email}, Telefono: {usuario_telefono}, Rol: {rol}\n')
    log.write('\n')

    # Insertar datos en la tabla "usuarios"
    cur.executemany('''
        INSERT INTO usuarios (
            usuarioID,
            usuario_nombre,
            usuario_apellido,
            usuario_contrasena,
            usuario_email,
            usuario_telefono,
            rol
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', datos_usuarios)

    # Generar datos para la tabla "libros"
    datos_libros = []
    for i in range(1, 31):
        libroID = 1000 + i
        titulo = fake.sentence(nb_words=3)
        editorial = fake.company()
        genero = fake.word()
        image = f'image{random.randint(0, 8)}.jpg'
        datos_libros.append((libroID, titulo, editorial, genero, image))

    # Insertar datos en la tabla "libros"
    cur.executemany('''
        INSERT INTO libros (libroID, titulo, editorial, genero, image) VALUES (?, ?, ?, ?, ?)
    ''', datos_libros)

    # Generar datos para la tabla "libros_copias"
    datos_copias = []
    for libro in datos_libros:
        libroID = libro[0]  # Obtener libroID
        num_copias = random.randint(1, 5)  # Número aleatorio de copias por libro
        for _ in range(num_copias):
            datos_copias.append((libroID,))

    # Insertar datos en la tabla "libros_copias"
    cur.executemany('''
        INSERT INTO libros_copias (libroID) VALUES (?)
    ''', datos_copias)

    # Generar datos para la tabla "autores"
    datos_autores = []
    for i in range(1, 31):
        autorID = i
        autor_nombre = fake.first_name()
        autor_apellido = fake.last_name()
        datos_autores.append((autorID, autor_nombre, autor_apellido))

    # Insertar datos en la tabla "autores"
    cur.executemany('''
        INSERT INTO autores (autorID, autor_nombre, autor_apellido) VALUES (?, ?, ?)
    ''', datos_autores)

    # Generar datos para la tabla "resenas"
    datos_resenas = []
    resenaID = 1  
    for libroID in range(1001, 1031):  
        num_resenas = random.randint(1, 6)  # Determinar cuántas resenas generar para cada libro
        for _ in range(num_resenas):
            usuarioID = random.randint(1, 30)  # Seleccionar un usuario aleatorio
            valoracion = fake.random_int(min=1, max=5)
            comentario = fake.text(max_nb_chars=100)
            datos_resenas.append((resenaID, usuarioID, libroID, valoracion, comentario))
            resenaID += 1  

    # Insertar datos en la tabla "resenas"
    cur.executemany('''
        INSERT INTO resenas (resenaID, usuarioID, libroID, valoracion, comentario) VALUES (?, ?, ?, ?, ?)
    ''', datos_resenas)


    # Generar datos para la tabla "prestamos"
    # Filtrar IDs de usuarios con rol 'user'
    usuarios_user = [usuario[0] for usuario in datos_usuarios if usuario[6] == 'user']

    # Obtener IDs de todas las copias generadas
    cur.execute('SELECT copiaID FROM libros_copias')
    copias_disponibles = [row[0] for row in cur.fetchall()]

    # Generar datos de préstamos asignando copias específicas
    datos_prestamos = []
    prestamoID = 1  # Contador único para préstamoID

    for usuarioID in usuarios_user:
        num_prestamos = random.randint(1, 5)  # Número de préstamos por usuario
        for _ in range(num_prestamos):
            if not copias_disponibles:
                break  # Detenerse si no quedan copias disponibles

            copiaID = copias_disponibles.pop(0)  # Obtener y remover la primera copia disponible
            fecha_entrega = fake.date_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 3, 31))
            fecha_devolucion = fecha_entrega + timedelta(days=fake.random_int(min=7, max=90))  # Plazo de devolución

            datos_prestamos.append((prestamoID, usuarioID, copiaID, fecha_entrega, fecha_devolucion))
            prestamoID += 1

    # Insertar datos en la tabla "prestamos"
    cur.executemany('''
        INSERT INTO prestamos (prestamoID, usuarioID, copiaID, fecha_entrega, fecha_devolucion) VALUES (?, ?, ?, ?, ?)
    ''', datos_prestamos)


    # Generar datos para la tabla "notificaciones"
    datos_notificaciones = []
    for i in range(1, 31):
        notificacionID = i
        titulo = fake.sentence(nb_words=4)  # Título breve
        descripcion = fake.text(max_nb_chars=100)  # Descripción más detallada
        vista = fake.boolean(chance_of_getting_true=50)  # Estado de vista (True o False)
        categoria = fake.random_element(elements=["warning", "danger", "info"])  # Categorías válidas
        usuarioID = random.randint(1, 30)  # Asociar con un usuario aleatorio
        datos_notificaciones.append((notificacionID, titulo, descripcion, vista, categoria, usuarioID))

    # Insertar datos en la tabla "notificaciones"
    cur.executemany('''
        INSERT INTO notificaciones (
            notificacionID, titulo, descripcion, vista, categoria, usuarioID
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', datos_notificaciones)



    # Generar datos para la tabla "libros_autores"
    datos_libros_autores = []
    for i in range(1, 31):
        libroID = 1000 + i
        autorID = i
        datos_libros_autores.append((libroID, autorID))

    # Insertar datos en la tabla "libros_autores"
    cur.executemany('''
        INSERT INTO libros_autores (libroID, autorID) VALUES (?, ?)
    ''', datos_libros_autores)



# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Datos insertados correctamente en la base de datos existente.")
