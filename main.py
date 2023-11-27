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
    allow_origins=["*"],
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
async def obtener_dispositivo(id_dispositivo: int):
    """Obtiene un dispositivo por su id."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    dispositivo = None
    for row in c:
        dispositivo = {"id_dispositivo": row[0], "dispositivo": row[1], "valor": row[2]}
    return dispositivo

@app.get("/dispositivos/{id_dispositivo}/{valor}")
async def obtener_dispositivo(id_dispositivo: int, valor: int):
    """Obtiene el valor de un dispositivo por su ID."""
    c = conn.cursor()
    c.execute('SELECT valor FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    valor_dispositivo = c.fetchone()

    if valor_dispositivo is not None:
        return {"id_dispositivo": id_dispositivo, "valor": valor_dispositivo[0]}
    else:
        return {"message": "Dispositivo no encontrado"}

@app.put("/dispositivos/{id_dispositivo}/{valor}")
async def actualizar_dispositivo(id_dispositivo: int, valor: int):
    """Actualiza un dispositivo."""
    # Actualiza el dispositivo en la base de datos con el nuevo valor
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET valor = ? WHERE id_dispositivo = ?', (valor, id_dispositivo))
    conn.commit()

    # Recupera el valor actualizado desde la base de datos
    c.execute('SELECT valor FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    nuevo_valor = c.fetchone()[0]

    return {"message": "Dispositivo actualizado correctamente", "nuevo_valor": nuevo_valor}

