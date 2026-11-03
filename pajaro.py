
import os
import random
import requests

PAJAROS = [
    {
        "nombre": "Martín pescador",
        "emoji": "🐦",
        "dato": "Puede lanzarse al agua para capturar peces con una precisión increíble.",
        "imagen": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=800"
    },
    {
        "nombre": "Búho real",
        "emoji": "🦉",
        "dato": "Puede girar la cabeza hasta unos 270 grados.",
        "imagen": "https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=800"
    },
    {
        "nombre": "Flamenco",
        "emoji": "🦩",
        "dato": "Su color rosado procede de los pigmentos de los alimentos que come.",
        "imagen": "https://images.unsplash.com/photo-1497206365907-f5e630693df0?w=800"
    },
    {
        "nombre": "Colibrí",
        "emoji": "🌺",
        "dato": "Puede quedarse suspendido en el aire mientras vuela.",
        "imagen": "https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=800"
    }
]

def publicar_pajaro():
    webhook = os.environ["DISCORD_WEBHOOK"]
    pajaro = random.choice(PAJAROS)

    mensaje = {
        "embeds": [{
            "title": f"{pajaro['emoji']} ¡Pájaro del día: {pajaro['nombre']}!",
            "description": pajaro["dato"],
            "image": {"url": pajaro["imagen"]},
            "color": 3447003,
            "footer": {"text": "🐦 Tu dosis diaria de naturaleza"}
        }]
    }

    respuesta = requests.post(webhook, json=mensaje, timeout=20)
    respuesta.raise_for_status()
    print("¡Pájaro publicado correctamente!")

if __name__ == "__main__":
    publicar_pajaro()
