
import os
import json
import random
import requests
import re
from html import unescape

ARCHIVO_HISTORIAL = "historial.json"

AVES = [
    {"nombre": "Águila imperial ibérica", "cientifico": "Aquila adalberti", "tipo": "Residente", "habitat": "Bosques mediterráneos", "comida": "Conejos y otras presas", "dato": "Es una de las rapaces más emblemáticas y amenazadas de la península ibérica."},
    {"nombre": "Quebrantahuesos", "cientifico": "Gypaetus barbatus", "tipo": "Residente", "habitat": "Montañas", "comida": "Huesos y restos de animales", "dato": "Es famoso por alimentarse de huesos."},
    {"nombre": "Buitre leonado", "cientifico": "Gyps fulvus", "tipo": "Residente", "habitat": "Cortados y montañas", "comida": "Carroña", "dato": "Puede recorrer grandes distancias buscando alimento."},
    {"nombre": "Buitre negro", "cientifico": "Aegypius monachus", "tipo": "Residente", "habitat": "Bosques mediterráneos", "comida": "Carroña", "dato": "Es una de las aves rapaces más grandes de Europa."},
    {"nombre": "Águila real", "cientifico": "Aquila chrysaetos", "tipo": "Residente", "habitat": "Montañas y sierras", "comida": "Mamíferos y aves", "dato": "Tiene una vista extraordinariamente aguda."},
    {"nombre": "Águila perdicera", "cientifico": "Aquila fasciata", "tipo": "Residente", "habitat": "Sierras mediterráneas", "comida": "Aves y pequeños mamíferos", "dato": "Es una excelente cazadora de aves."},
    {"nombre": "Cernícalo vulgar", "cientifico": "Falco tinnunculus", "tipo": "Residente", "habitat": "Campos y ciudades", "comida": "Insectos y pequeños roedores", "dato": "Puede quedarse suspendido en el aire mientras busca presas."},
    {"nombre": "Halcón peregrino", "cientifico": "Falco peregrinus", "tipo": "Residente", "habitat": "Acantilados y ciudades", "comida": "Otras aves", "dato": "Es conocido por su extraordinaria velocidad en picado."},
    {"nombre": "Búho real", "cientifico": "Bubo bubo", "tipo": "Residente", "habitat": "Montañas y bosques", "comida": "Mamíferos y aves", "dato": "Sus grandes ojos están adaptados a la vida nocturna."},
    {"nombre": "Lechuza común", "cientifico": "Tyto alba", "tipo": "Residente", "habitat": "Campos y edificios rurales", "comida": "Roedores", "dato": "Su rostro tiene forma de corazón."},
    {"nombre": "Mochuelo europeo", "cientifico": "Athene noctua", "tipo": "Residente", "habitat": "Olivares y campos", "comida": "Insectos y pequeños animales", "dato": "También puede estar activo durante el día."},
    {"nombre": "Autillo europeo", "cientifico": "Otus scops", "tipo": "Estival", "habitat": "Bosques y parques", "comida": "Insectos", "dato": "Su canto nocturno parece un silbido repetido."},
    {"nombre": "Cigüeña blanca", "cientifico": "Ciconia ciconia", "tipo": "Residente y estival", "habitat": "Humedales y pueblos", "comida": "Insectos y pequeños animales", "dato": "Muchas cigüeñas construyen nidos que reutilizan durante años."},
    {"nombre": "Cigüeña negra", "cientifico": "Ciconia nigra", "tipo": "Estival", "habitat": "Bosques y ríos tranquilos", "comida": "Peces y anfibios", "dato": "Es mucho más discreta que la cigüeña blanca."},
    {"nombre": "Flamenco común", "cientifico": "Phoenicopterus roseus", "tipo": "Residente e invernante", "habitat": "Lagunas y salinas", "comida": "Pequeños crustáceos y algas", "dato": "Su color rosado depende de los pigmentos de su alimentación."},
    {"nombre": "Espátula común", "cientifico": "Platalea leucorodia", "tipo": "Residente y migratoria", "habitat": "Marismas y humedales", "comida": "Pequeños peces y crustáceos", "dato": "Su pico tiene forma de espátula."},
    {"nombre": "Garza real", "cientifico": "Ardea cinerea", "tipo": "Residente e invernante", "habitat": "Ríos y humedales", "comida": "Peces y anfibios", "dato": "Puede permanecer inmóvil durante mucho tiempo esperando alimento."},
    {"nombre": "Garza imperial", "cientifico": "Ardea purpurea", "tipo": "Estival", "habitat": "Carrizales y marismas", "comida": "Peces y anfibios", "dato": "Su plumaje tiene tonos rojizos y púrpuras."},
    {"nombre": "Martinete común", "cientifico": "Nycticorax nycticorax", "tipo": "Residente y estival", "habitat": "Humedales arbolados", "comida": "Peces y pequeños animales", "dato": "Suele buscar alimento al atardecer y por la noche."},
    {"nombre": "Avetoro común", "cientifico": "Botaurus stellaris", "tipo": "Residente e invernante", "habitat": "Grandes carrizales", "comida": "Peces y anfibios", "dato": "Su canto grave puede escucharse a gran distancia."},
    {"nombre": "Morito común", "cientifico": "Plegadis falcinellus", "tipo": "Residente y migratoria", "habitat": "Marismas", "comida": "Invertebrados y pequeños animales", "dato": "Su plumaje puede mostrar reflejos metálicos."},
    {"nombre": "Ánade azulón", "cientifico": "Anas platyrhynchos", "tipo": "Residente e invernante", "habitat": "Lagos y ríos", "comida": "Plantas e invertebrados", "dato": "Es uno de los patos más conocidos de Europa."},
    {"nombre": "Cerceta común", "cientifico": "Anas crecca", "tipo": "Invernante", "habitat": "Lagunas y marismas", "comida": "Semillas e invertebrados", "dato": "Es uno de los patos más pequeños de Europa."},
    {"nombre": "Pato cuchara", "cientifico": "Spatula clypeata", "tipo": "Invernante", "habitat": "Humedales", "comida": "Pequeños organismos acuáticos", "dato": "Su pico ancho funciona como un filtro."},
    {"nombre": "Ánsar común", "cientifico": "Anser anser", "tipo": "Invernante", "habitat": "Marismas y campos", "comida": "Hierbas y semillas", "dato": "Sus bandos migratorios pueden formar grandes figuras en el cielo."},
    {"nombre": "Grulla común", "cientifico": "Grus grus", "tipo": "Invernante", "habitat": "Dehesas y humedales", "comida": "Semillas y pequeños animales", "dato": "Sus llamadas se pueden escuchar a kilómetros de distancia."},
    {"nombre": "Avoceta común", "cientifico": "Recurvirostra avosetta", "tipo": "Residente e invernante", "habitat": "Salinas y lagunas", "comida": "Pequeños invertebrados", "dato": "Su pico curvado hacia arriba es inconfundible."},
    {"nombre": "Cigüeñuela común", "cientifico": "Himantopus himantopus", "tipo": "Estival", "habitat": "Lagunas y salinas", "comida": "Invertebrados acuáticos", "dato": "Tiene unas patas extraordinariamente largas."},
    {"nombre": "Chorlitejo patinegro", "cientifico": "Anarhynchus alexandrinus", "tipo": "Residente y migratorio", "habitat": "Playas y salinas", "comida": "Pequeños invertebrados", "dato": "Sus nidos pueden encontrarse directamente sobre la arena."},
    {"nombre": "Correlimos común", "cientifico": "Calidris alpina", "tipo": "Invernante y de paso", "habitat": "Marismas y playas", "comida": "Pequeños invertebrados", "dato": "Realiza migraciones de enormes distancias."},
    {"nombre": "Aguja colinegra", "cientifico": "Limosa limosa", "tipo": "Invernante y de paso", "habitat": "Humedales y marismas", "comida": "Gusanos y pequeños invertebrados", "dato": "Su pico largo le permite buscar alimento en el barro."},
    {"nombre": "Zarapito real", "cientifico": "Numenius arquata", "tipo": "Invernante y de paso", "habitat": "Marismas y costas", "comida": "Gusanos y crustáceos", "dato": "Tiene uno de los picos más largos entre las aves limícolas."},
    {"nombre": "Charrán común", "cientifico": "Sterna hirundo", "tipo": "Estival y de paso", "habitat": "Costas y lagunas", "comida": "Peces", "dato": "Se lanza al agua para capturar peces."},
    {"nombre": "Gaviota patiamarilla", "cientifico": "Larus michahellis", "tipo": "Residente", "habitat": "Costas y ciudades", "comida": "Alimentos variados", "dato": "Es una de las gaviotas más habituales del litoral español."},
    {"nombre": "Gaviota reidora", "cientifico": "Chroicocephalus ridibundus", "tipo": "Invernante y residente", "habitat": "Humedales y ciudades", "comida": "Insectos y peces pequeños", "dato": "En verano muestra una capucha oscura."},
    {"nombre": "Alcatraz atlántico", "cientifico": "Morus bassanus", "tipo": "Invernante y de paso", "habitat": "Mar abierto y costas", "comida": "Peces", "dato": "Se zambulle desde el aire para capturar peces."},
    {"nombre": "Cormorán grande", "cientifico": "Phalacrocorax carbo", "tipo": "Residente e invernante", "habitat": "Ríos y costas", "comida": "Peces", "dato": "A menudo extiende las alas para secarlas después de bucear."},
    {"nombre": "Paíño europeo", "cientifico": "Hydrobates pelagicus", "tipo": "Estival y de paso", "habitat": "Mar abierto", "comida": "Pequeños organismos marinos", "dato": "Es una de las aves marinas más pequeñas de Europa."},
    {"nombre": "Pardela cenicienta", "cientifico": "Calonectris diomedea", "tipo": "Estival", "habitat": "Océano y acantilados", "comida": "Peces y calamares", "dato": "Puede pasar meses en mar abierto."},
    {"nombre": "Vencejo común", "cientifico": "Apus apus", "tipo": "Estival", "habitat": "Ciudades y pueblos", "comida": "Insectos voladores", "dato": "Puede pasar gran parte de su vida en el aire."},
    {"nombre": "Golondrina común", "cientifico": "Hirundo rustica", "tipo": "Estival", "habitat": "Campos y pueblos", "comida": "Insectos voladores", "dato": "Regresa a Europa desde África cada primavera."},
    {"nombre": "Avión común", "cientifico": "Delichon urbicum", "tipo": "Estival", "habitat": "Pueblos y ciudades", "comida": "Insectos voladores", "dato": "Construye nidos de barro bajo aleros y puentes."},
    {"nombre": "Abejaruco europeo", "cientifico": "Merops apiaster", "tipo": "Estival", "habitat": "Campos abiertos", "comida": "Abejas y otros insectos", "dato": "Es una de las aves más coloridas de España."},
    {"nombre": "Abubilla", "cientifico": "Upupa epops", "tipo": "Residente y estival", "habitat": "Campos y jardines", "comida": "Insectos y larvas", "dato": "Su cresta se despliega como un abanico."},
    {"nombre": "Oropéndola europea", "cientifico": "Oriolus oriolus", "tipo": "Estival", "habitat": "Bosques de ribera", "comida": "Frutas e insectos", "dato": "Su canto es aflautado y muy musical."},
    {"nombre": "Alcaudón común", "cientifico": "Lanius senator", "tipo": "Estival", "habitat": "Campos con arbustos", "comida": "Insectos y pequeños vertebrados", "dato": "Tiene un antifaz negro muy característico."},
    {"nombre": "Cuco común", "cientifico": "Cuculus canorus", "tipo": "Estival", "habitat": "Bosques y campos", "comida": "Orugas e insectos", "dato": "Pone sus huevos en nidos de otras especies."},
    {"nombre": "Ruiseñor común", "cientifico": "Luscinia megarhynchos", "tipo": "Estival", "habitat": "Zonas con vegetación densa", "comida": "Insectos y frutos", "dato": "Su canto es especialmente variado."},
    {"nombre": "Petirrojo europeo", "cientifico": "Erithacus rubecula", "tipo": "Residente e invernante", "habitat": "Bosques y jardines", "comida": "Insectos y frutos", "dato": "Su pecho anaranjado lo hace muy reconocible."},
    {"nombre": "Mirlo común", "cientifico": "Turdus merula", "tipo": "Residente", "habitat": "Bosques y jardines", "comida": "Lombrices y frutos", "dato": "Su canto se escucha con frecuencia al amanecer."},
    {"nombre": "Zorzal común", "cientifico": "Turdus philomelos", "tipo": "Residente e invernante", "habitat": "Bosques y jardines", "comida": "Frutos y pequeños invertebrados", "dato": "Puede romper caracoles contra piedras."},
    {"nombre": "Lavandera blanca", "cientifico": "Motacilla alba", "tipo": "Residente e invernante", "habitat": "Ríos y espacios abiertos", "comida": "Insectos", "dato": "Mueve constantemente su larga cola."},
    {"nombre": "Bisbita pratense", "cientifico": "Anthus pratensis", "tipo": "Invernante y de paso", "habitat": "Praderas y campos", "comida": "Insectos y semillas", "dato": "Es habitual en campos abiertos durante el invierno."},
    {"nombre": "Jilguero europeo", "cientifico": "Carduelis carduelis", "tipo": "Residente e invernante", "habitat": "Campos y jardines", "comida": "Semillas", "dato": "Su cara roja y sus alas amarillas son muy llamativas."},
    {"nombre": "Verderón común", "cientifico": "Chloris chloris", "tipo": "Residente", "habitat": "Parques y jardines", "comida": "Semillas", "dato": "Su pico fuerte le ayuda a abrir semillas."},
    {"nombre": "Pardillo común", "cientifico": "Linaria cannabina", "tipo": "Residente e invernante", "habitat": "Matorrales y campos", "comida": "Semillas", "dato": "El macho luce tonos rojizos durante la época reproductora."},
    {"nombre": "Pinzón vulgar", "cientifico": "Fringilla coelebs", "tipo": "Residente e invernante", "habitat": "Bosques y parques", "comida": "Semillas e insectos", "dato": "Su canto es uno de los más conocidos de los bosques europeos."},
    {"nombre": "Estornino negro", "cientifico": "Sturnus unicolor", "tipo": "Residente", "habitat": "Pueblos y campos", "comida": "Insectos y frutos", "dato": "Puede imitar sonidos de su entorno."},
    {"nombre": "Urraca común", "cientifico": "Pica pica", "tipo": "Residente", "habitat": "Campos y ciudades", "comida": "Alimentos variados", "dato": "Es un ave muy adaptable e inteligente."},
    {"nombre": "Arrendajo euroasiático", "cientifico": "Garrulus glandarius", "tipo": "Residente", "habitat": "Bosques", "comida": "Bellotas e insectos", "dato": "Ayuda a dispersar robles al esconder bellotas."},
    {"nombre": "Cuervo grande", "cientifico": "Corvus corax", "tipo": "Residente", "habitat": "Montañas y acantilados", "comida": "Alimentos variados", "dato": "Puede resolver problemas complejos."},
    {"nombre": "Rabilargo ibérico", "cientifico": "Cyanopica cooki", "tipo": "Residente", "habitat": "Dehesas y bosques abiertos", "comida": "Insectos y frutos", "dato": "Es una especie especialmente característica de la península ibérica."},
    {"nombre": "Carbonero común", "cientifico": "Parus major", "tipo": "Residente", "habitat": "Bosques y jardines", "comida": "Insectos y semillas", "dato": "Tiene una franja negra que recorre su pecho amarillo."},
    {"nombre": "Herrerillo común", "cientifico": "Cyanistes caeruleus", "tipo": "Residente", "habitat": "Bosques y jardines", "comida": "Insectos y semillas", "dato": "Su combinación de azul y amarillo es muy característica."},
    {"nombre": "Trepador azul", "cientifico": "Sitta europaea", "tipo": "Residente", "habitat": "Bosques maduros", "comida": "Insectos y semillas", "dato": "Puede bajar por los troncos cabeza abajo."},
    {"nombre": "Pico picapinos", "cientifico": "Dendrocopos major", "tipo": "Residente", "habitat": "Bosques", "comida": "Insectos y larvas", "dato": "Utiliza su pico para buscar alimento en la madera."},
    {"nombre": "Pito real ibérico", "cientifico": "Picus sharpei", "tipo": "Residente", "habitat": "Bosques y parques", "comida": "Hormigas", "dato": "Su lengua larga le ayuda a capturar hormigas."},
    {"nombre": "Chochín común", "cientifico": "Troglodytes troglodytes", "tipo": "Residente", "habitat": "Bosques húmedos y matorrales", "comida": "Pequeños invertebrados", "dato": "Es diminuto, pero tiene un canto sorprendentemente potente."}
]

def cargar_historial():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []

    try:
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []

def guardar_historial(historial):
    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=2)

def buscar_fotografia(nombre):
    """Busca una fotografía de un ave en Wikimedia Commons."""

    url_api = "https://commons.wikimedia.org/w/api.php"

    parametros = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f'filetype:bitmap "{nombre}" bird',
        "gsrnamespace": 6,
        "gsrlimit": 5,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": 1000
    }

    try:
        respuesta = requests.get(
            url_api,
            params=parametros,
            timeout=20
        )
        respuesta.raise_for_status()

        datos = respuesta.json()
        paginas = datos.get("query", {}).get("pages", {})

        for pagina in paginas.values():
            imagenes = pagina.get("imageinfo", [])

            if imagenes:
                info = imagenes[0]
                metadatos = info.get("extmetadata", {})

                autor_html = metadatos.get(
                    "Artist", {}
                ).get("value", "Autor desconocido")

                autor = unescape(
                    re.sub(r"<[^>]+>", "", autor_html)
                )

                licencia = metadatos.get(
                    "LicenseShortName", {}
                ).get("value", "Licencia no indicada")

                pagina_imagen = info.get("descriptionurl", "")

                return {
                    "url": info.get("thumburl") or info.get("url"),
                    "autor": autor,
                    "licencia": licencia,
                    "pagina": pagina_imagen
                }

        print("No se encontró ninguna fotografía.")
        return None

    except (requests.RequestException, ValueError) as error:
        print(f"Error al buscar la fotografía: {error}")
        return None

def publicar_ave():
    webhook = os.environ["DISCORD_WEBHOOK"]
    historial = cargar_historial()

    disponibles = [
        ave for ave in AVES
        if ave["nombre"] not in historial
    ]

    if not disponibles:
        historial = []
        disponibles = AVES.copy()

    ave = random.choice(disponibles)
    datos_foto = buscar_fotografia(ave["nombre"])

    fotografia = datos_foto["url"] if datos_foto else None
    print("DATOS DE LA FOTO:", datos_foto)
    
    mensaje = {
        "embeds": [{
            "title": f"🐦 Ave del día: {ave['nombre']}",
            "description": (
                f"🔬 **Nombre científico:** *{ave['cientifico']}*\n"
                f"🧭 **Presencia en España:** {ave['tipo']}\n"
                f"🏡 **Hábitat:** {ave['habitat']}\n"
                f"🍽️ **Alimentación:** {ave['comida']}\n\n"
                f"💡 **Curiosidad:** {ave['dato']}\n\n"
                f"\n\n📷 **Fotografía:** {datos_foto['autor'] if datos_foto else 'No disponible'}\n"
                f"📜 **Licencia:** {datos_foto['licencia'] if datos_foto else 'No disponible'}\n"
                f"🔗 **Origen:** {datos_foto['pagina'] if datos_foto else 'No disponible'}"
            ),
            "color": 3447003,
            "image": {"url": fotografia} if fotografia else {},
            "footer": {
                "text": "🇪🇸 Pájaro del Día | Aves de España"
            }
        }]
    }

    respuesta = requests.post(webhook, json=mensaje, timeout=20)
    respuesta.raise_for_status()

    historial.append(ave["nombre"])
    guardar_historial(historial)

    print(f"¡Publicado: {ave['nombre']}!")

if __name__ == "__main__":
    publicar_ave()
