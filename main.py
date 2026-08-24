from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import json
import asyncio

app = FastAPI()

# =========================================================
# STATIC DOSYALAR
# =========================================================
app.mount("/controller", StaticFiles(directory="controller", html=True))
app.mount("/cube", StaticFiles(directory="cube", html=True))

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
# CUBE'A DURUM GÖNDER (Asenkron & Performanslı)
# =========================================================
async def send_state_to_cubes():
    if not cube_clients:
        return

    message = json.dumps({
        "type": "control",
        "player1": game_state["player1"],
        "player2": game_state["player2"],
    })

    # Tüm ekranlara veriyi aynı anda (paralel) göndererek gecikmeyi sıfırlıyoruz
    tasks = [asyncio.create_task(client.send_text(message)) for client in cube_clients]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Hata veren (bağlantısı kopan) istemcileri temizliyoruz
    disconnected = [cube_clients for cube_clients, res in zip(list(cube_clients), results) if isinstance(res, Exception)]
    for client in disconnected:
        cube_clients.discard(client)

# =========================================================
# CUBE WEBSOCKET
# =========================================================
@app.websocket("/ws/cube")
async def cube_socket(ws: WebSocket):
    await ws.accept()
    cube_clients.add(ws)
    await send_state_to_cubes()

    try:
        while True:
            await ws.receive_text() # Bağlantıyı canlı tutar
    except (WebSocketDisconnect, Exception):
        pass
    finally:
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
                    continue

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

                # Değeri -1.0 ile 1.0 arasında sınırla
                value = max(-1.0, min(1.0, value))
                game_state[player] = value
                
                await send_state_to_cubes()

    except (WebSocketDisconnect, Exception):
        pass
    finally:
        # İstemci koptuğunda her halükarda listeden güvenle silinir
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
    # Localhost yerine 0.0.0.0 yerel ağ paylaşımları için en doğrusudur
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
