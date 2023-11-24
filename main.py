import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Conecta a la base de datos
conn = sqlite3.connect("sql/dispositivos.db")

app = fastapi.FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://frontend-api-f54e97981b98.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dispositivos(BaseModel):
    id_dispositivo: int
    dispositivo: str
    valor: int

@app.post("/dispositivos")
async def crear_dispositivos(dispositivo: Dispositivos):
    c = conn.cursor()
    c.execute('INSERT INTO dispositivos (id_dispositivo, dispositivo, valor) VALUES (?, ?, ?)',
              (dispositivo.id_dispositivo, dispositivo.dispositivo, dispositivo.valor))
    conn.commit()
    return dispositivo

@app.get("/dispositivos")
async def obtener_dispositivos():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos;')
    response = []
    for row in c:
        dispositivo = {"id_dispositivo": row[0], "dispositivo": row[1], "valor": row[2]}
        response.append(dispositivo)
    return response

@app.get("/dispositivos/{id_dispositivo}")
async def obtener_dispoditivo(id_dispositivo: int):
    """Obtiene un contacto por su email."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    contacto = None
    for row in c:
        contacto = {"id_dispositivo": row[0], "dispositivo": row[1], "valor": row[2]}
    return disositivo



@app.put("/dispositivos/{id_dispositivo}/{valor}")
async def actualizar_dispositivo(valor: int, id_dispositivo: int):
    """Actualiza un dispositivo."""
    # DONE Actualiza el dispositivo en la base de datos
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET valor = ? WHERE id_dispositivo = ?',
              (valor, id_dispositivo))
    conn.commit()
    return {"message": "Dispositivo actualizado correctamente"}

