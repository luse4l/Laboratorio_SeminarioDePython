<<<<<<< HEAD
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
=======
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
>>>>>>> Lucia-abmProducto

# Crear motor de base de datos SQLite
engine = create_engine('sqlite:///database.db', echo=True)

# Declarar la base
Base = declarative_base()

# Crear una clase que representa una tabla
class Producto(Base):
 __tablename__ = 'productos'
 id = Column(Integer, primary_key=True, autoincrement = True, nullable = False)
<<<<<<< HEAD
 nombre = Column(String, nullable = False)
 precio = Column(Float, nullable = False)

#preguntar a sofi por que creo la clase ventas !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=======
 nombre = Column(String(100), nullable = False) #limitamos el nombre a 100 caracteres
 precio = Column(Float, nullable = False)
 ventas = relationship("Venta", back_populates="producto")
#Ponemos la clase venta entre comillas porque todavia no existe
#back_populates apunta a producto de abajo. back_populates automatiza el trabajo de mantener las 
#dos tablas conectadas en la memoria de Python

class Venta(Base):
    __tablename__ = 'ventas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False) #conexion cn el id producto
    producto = relationship("Producto", back_populates="ventas") #espejo de ventas en producto
>>>>>>> Lucia-abmProducto

# Crear las tablas en el archivo si no existen
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base
Session = sessionmaker(bind=engine)
<<<<<<< HEAD
session = Session()

# Agregar un producto
#nuevo_producto = Producto(nombre="Esponja", precio=11.11)
#session.add(nuevo_producto)
#session.commit()

#Consultar productos
#for producto in session.query(Producto).all():
<<<<<<< HEAD
    #print(producto.nombre, producto.precio)
=======
    #print(producto.nombre, producto.precio)
>>>>>>> Lucia-abmProducto
=======
>>>>>>> Lucia-abmProducto
