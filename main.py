from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import io
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de base de datos PostgreSQL usando variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/excel_test")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), nullable=False)
    correo = Column(String(250), nullable=False)
    celular = Column(String(250), nullable=False)

# Intentar crear las tablas si no existen
try:
    Base.metadata.create_all(bind=engine)
except:
    pass

app = FastAPI(title="API de Clientes")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado. Usa CSV o Excel.")
    
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            # Leemos el CSV (asumiendo que viene separado por ; según el ejemplo)
            df = pd.read_csv(io.BytesIO(contents), sep=';')
        else:
            df = pd.read_excel(io.BytesIO(contents))
            
        # Estandarizamos los nombres de las columnas a minúsculas
        df.columns = df.columns.str.lower()
        
        db = SessionLocal()
        nuevos_clientes = 0
        for _, row in df.iterrows():
            cliente = Cliente(
                nombre=str(row['nombre']),
                correo=str(row['correo']),
                celular=str(row['celular'])
            )
            db.add(cliente)
            nuevos_clientes += 1
            
        db.commit()
        db.close()
        
        return {"mensaje": f"Se han cargado {nuevos_clientes} clientes exitosamente."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clientes")
def obtener_clientes():
    try:
        db = SessionLocal()
        clientes = db.query(Cliente).all()
        db.close()
        return [{"id": c.id, "nombre": c.nombre, "correo": c.correo, "celular": c.celular} for c in clientes]
    except Exception as e:
        return {"error": str(e)}
