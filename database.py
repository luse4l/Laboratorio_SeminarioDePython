from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Crear motor de base de datos SQLite
engine = create_engine('sqlite:///database.db', echo=True)

# Declarar la base
Base = declarative_base()

# Crear una clase que representa una tabla
class Producto(Base):
 __tablename__ = 'productos'
 id = Column(Integer, primary_key=True, autoincrement = True, nullable = False)
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

# Crear las tablas en el archivo si no existen
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base
Session = sessionmaker(bind=engine)
