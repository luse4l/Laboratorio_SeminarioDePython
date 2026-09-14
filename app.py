# Importamos las herramientas necesarias de FastAPI.
# - FastAPI: La clase principal para crear nuestra aplicación.
# - HTTPException, status: Para manejar errores (aunque no se usen en este fragmento, es buena práctica tenerlos).
# - Depends: SÚPER IMPORTANTE. Se usa para la "Inyección de Dependencias" (explicado más abajo).
from fastapi import FastAPI, HTTPException, status, Depends

# Importamos Session de SQLAlchemy para poder tipar nuestra variable de base de datos.
# Esto ayuda a que el editor de código nos sugiera métodos (como .query(), .add(), etc.)
from sqlalchemy.orm import Session

# Importamos cosas específicas de nuestra aplicación (asumiendo que están en un archivo database.py).
# - Producto: El modelo SQLAlchemy que representa la tabla de productos en la base de datos.
# - SessionLocal: La "fábrica" de sesiones que configuramos previamente para conectarnos a la BD.
from database import Producto, SessionLocal

#instanciamos la app
app = FastAPI()

# El decorador @app.get("/") le dice a FastAPI que cuando alguien haga una 
# petición GET a la raíz de la URL (ej: http://localhost:8000/), ejecute esta función.
@app.get("/")
async def root():
    # Retorna un simple diccionario que FastAPI convierte automáticamente a JSON.
    # Es muy útil para verificar rápidamente si la API está encendida y funcionando.
    return {"message": "Hello World"}

# Esta función es un "Generador". Se encarga de manejar el ciclo de vida 
# de la conexión a la base de datos para cada petición que recibe la API.
def get_db():
    # 1. Abre una nueva sesión/conexión temporal con la base de datos.
    db = SessionLocal()
    try:
        # 2. 'yield' es como un 'return' pausado. 
        # Le "presta" la conexión (db) a la función del endpoint (listar_productos) 
        # para que haga sus consultas. La ejecución de esta función get_db() se 
        # queda pausada aquí hasta que el endpoint termina de responderle al usuario.
        yield db
    finally:
        # 3. Una vez que el endpoint terminó (ya sea con éxito o si hubo un error), 
        # el código se reanuda aquí y SIEMPRE cierra la conexión.
        # ESTO ES VITAL: Si no cerramos la conexión, la base de datos se saturará 
        # de conexiones abiertas y la aplicación se caerá.
        db.close()

# Obtener todos los productos
@app.get("/productos")
# La magia de Depends: 
# Cuando alguien llama a /productos, FastAPI lee: "database: Session = Depends(get_db)"
# 1. FastAPI ejecuta get_db() automáticamente.
# 2. Agarra el 'db' que le prestó el 'yield'.
# 3. Se lo inyecta a la variable 'database' para que la usemos adentro.
def listar_productos(database: Session = Depends(get_db)):
    # Usamos la sesión de la base de datos para hacer una consulta (query).
    # "SELECT * FROM productos;" -> Eso es lo que hace por detrás .query(Producto).all()
    # Trae todos los registros y los convierte en objetos de Python (lista de Productos).
    productos = database.query(Producto).all()
    # Retornamos la lista. FastAPI es inteligente y tomará esta lista de objetos 
    # de SQLAlchemy y la transformará en una lista de diccionarios JSON para el cliente.
    return productos


# Obtener un producto por ID
@app.get("/producto/{id}")
def obtener_producto(id: int, database):
 producto = Producto.query.get(id)
 if producto is None:
    raise HTTPException

# Crear un nuevo producto
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(datos_producto, database):
 producto_nuevo = Producto(
    nombre=datos_producto.nombre,
    precio=datos_producto.precio
 )
 database.add(producto_nuevo)
 try:
    database.commit()
    database.refresh(producto_nuevo)
 except:
    database.rollback()
    raise HTTPException(status_code=400, detail="Error al crear persona")
 return vars(producto_nuevo)
#Preguntar a sofi por q cambio todo <3


# Actualizar un producto existente
@app.put("/productos/{id}")
def modificar_producto(id, datos_producto, database):
 producto = Producto.query.get(id)
 if producto is None:
    raise HTTPException(status_code=404, detail="Persona no encontrada")

 producto.nombre = datos_producto.nombre if datos_producto.nombre is not None else None
 producto.precio = datos_producto.precio if datos_producto.precio is not None else None

 database.commit()
 return vars(producto)

# Eliminar un producto
@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id, database):
 producto = Producto.query.get(id)
 if producto is None:
    raise HTTPException(status_code=404, detail="Producto no encontrado")
 database.delete(producto)
 database.commit()