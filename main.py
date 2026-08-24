from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# =========================================================
# STATIC DOSYALAR
# =========================================================
# 'controller' ve 'cube' klasörlerinin bu dosya ile aynı dizinde olduğundan emin olun.
app.mount("/controller", StaticFiles(directory="controller", html=True),)
app.mount("/cube", StaticFiles(directory="cube", html=True),)

# =========================================================
# BAĞLANTILAR
# =========================================================
cube_clients = set()
controller_clients = set()

# =========================================================
# OYUN DURUMU
# =========================================================
game_state = {
    "player1": 0.0,
    "player2": 0.0,
}

# =========================================================
# CUBE'A DURUM GÖNDER
# =========================================================
async def send_state_to_cubes():
    message = json.dumps({
        "type": "control",
        "player1": game_state["player1"],
        "player2": game_state["player2"],
    })

    disconnected = []
    for client in cube_clients:
        try:
            await client.send_text(message)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        cube_clients.discard(client)

# =========================================================
# CUBE WEBSOCKET
# =========================================================
@app.websocket("/ws/cube")
async def cube_socket(ws: WebSocket):
    await ws.accept()
    cube_clients.add(ws)
    await send_state_to_cubes() # Bağlanınca mevcut durumu gönder

    try:
        while True:
            await ws.receive_text() # Bağlantıyı canlı tut
    except WebSocketDisconnect:
        cube_clients.discard(ws)
    except Exception:
        cube_clients.discard(ws)

# =========================================================
# CONTROLLER WEBSOCKET
# =========================================================
@app.websocket("/ws/controller")
async def controller_socket(ws: WebSocket):
    await ws.accept()
    controller_clients.add(ws)

    try:
        while True:
            raw_data = await ws.receive_text()
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                continue

            # Oyuncu Seçimi
            if data.get("type") == "join":
                player = data.get("player")
                if player in ("player1", "player2"):
                    continue # İstemci kaydedildi, devam et

            # Joystick Kontrolü
            if data.get("type") == "control":
                player = data.get("player")
                value = data.get("x")

                if player not in ("player1", "player2"):
                    continue

                try:
                    value = float(value)
                except (TypeError, ValueError):
                    continue

                value = max(-1.0, min(1.0, value))
                game_state[player] = value
                
                # Yeni konumu tüm oyun ekranlarına gönder
                await send_state_to_cubes()

    except WebSocketDisconnect:
        controller_clients.discard(ws)
    except Exception:
        controller_clients.discard(ws)
    finally:
        controller_clients.discard(ws)

# =========================================================
# ANA SAYFA
# =========================================================
@app.get("/")
def root():
    return {
        "status": "running",
        "cube_clients": len(cube_clients),
        "controller_clients": len(controller_clients),
        "player1": game_state["player1"],
        "player2": game_state["player2"],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
