from fastapi import FastAPI, HTTPException, status
from database import Producto

app = FastAPI()

# Obtener todos los productos
@app.get("/productos")
def listar_productos(database):
 productos = Producto.query.all()
 return [vars(p) for p in productos]

#producto = session.query(Producto).all()  ?????????????????????????????????????'

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