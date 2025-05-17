from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String, nullable=False)
    contrasena = Column(String, nullable=False)
    notas = relationship("Nota", back_populates="usuario")

class Nota(Base):
    __tablename__ = 'nota'
    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    categoria = Column(String, nullable=False)
    enlaces = Column(Text)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    usuario = relationship("Usuario", back_populates="notas")

# Crear base de datos en disco
engine = create_engine('sqlite:///gestor_notas.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# NO agregues usuarios ni notas aquí, solo consulta:
usuarios = session.query(Usuario).all()
print("Usuarios:")
for u in usuarios:
    print(f"{u.id_usuario}: {u.nombre_usuario}")

for u in usuarios:
    notas_usuario = session.query(Nota).filter_by(id_usuario=u.id_usuario).all()
    print(f"Notas del usuario {u.nombre_usuario}:")
    for n in notas_usuario:
        print(f"{n.titulo} - {n.categoria}")
