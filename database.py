from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear motor de base de datos SQLite
engine = create_engine('sqlite:///mi_base.db', echo=True)

# Declarar la base
Base = declarative_base()

# Crear una clase que representa una tabla
class Producto(Base):
 __tablename__ = 'productos'
 id = Column(Integer, primary_key=True, autoincrement = True, nullable = False)
 nombre = Column(String)
 precio = Column(Float)

# Crear las tablas en el archivo si no existen
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base
Session = sessionmaker(bind=engine)
session = Session()

# Agregar un producto
#nuevo_producto = Producto(nombre="Esponja", precio=11.11)
#session.add(nuevo_producto)
#session.commit()

#Consultar productos
#for producto in session.query(Producto).all():
    #print(producto.nombre, producto.precio)
