
import os
import json
import random
import requests

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
    {"nombre": "Chochín común", "cientifico": "Troglodytes troglodytes", "tipo": "Residente", "habitat": "Bosques húmedos y matorrales", "comida": "Pequeños invertebrados", "dato": "Es diminuto, pero tiene un canto sorprendentemente potente."},

    {"nombre": "Alimoche común", "cientifico": "Neophron percnopterus", "tipo": "Estival", "habitat": "Cortados, montañas y campos abiertos", "comida": "Carroña, huevos y pequeños restos", "dato": "Es el buitre europeo más pequeño y tiene la cara amarilla."},
    {"nombre": "Águila pescadora", "cientifico": "Pandion haliaetus", "tipo": "Migratoria e invernante", "habitat": "Costas, embalses y grandes ríos", "comida": "Peces", "dato": "Sus patas están especialmente adaptadas para sujetar peces resbaladizos."},
    {"nombre": "Culebrera europea", "cientifico": "Circaetus gallicus", "tipo": "Estival", "habitat": "Paisajes abiertos con arbolado", "comida": "Serpientes y otros reptiles", "dato": "Está especializada en capturar serpientes."},
    {"nombre": "Aguilucho lagunero occidental", "cientifico": "Circus aeruginosus", "tipo": "Residente e invernante", "habitat": "Carrizales y humedales", "comida": "Aves, roedores y anfibios", "dato": "Vuela bajo sobre los carrizales mientras busca alimento."},
    {"nombre": "Aguilucho cenizo", "cientifico": "Circus pygargus", "tipo": "Estival", "habitat": "Cultivos y pastizales", "comida": "Roedores e insectos", "dato": "Cría con frecuencia en campos de cereal."},
    {"nombre": "Aguilucho pálido", "cientifico": "Circus cyaneus", "tipo": "Invernante", "habitat": "Campiñas, brezales y praderas", "comida": "Roedores y pequeñas aves", "dato": "En vuelo suele llevar las alas levantadas en una ligera V."},
    {"nombre": "Cernícalo primilla", "cientifico": "Falco naumanni", "tipo": "Estival", "habitat": "Pueblos, cortijos y campos abiertos", "comida": "Insectos y pequeños roedores", "dato": "Forma colonias de cría en edificios y construcciones rurales."},
    {"nombre": "Esmerejón", "cientifico": "Falco columbarius", "tipo": "Invernante y de paso", "habitat": "Llanuras y campos abiertos", "comida": "Pequeñas aves", "dato": "Es uno de los halcones más pequeños que visitan España."},
    {"nombre": "Alcotán europeo", "cientifico": "Falco subbuteo", "tipo": "Estival", "habitat": "Dehesas, bosques abiertos y humedales", "comida": "Insectos voladores y aves", "dato": "Puede capturar libélulas y aves mientras vuela."},
    {"nombre": "Búho chico", "cientifico": "Asio otus", "tipo": "Residente e invernante", "habitat": "Bosques y arboledas", "comida": "Roedores y pequeños mamíferos", "dato": "Sus penachos parecen orejas, aunque no lo son."},
    {"nombre": "Búho campestre", "cientifico": "Asio flammeus", "tipo": "Invernante y de paso", "habitat": "Marismas, praderas y campos", "comida": "Roedores", "dato": "A diferencia de muchos búhos, puede cazar a plena luz del día."},
    {"nombre": "Cárabo común", "cientifico": "Strix aluco", "tipo": "Residente", "habitat": "Bosques y parques arbolados", "comida": "Roedores y pequeños animales", "dato": "Su reclamo nocturno es uno de los sonidos clásicos del bosque."},
    {"nombre": "Garceta común", "cientifico": "Egretta garzetta", "tipo": "Residente e invernante", "habitat": "Marismas, lagunas y ríos", "comida": "Peces e invertebrados acuáticos", "dato": "Sus dedos amarillos destacan sobre sus patas oscuras."},
    {"nombre": "Garcilla bueyera", "cientifico": "Bubulcus ibis", "tipo": "Residente", "habitat": "Pastizales, campos y humedales", "comida": "Insectos y pequeños invertebrados", "dato": "A menudo sigue al ganado para capturar insectos que levanta al caminar."},
    {"nombre": "Garcilla cangrejera", "cientifico": "Ardeola ralloides", "tipo": "Estival", "habitat": "Humedales con vegetación", "comida": "Peces, anfibios e insectos", "dato": "En plumaje nupcial luce tonos dorados y blancos."},
    {"nombre": "Garceta grande", "cientifico": "Ardea alba", "tipo": "Invernante y de paso", "habitat": "Humedales y lagunas", "comida": "Peces y anfibios", "dato": "Su plumaje es completamente blanco y su tamaño es notable."},
    {"nombre": "Pato colorado", "cientifico": "Netta rufina", "tipo": "Residente e invernante", "habitat": "Lagunas y embalses", "comida": "Plantas acuáticas e invertebrados", "dato": "El macho tiene una cabeza de color castaño rojizo muy llamativa."},
    {"nombre": "Porrón europeo", "cientifico": "Aythya ferina", "tipo": "Invernante y residente", "habitat": "Lagunas y embalses", "comida": "Plantas y pequeños animales acuáticos", "dato": "Se alimenta buceando bajo la superficie."},
    {"nombre": "Porrón moñudo", "cientifico": "Aythya fuligula", "tipo": "Invernante", "habitat": "Lagos, embalses y humedales", "comida": "Moluscos y plantas acuáticas", "dato": "El macho presenta un característico pequeño moño en la nuca."},
    {"nombre": "Cerceta carretona", "cientifico": "Spatula querquedula", "tipo": "De paso y estival escasa", "habitat": "Lagunas someras", "comida": "Invertebrados acuáticos y semillas", "dato": "Es una pequeña anátida migradora de largas distancias."},
    {"nombre": "Silbón europeo", "cientifico": "Mareca penelope", "tipo": "Invernante", "habitat": "Estuarios, marismas y lagunas", "comida": "Hierbas y plantas acuáticas", "dato": "El macho emite un silbido muy reconocible."},
    {"nombre": "Ánade friso", "cientifico": "Mareca strepera", "tipo": "Residente e invernante", "habitat": "Humedales y lagunas", "comida": "Plantas acuáticas", "dato": "Su plumaje es discreto, con dibujos finos de tonos grises."},
    {"nombre": "Ánade rabudo", "cientifico": "Anas acuta", "tipo": "Invernante y de paso", "habitat": "Marismas y lagunas", "comida": "Semillas y plantas acuáticas", "dato": "Su larga cola puntiaguda da nombre a la especie."},
    {"nombre": "Tarro blanco", "cientifico": "Tadorna tadorna", "tipo": "Residente e invernante", "habitat": "Marismas y costas", "comida": "Moluscos y pequeños invertebrados", "dato": "Combina plumaje blanco, negro y castaño con un pico rojo."},
    {"nombre": "Tarro canelo", "cientifico": "Tadorna ferruginea", "tipo": "Ocasional y local", "habitat": "Lagunas y humedales", "comida": "Semillas e invertebrados", "dato": "Su plumaje anaranjado uniforme lo hace fácil de reconocer."},
    {"nombre": "Porrón pardo", "cientifico": "Aythya nyroca", "tipo": "Ocasional", "habitat": "Lagunas con vegetación", "comida": "Plantas e invertebrados acuáticos", "dato": "Es un pato buceador escaso y de distribución localizada."},
    {"nombre": "Malvasía cabeciblanca", "cientifico": "Oxyura leucocephala", "tipo": "Residente", "habitat": "Lagunas de agua dulce", "comida": "Semillas e invertebrados acuáticos", "dato": "El macho tiene un pico azul intenso en época reproductora."},
    {"nombre": "Focha común", "cientifico": "Fulica atra", "tipo": "Residente", "habitat": "Lagunas, embalses y marismas", "comida": "Plantas acuáticas e invertebrados", "dato": "Su escudete blanco sobre la frente contrasta con el plumaje oscuro."},
    {"nombre": "Gallineta común", "cientifico": "Gallinula chloropus", "tipo": "Residente", "habitat": "Ríos, estanques y humedales", "comida": "Vegetación e invertebrados", "dato": "Suele mover la cola al caminar y muestra una línea blanca en el flanco."},
    {"nombre": "Calamón común", "cientifico": "Porphyrio porphyrio", "tipo": "Residente", "habitat": "Carrizales y lagunas", "comida": "Brotes y tallos de plantas acuáticas", "dato": "Su plumaje azul violáceo y sus patas rojas son muy llamativos."},
    {"nombre": "Rascón europeo", "cientifico": "Rallus aquaticus", "tipo": "Residente e invernante", "habitat": "Carrizales y vegetación palustre", "comida": "Invertebrados y pequeños animales", "dato": "A menudo se oye antes de conseguir verlo entre la vegetación."},
    {"nombre": "Polluela pintoja", "cientifico": "Porzana porzana", "tipo": "De paso y estival escasa", "habitat": "Humedales con vegetación baja", "comida": "Invertebrados y semillas", "dato": "Es una pequeña y discreta ave de los humedales."},
    {"nombre": "Sisón común", "cientifico": "Tetrax tetrax", "tipo": "Residente y migratorio", "habitat": "Estepas y cultivos extensivos", "comida": "Plantas, semillas e insectos", "dato": "El macho muestra un llamativo diseño blanco y negro en el cuello durante el cortejo."},
    {"nombre": "Avutarda común", "cientifico": "Otis tarda", "tipo": "Residente", "habitat": "Estepas y grandes llanuras cerealistas", "comida": "Brotes, semillas e insectos", "dato": "Es una de las aves voladoras más pesadas del mundo."},
    {"nombre": "Alcaraván común", "cientifico": "Burhinus oedicnemus", "tipo": "Residente y migratorio", "habitat": "Terrenos pedregosos y cultivos", "comida": "Insectos y pequeños invertebrados", "dato": "Sus grandes ojos amarillos ayudan a reconocerlo."},
    {"nombre": "Canastera común", "cientifico": "Glareola pratincola", "tipo": "Estival", "habitat": "Marismas y campos abiertos", "comida": "Insectos voladores", "dato": "Captura insectos en vuelo como si fuera una golondrina."},
    {"nombre": "Chorlito dorado europeo", "cientifico": "Pluvialis apricaria", "tipo": "Invernante y de paso", "habitat": "Praderas y campos húmedos", "comida": "Invertebrados", "dato": "En plumaje nupcial presenta tonos dorados y negros."},
    {"nombre": "Chorlito gris", "cientifico": "Pluvialis squatarola", "tipo": "Invernante y de paso", "habitat": "Playas y estuarios", "comida": "Gusanos y pequeños invertebrados", "dato": "Es habitual observarlo en zonas intermareales durante el invierno."},
    {"nombre": "Chorlitejo grande", "cientifico": "Charadrius hiaticula", "tipo": "Invernante y de paso", "habitat": "Playas y orillas fangosas", "comida": "Pequeños invertebrados", "dato": "Tiene una banda oscura muy marcada en el pecho."},
    {"nombre": "Chorlitejo chico", "cientifico": "Charadrius dubius", "tipo": "Estival", "habitat": "Riberas y graveras", "comida": "Insectos y pequeños invertebrados", "dato": "Suele criar en orillas de grava y zonas removidas junto al agua."},
    {"nombre": "Chorlito carambolo", "cientifico": "Eudromias morinellus", "tipo": "De paso", "habitat": "Montañas y páramos durante la migración", "comida": "Invertebrados", "dato": "Es un limícola de paso poco habitual y muy atractivo."},
    {"nombre": "Correlimos tridáctilo", "cientifico": "Calidris alba", "tipo": "Invernante y de paso", "habitat": "Playas arenosas", "comida": "Pequeños invertebrados", "dato": "Corre rápidamente por la orilla siguiendo el vaivén de las olas."},
    {"nombre": "Correlimos menudo", "cientifico": "Calidris minuta", "tipo": "De paso e invernante", "habitat": "Marismas y lagunas someras", "comida": "Pequeños invertebrados", "dato": "Es uno de los limícolas más pequeños que aparecen en España."},
    {"nombre": "Correlimos zarapitín", "cientifico": "Calidris ferruginea", "tipo": "De paso", "habitat": "Marismas y salinas", "comida": "Invertebrados acuáticos", "dato": "En plumaje nupcial muestra tonos rojizos en el pecho."},
    {"nombre": "Combatiente", "cientifico": "Calidris pugnax", "tipo": "De paso e invernante", "habitat": "Humedales y praderas inundadas", "comida": "Invertebrados", "dato": "Los machos lucen grandes gorgueras durante la época de reproducción."},
    {"nombre": "Archibebe común", "cientifico": "Tringa totanus", "tipo": "Residente e invernante", "habitat": "Marismas y estuarios", "comida": "Gusanos y crustáceos", "dato": "Sus patas anaranjadas son una buena pista para identificarlo."},
    {"nombre": "Archibebe claro", "cientifico": "Tringa nebularia", "tipo": "De paso e invernante", "habitat": "Marismas y lagunas", "comida": "Peces pequeños e invertebrados", "dato": "Tiene patas verdosas y un pico ligeramente curvado hacia arriba."},
    {"nombre": "Andarríos chico", "cientifico": "Actitis hypoleucos", "tipo": "Residente e invernante", "habitat": "Ríos y arroyos", "comida": "Insectos y pequeños invertebrados", "dato": "Balancea el cuerpo y la cola cuando está posado."},
    {"nombre": "Andarríos grande", "cientifico": "Tringa ochropus", "tipo": "Invernante y de paso", "habitat": "Ríos, charcas y humedales", "comida": "Invertebrados", "dato": "Suele preferir aguas dulces y orillas arboladas."},
    {"nombre": "Vuelvepiedras común", "cientifico": "Arenaria interpres", "tipo": "Invernante y de paso", "habitat": "Costas rocosas", "comida": "Pequeños invertebrados", "dato": "Voltea piedras y algas para encontrar alimento."},
    {"nombre": "Falaropo picofino", "cientifico": "Phalaropus lobatus", "tipo": "De paso", "habitat": "Lagunas y aguas costeras", "comida": "Pequeños invertebrados acuáticos", "dato": "Durante la migración puede verse nadando y girando sobre el agua."},
    {"nombre": "Falaropo picogrueso", "cientifico": "Phalaropus fulicarius", "tipo": "De paso ocasional", "habitat": "Aguas costeras y mar abierto", "comida": "Pequeños organismos marinos", "dato": "Es un visitante poco frecuente de las costas españolas."},
    {"nombre": "Págalo grande", "cientifico": "Stercorarius skua", "tipo": "De paso e invernante", "habitat": "Mar abierto y costas", "comida": "Peces y otros animales marinos", "dato": "Persigue a otras aves marinas para conseguir parte de su alimento."},
    {"nombre": "Págalo parásito", "cientifico": "Stercorarius parasiticus", "tipo": "De paso", "habitat": "Mar abierto y costas", "comida": "Peces y alimento robado a otras aves", "dato": "Es un volador ágil que hostiga a otras aves marinas."},
    {"nombre": "Gaviota sombría", "cientifico": "Larus fuscus", "tipo": "Invernante y de paso", "habitat": "Costas, estuarios y puertos", "comida": "Peces y alimentos variados", "dato": "Sus alas oscuras contrastan con el cuerpo más claro."},
    {"nombre": "Gaviota cana", "cientifico": "Larus canus", "tipo": "Invernante ocasional", "habitat": "Costas y grandes humedales", "comida": "Peces e invertebrados", "dato": "Es una gaviota de tamaño medio que llega desde latitudes norteñas."},
    {"nombre": "Gaviota de Audouin", "cientifico": "Ichthyaetus audouinii", "tipo": "Residente y estival", "habitat": "Costas e islas mediterráneas", "comida": "Peces", "dato": "Es una especie mediterránea de gran interés para la conservación."},
    {"nombre": "Gaviota picofina", "cientifico": "Chroicocephalus genei", "tipo": "Residente y estival", "habitat": "Salinas y lagunas costeras", "comida": "Pequeños peces e invertebrados", "dato": "Tiene un pico fino y una silueta elegante."},
    {"nombre": "Pagaza piconegra", "cientifico": "Gelochelidon nilotica", "tipo": "Estival", "habitat": "Marismas y lagunas", "comida": "Insectos y pequeños vertebrados", "dato": "A diferencia de muchos charranes, captura también insectos terrestres."},
    {"nombre": "Charrancito común", "cientifico": "Sternula albifrons", "tipo": "Estival", "habitat": "Playas, salinas y lagunas", "comida": "Peces pequeños", "dato": "Es el charrán más pequeño que cría habitualmente en España."},
    {"nombre": "Fumarel común", "cientifico": "Chlidonias niger", "tipo": "De paso", "habitat": "Lagunas y humedales", "comida": "Insectos y pequeños peces", "dato": "A menudo busca alimento volando bajo sobre el agua."},
    {"nombre": "Fumarel cariblanco", "cientifico": "Chlidonias hybrida", "tipo": "Estival y de paso", "habitat": "Humedales con vegetación", "comida": "Insectos y pequeños peces", "dato": "En época reproductora muestra una cara y vientre oscuros."},
    {"nombre": "Gaviota tridáctila", "cientifico": "Rissa tridactyla", "tipo": "Invernante y de paso", "habitat": "Acantilados y mar abierto", "comida": "Peces y organismos marinos", "dato": "Cría en colonias sobre repisas de acantilados marinos."},
    {"nombre": "Pardela balear", "cientifico": "Puffinus mauretanicus", "tipo": "De paso e invernante", "habitat": "Mar abierto y costas", "comida": "Peces y calamares", "dato": "Es una especie marina endémica de las islas Baleares y muy amenazada."},
    {"nombre": "Pardela mediterránea", "cientifico": "Puffinus yelkouan", "tipo": "De paso e invernante", "habitat": "Mar Mediterráneo", "comida": "Peces y pequeños organismos marinos", "dato": "Pasa gran parte de su vida sobre el mar."},
    {"nombre": "Pardela chica", "cientifico": "Puffinus assimilis", "tipo": "Ocasional", "habitat": "Aguas oceánicas", "comida": "Pequeños peces y calamares", "dato": "Es una pequeña pardela de hábitos pelágicos."},
    {"nombre": "Pardela pichoneta", "cientifico": "Puffinus puffinus", "tipo": "De paso", "habitat": "Océano y costas", "comida": "Peces y calamares", "dato": "Regresa a tierra principalmente para reproducirse."},
    {"nombre": "Pardela capirotada", "cientifico": "Ardenna gravis", "tipo": "De paso", "habitat": "Océano Atlántico", "comida": "Peces y calamares", "dato": "Realiza desplazamientos oceánicos de gran escala."},
    {"nombre": "Paíño de Madeira", "cientifico": "Hydrobates castro", "tipo": "Residente y de paso", "habitat": "Islas y aguas oceánicas", "comida": "Pequeños organismos marinos", "dato": "Es un ave marina nocturna que suele acercarse a tierra para criar."},
    {"nombre": "Paíño boreal", "cientifico": "Oceanodroma leucorhoa", "tipo": "Ocasional y de paso", "habitat": "Mar abierto", "comida": "Plancton y pequeños organismos marinos", "dato": "Puede pasar largos periodos lejos de la costa."},
    {"nombre": "Cormorán moñudo", "cientifico": "Gulosus aristotelis", "tipo": "Residente", "habitat": "Costas rocosas e islotes", "comida": "Peces", "dato": "Suele secar sus alas en rocas después de bucear."},
    {"nombre": "Pico menor", "cientifico": "Dryobates minor", "tipo": "Residente", "habitat": "Bosques de ribera y arboledas", "comida": "Insectos y larvas", "dato": "Es el pájaro carpintero más pequeño de Europa."},
    {"nombre": "Pico mediano", "cientifico": "Leiopicus medius", "tipo": "Residente localizado", "habitat": "Robledales y bosques maduros", "comida": "Insectos y larvas", "dato": "Está muy ligado a bosques con árboles viejos y corteza rugosa."},
    {"nombre": "Torcecuello euroasiático", "cientifico": "Jynx torquilla", "tipo": "Estival e invernante escaso", "habitat": "Dehesas, huertos y arboledas", "comida": "Hormigas y larvas", "dato": "Puede girar el cuello de una forma muy llamativa cuando se siente amenazado."},
    {"nombre": "Acentor común", "cientifico": "Prunella modularis", "tipo": "Residente e invernante", "habitat": "Matorrales y jardines", "comida": "Insectos y semillas", "dato": "Suele permanecer oculto entre arbustos bajos."},
    {"nombre": "Acentor alpino", "cientifico": "Prunella collaris", "tipo": "Residente", "habitat": "Alta montaña y roquedos", "comida": "Insectos y semillas", "dato": "Vive en zonas montañosas por encima del límite del bosque."},
    {"nombre": "Alondra común", "cientifico": "Alauda arvensis", "tipo": "Residente e invernante", "habitat": "Praderas y campos", "comida": "Semillas e insectos", "dato": "Su canto de vuelo es largo y muy elaborado."},
    {"nombre": "Cogujada común", "cientifico": "Galerida cristata", "tipo": "Residente", "habitat": "Campos secos y caminos", "comida": "Semillas e insectos", "dato": "Su cresta puntiaguda suele estar visible incluso cuando está posada."},
    {"nombre": "Cogujada montesina", "cientifico": "Galerida theklae", "tipo": "Residente", "habitat": "Laderas secas y matorral mediterráneo", "comida": "Semillas e insectos", "dato": "Está especialmente asociada a terrenos pedregosos y secos."},
    {"nombre": "Terrera común", "cientifico": "Calandrella brachydactyla", "tipo": "Estival", "habitat": "Estepas y cultivos extensivos", "comida": "Semillas e insectos", "dato": "Es una pequeña alondra de espacios abiertos."},
    {"nombre": "Terrera marismeña", "cientifico": "Alaudala rufescens", "tipo": "Residente", "habitat": "Estepas y saladares", "comida": "Semillas e insectos", "dato": "Su plumaje discreto se confunde fácilmente con el suelo desnudo."},
    {"nombre": "Calandria común", "cientifico": "Melanocorypha calandra", "tipo": "Residente", "habitat": "Llanuras cerealistas y estepas", "comida": "Semillas e insectos", "dato": "Tiene manchas negras a los lados del cuello."},
    {"nombre": "Golondrina dáurica", "cientifico": "Cecropis daurica", "tipo": "Estival", "habitat": "Campos, barrancos y pueblos", "comida": "Insectos voladores", "dato": "Construye nidos de barro con una entrada tubular característica."},
    {"nombre": "Avión roquero", "cientifico": "Ptyonoprogne rupestris", "tipo": "Residente e invernante", "habitat": "Cortados y edificios", "comida": "Insectos voladores", "dato": "Puede verse volando junto a paredes rocosas incluso en invierno."},
    {"nombre": "Avión zapador", "cientifico": "Riparia riparia", "tipo": "Estival y de paso", "habitat": "Riberas arenosas y humedales", "comida": "Insectos voladores", "dato": "Excava túneles de nidificación en taludes de arena."},
    {"nombre": "Vencejo real", "cientifico": "Tachymarptis melba", "tipo": "Estival", "habitat": "Acantilados y ciudades", "comida": "Insectos voladores", "dato": "Es mucho mayor que el vencejo común y tiene el vientre blanco."},
    {"nombre": "Vencejo pálido", "cientifico": "Apus pallidus", "tipo": "Estival", "habitat": "Costas y ciudades", "comida": "Insectos voladores", "dato": "Su plumaje es más claro que el del vencejo común."},
    {"nombre": "Vencejo cafre", "cientifico": "Apus caffer", "tipo": "Estival muy localizado", "habitat": "Pueblos y zonas rocosas cálidas", "comida": "Insectos voladores", "dato": "Es un visitante reproductor escaso y localizado en el sur peninsular."},
    {"nombre": "Ruiseñor bastardo", "cientifico": "Cettia cetti", "tipo": "Residente", "habitat": "Riberas y vegetación densa", "comida": "Insectos y pequeños invertebrados", "dato": "Su potente canto suele delatarlo desde la espesura."},
    {"nombre": "Buitrón", "cientifico": "Cisticola juncidis", "tipo": "Residente", "habitat": "Praderas húmedas y cultivos", "comida": "Insectos", "dato": "Su vuelo ondulado y su reclamo repetido son muy característicos."},
    {"nombre": "Carricero común", "cientifico": "Acrocephalus scirpaceus", "tipo": "Estival", "habitat": "Carrizales", "comida": "Insectos", "dato": "Vive entre los tallos de los carrizos y resulta difícil de observar."},
    {"nombre": "Carricero tordal", "cientifico": "Acrocephalus arundinaceus", "tipo": "Estival", "habitat": "Carrizales extensos", "comida": "Insectos", "dato": "Es uno de los carriceros de mayor tamaño de Europa."},
    {"nombre": "Carricerín común", "cientifico": "Acrocephalus schoenobaenus", "tipo": "De paso", "habitat": "Carrizales y humedales", "comida": "Insectos", "dato": "Es un pequeño migrador que atraviesa España durante sus viajes."},
    {"nombre": "Buscarla unicolor", "cientifico": "Locustella luscinioides", "tipo": "Estival", "habitat": "Carrizales y marismas", "comida": "Insectos", "dato": "Su canto recuerda a un zumbido continuo."},
    {"nombre": "Zarcero políglota", "cientifico": "Hippolais polyglotta", "tipo": "Estival", "habitat": "Sotos y matorrales", "comida": "Insectos", "dato": "Su canto incluye una gran variedad de sonidos."},
    {"nombre": "Curruca capirotada", "cientifico": "Sylvia atricapilla", "tipo": "Residente e invernante", "habitat": "Bosques, parques y jardines", "comida": "Insectos y frutos", "dato": "El macho tiene una pequeña capucha negra."},
    {"nombre": "Curruca cabecinegra", "cientifico": "Curruca melanocephala", "tipo": "Residente", "habitat": "Matorral mediterráneo", "comida": "Insectos y frutos", "dato": "El macho presenta la cabeza negra y un anillo ocular rojizo."},
    {"nombre": "Curruca carrasqueña", "cientifico": "Curruca iberiae", "tipo": "Estival", "habitat": "Matorrales mediterráneos", "comida": "Insectos", "dato": "Es una curruca pequeña propia de ambientes arbustivos."},
    {"nombre": "Curruca rabilarga", "cientifico": "Curruca undata", "tipo": "Residente", "habitat": "Brezales y matorral bajo", "comida": "Insectos", "dato": "Tiene una cola larga que suele mantener levantada."},
    {"nombre": "Curruca zarcera", "cientifico": "Curruca communis", "tipo": "Estival", "habitat": "Setos y matorrales", "comida": "Insectos y frutos", "dato": "Es migradora y pasa el invierno en África."},
    {"nombre": "Curruca mosquitera", "cientifico": "Sylvia borin", "tipo": "De paso", "habitat": "Bosques húmedos y matorrales", "comida": "Insectos y frutos", "dato": "Su aspecto es sencillo y carece de marcas llamativas en la cabeza."},
    {"nombre": "Mosquitero común", "cientifico": "Phylloscopus collybita", "tipo": "Invernante y residente", "habitat": "Bosques, parques y jardines", "comida": "Pequeños insectos", "dato": "Mueve las alas y la cola con frecuencia mientras busca alimento."},
    {"nombre": "Mosquitero musical", "cientifico": "Phylloscopus trochilus", "tipo": "De paso", "habitat": "Bosques y matorrales", "comida": "Insectos", "dato": "Es un migrador de larga distancia que pasa el invierno en África."},
    {"nombre": "Mosquitero papialbo", "cientifico": "Phylloscopus bonelli", "tipo": "Estival", "habitat": "Bosques mediterráneos", "comida": "Insectos", "dato": "Su canto rápido y repetitivo es típico de los bosques secos."},
    {"nombre": "Reyezuelo listado", "cientifico": "Regulus ignicapilla", "tipo": "Residente", "habitat": "Bosques y jardines arbolados", "comida": "Pequeños insectos", "dato": "Es diminuto y luce una franja de color en la coronilla."},
    {"nombre": "Reyezuelo sencillo", "cientifico": "Regulus regulus", "tipo": "Residente e invernante", "habitat": "Pinares y bosques de montaña", "comida": "Pequeños insectos", "dato": "Es uno de los pájaros más pequeños de Europa."},
    {"nombre": "Mito común", "cientifico": "Aegithalos caudatus", "tipo": "Residente", "habitat": "Bosques, setos y parques", "comida": "Pequeños insectos", "dato": "Su cola es muy larga en proporción a su cuerpo."},
    {"nombre": "Pájaro moscón", "cientifico": "Remiz pendulinus", "tipo": "Residente e invernante", "habitat": "Riberas y carrizales", "comida": "Insectos y semillas", "dato": "Construye un nido colgante con forma de bolsa."},
    {"nombre": "Bigotudo", "cientifico": "Panurus biarmicus", "tipo": "Residente", "habitat": "Carrizales extensos", "comida": "Semillas e insectos", "dato": "El macho tiene unas marcas negras que parecen bigotes."},
    {"nombre": "Alcaudón real", "cientifico": "Lanius meridionalis", "tipo": "Residente", "habitat": "Campos abiertos y matorrales", "comida": "Insectos y pequeños vertebrados", "dato": "Puede empalar presas en espinas para almacenarlas."},
    {"nombre": "Alcaudón dorsirrojo", "cientifico": "Lanius collurio", "tipo": "Estival", "habitat": "Setos y praderas", "comida": "Insectos y pequeños vertebrados", "dato": "El macho tiene el dorso rojizo y una máscara oscura."},
    {"nombre": "Alcaudón chico", "cientifico": "Lanius minor", "tipo": "Ocasional", "habitat": "Campos abiertos con árboles", "comida": "Insectos", "dato": "Es una especie muy escasa en España."},
    {"nombre": "Chova piquirroja", "cientifico": "Pyrrhocorax pyrrhocorax", "tipo": "Residente", "habitat": "Acantilados, montañas y pueblos", "comida": "Invertebrados", "dato": "Su pico rojo y curvado es muy característico."},
    {"nombre": "Chova piquigualda", "cientifico": "Pyrrhocorax graculus", "tipo": "Residente", "habitat": "Alta montaña", "comida": "Invertebrados y semillas", "dato": "Vive en zonas alpinas y puede acercarse a refugios de montaña."},
    {"nombre": "Graja", "cientifico": "Corvus frugilegus", "tipo": "Ocasional y localizada", "habitat": "Campos agrícolas y arboledas", "comida": "Invertebrados y semillas", "dato": "Se distingue por la zona desnuda y clara de la base del pico en adultos."},
    {"nombre": "Grajilla occidental", "cientifico": "Coloeus monedula", "tipo": "Residente", "habitat": "Pueblos, ciudades y cortados", "comida": "Semillas e invertebrados", "dato": "Sus ojos claros destacan sobre la cabeza oscura."},
    {"nombre": "Corneja negra", "cientifico": "Corvus corone", "tipo": "Residente", "habitat": "Campos, bosques y ciudades", "comida": "Alimentos variados", "dato": "Es muy adaptable y puede aprovechar muchos tipos de alimento."},
    {"nombre": "Gorrión común", "cientifico": "Passer domesticus", "tipo": "Residente", "habitat": "Pueblos y ciudades", "comida": "Semillas y restos vegetales", "dato": "Está estrechamente ligado a los asentamientos humanos."},
    {"nombre": "Gorrión molinero", "cientifico": "Passer montanus", "tipo": "Residente", "habitat": "Campos, huertos y pueblos", "comida": "Semillas e insectos", "dato": "Tiene una mancha negra en la mejilla blanca."},
    {"nombre": "Gorrión chillón", "cientifico": "Petronia petronia", "tipo": "Residente", "habitat": "Pueblos de piedra y roquedos", "comida": "Semillas e insectos", "dato": "Suele criar en huecos de edificios y paredes rocosas."},
    {"nombre": "Gorrión moruno", "cientifico": "Passer hispaniolensis", "tipo": "Residente y local", "habitat": "Dehesas, humedales y pueblos", "comida": "Semillas e insectos", "dato": "Forma grandes colonias y bandos fuera de la época de cría."},
    {"nombre": "Escribano soteño", "cientifico": "Emberiza cirlus", "tipo": "Residente", "habitat": "Setos, huertos y campos arbolados", "comida": "Semillas e insectos", "dato": "El macho presenta dibujos amarillos y negros en la cabeza."},
    {"nombre": "Escribano cerillo", "cientifico": "Emberiza citrinella", "tipo": "Residente e invernante", "habitat": "Praderas y lindes de bosque", "comida": "Semillas e insectos", "dato": "El macho tiene la cabeza y el pecho amarillos."},
    {"nombre": "Escribano triguero", "cientifico": "Emberiza calandra", "tipo": "Residente", "habitat": "Campos cerealistas y pastizales", "comida": "Semillas e insectos", "dato": "Su canto suele escucharse desde cables y postes."},
    {"nombre": "Escribano montesino", "cientifico": "Emberiza cia", "tipo": "Residente", "habitat": "Laderas pedregosas y matorral", "comida": "Semillas e insectos", "dato": "Tiene un dibujo de líneas oscuras en la cabeza gris."},
    {"nombre": "Escribano palustre", "cientifico": "Emberiza schoeniclus", "tipo": "Invernante y residente localizado", "habitat": "Carrizales y humedales", "comida": "Semillas e insectos", "dato": "En invierno forma dormideros entre la vegetación palustre."},
    {"nombre": "Escribano hortelano", "cientifico": "Emberiza hortulana", "tipo": "De paso y estival escaso", "habitat": "Montañas y campos abiertos", "comida": "Semillas e insectos", "dato": "Es un migrador transahariano que aparece sobre todo durante los pasos."},
    {"nombre": "Lúgano", "cientifico": "Spinus spinus", "tipo": "Invernante y de paso", "habitat": "Bosques de coníferas y alisos", "comida": "Semillas", "dato": "Sus bandos pueden visitar árboles cargados de semillas."},
    {"nombre": "Piquituerto común", "cientifico": "Loxia curvirostra", "tipo": "Residente", "habitat": "Pinares y bosques de coníferas", "comida": "Piñones y semillas", "dato": "Las puntas cruzadas del pico le permiten extraer semillas de las piñas."},
    {"nombre": "Camachuelo común", "cientifico": "Pyrrhula pyrrhula", "tipo": "Residente e invernante", "habitat": "Bosques húmedos y jardines", "comida": "Yemas, semillas y frutos", "dato": "El macho tiene el pecho de un tono rojizo rosado."},
    {"nombre": "Picogordo", "cientifico": "Coccothraustes coccothraustes", "tipo": "Residente e invernante", "habitat": "Bosques caducifolios", "comida": "Semillas y huesos de frutos", "dato": "Su pico robusto puede romper semillas muy duras."},
    {"nombre": "Pardillo piquigualdo", "cientifico": "Linaria flavirostris", "tipo": "Invernante ocasional", "habitat": "Praderas y campos abiertos", "comida": "Semillas", "dato": "Es un visitante invernal poco común en la península."},
    {"nombre": "Camachuelo trompetero", "cientifico": "Bucanetes githagineus", "tipo": "Residente local", "habitat": "Zonas áridas y semidesérticas", "comida": "Semillas", "dato": "Está adaptado a ambientes muy secos del sureste peninsular y Canarias."},
    {"nombre": "Roquero solitario", "cientifico": "Monticola solitarius", "tipo": "Residente", "habitat": "Acantilados y pueblos de piedra", "comida": "Insectos y frutos", "dato": "El macho adulto presenta un plumaje azul oscuro."},
    {"nombre": "Roquero rojo", "cientifico": "Monticola saxatilis", "tipo": "Estival", "habitat": "Montañas y roquedos", "comida": "Insectos y frutos", "dato": "El macho combina tonos azulados y anaranjados."},
    {"nombre": "Colirrojo tizón", "cientifico": "Phoenicurus ochruros", "tipo": "Residente e invernante", "habitat": "Pueblos, roquedos y ciudades", "comida": "Insectos y pequeños frutos", "dato": "Suele agitar su cola rojiza mientras está posado."},
    {"nombre": "Colirrojo real", "cientifico": "Phoenicurus phoenicurus", "tipo": "Estival y de paso", "habitat": "Bosques abiertos y parques", "comida": "Insectos", "dato": "El macho tiene el pecho anaranjado y una máscara oscura."},
    {"nombre": "Tarabilla europea", "cientifico": "Saxicola rubicola", "tipo": "Residente", "habitat": "Matorrales, praderas y campos", "comida": "Insectos", "dato": "Suele posarse en tallos y vallas desde donde vigila el entorno."},
    {"nombre": "Tarabilla norteña", "cientifico": "Saxicola rubetra", "tipo": "De paso", "habitat": "Praderas y campos húmedos", "comida": "Insectos", "dato": "Es un migrador que atraviesa España en primavera y otoño."},
    {"nombre": "Collalba gris", "cientifico": "Oenanthe oenanthe", "tipo": "Estival y de paso", "habitat": "Montañas, pedregales y campos abiertos", "comida": "Insectos", "dato": "Su obispillo blanco destaca cuando vuela."},
    {"nombre": "Collalba rubia", "cientifico": "Oenanthe hispanica", "tipo": "Estival", "habitat": "Zonas secas y pedregosas", "comida": "Insectos", "dato": "Está adaptada a paisajes mediterráneos abiertos y cálidos."},
    {"nombre": "Collalba negra", "cientifico": "Oenanthe leucura", "tipo": "Residente", "habitat": "Roquedos y barrancos secos", "comida": "Insectos y pequeños frutos", "dato": "El adulto es casi completamente negro con la cola blanca y negra."},
    {"nombre": "Mirlo acuático europeo", "cientifico": "Cinclus cinclus", "tipo": "Residente", "habitat": "Arroyos y ríos de aguas limpias", "comida": "Larvas e invertebrados acuáticos", "dato": "Puede caminar bajo el agua para buscar alimento."},
    {"nombre": "Zorzal alirrojo", "cientifico": "Turdus iliacus", "tipo": "Invernante", "habitat": "Bosques, setos y parques", "comida": "Frutos e invertebrados", "dato": "Muestra tonos rojizos bajo las alas y en los flancos."},
    {"nombre": "Zorzal charlo", "cientifico": "Turdus viscivorus", "tipo": "Residente e invernante", "habitat": "Bosques y campos arbolados", "comida": "Frutos e invertebrados", "dato": "Consume frutos de muérdago y ayuda a dispersar sus semillas."},
    {"nombre": "Zorzal real", "cientifico": "Turdus pilaris", "tipo": "Invernante", "habitat": "Bosques, praderas y huertos", "comida": "Frutos e invertebrados", "dato": "En invierno puede formar bandos junto a otros zorzales."},
    {"nombre": "Estornino pinto", "cientifico": "Sturnus vulgaris", "tipo": "Invernante y de paso", "habitat": "Ciudades, campos y dormideros arbolados", "comida": "Insectos y frutos", "dato": "Sus bandos pueden formar grandes figuras cambiantes en el cielo."},
    {"nombre": "Tórtola europea", "cientifico": "Streptopelia turtur", "tipo": "Estival", "habitat": "Campos con setos y arbolado", "comida": "Semillas", "dato": "Es una migradora de larga distancia y su población ha sufrido un declive importante."},
    {"nombre": "Tórtola turca", "cientifico": "Streptopelia decaocto", "tipo": "Residente", "habitat": "Ciudades, pueblos y jardines", "comida": "Semillas", "dato": "Se ha expandido por gran parte de Europa durante el último siglo."},
    {"nombre": "Paloma torcaz", "cientifico": "Columba palumbus", "tipo": "Residente e invernante", "habitat": "Bosques, parques y campos", "comida": "Semillas, hojas y frutos", "dato": "Es la paloma más grande y tiene manchas blancas en el cuello."},
    {"nombre": "Paloma zurita", "cientifico": "Columba oenas", "tipo": "Residente e invernante", "habitat": "Bosques maduros y campos", "comida": "Semillas y brotes", "dato": "A diferencia de la paloma torcaz, carece de manchas blancas en el cuello."},
    {"nombre": "Perdiz roja", "cientifico": "Alectoris rufa", "tipo": "Residente", "habitat": "Campos, matorrales y cultivos", "comida": "Semillas e insectos", "dato": "Su flanco presenta un patrón muy marcado de barras blancas, negras y castañas."},
    {"nombre": "Codorniz común", "cientifico": "Coturnix coturnix", "tipo": "Estival", "habitat": "Cultivos y pastizales", "comida": "Semillas e insectos", "dato": "Su reclamo repetido se escucha a menudo entre la vegetación."},
    {"nombre": "Faisán vulgar", "cientifico": "Phasianus colchicus", "tipo": "Introducida y local", "habitat": "Campos y bosques abiertos", "comida": "Semillas e invertebrados", "dato": "El macho tiene una cola larga y plumaje muy vistoso."},
    {"nombre": "Pavo real común", "cientifico": "Pavo cristatus", "tipo": "Introducida y ornamental", "habitat": "Parques y fincas", "comida": "Semillas, frutos e insectos", "dato": "El macho despliega las plumas de la cola en forma de abanico."},
    {"nombre": "Cotorra argentina", "cientifico": "Myiopsitta monachus", "tipo": "Introducida", "habitat": "Parques y ciudades", "comida": "Semillas, frutos y brotes", "dato": "Construye grandes nidos comunales de ramas."},
    {"nombre": "Cotorra de Kramer", "cientifico": "Psittacula krameri", "tipo": "Introducida", "habitat": "Parques y jardines urbanos", "comida": "Frutos, semillas y brotes", "dato": "Tiene una cola larga y un pico rojo muy visible."},

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
    try:
        url = "https://commons.wikimedia.org/w/api.php"

        parametros = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {nombre}",
            "gsrnamespace": 6,
            "gsrlimit": 10,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 1000,
            "format": "json"
        }

        respuesta = requests.get(
            url,
            params=parametros,
            headers={"User-Agent": "PajaroDelDia/1.0"},
            timeout=20
        )
        respuesta.raise_for_status()

        paginas = respuesta.json().get("query", {}).get("pages", {})

        for pagina in paginas.values():
            imagenes = pagina.get("imageinfo", [])
            if imagenes:
                return imagenes[0].get("thumburl") or imagenes[0].get("url")

    except (requests.RequestException, ValueError):
        print("No se pudo encontrar una fotografía.")

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
    fotografia = buscar_fotografia(ave["nombre"])
    mensaje = {
        "embeds": [{
            "title": f"🐦 Ave del día: {ave['nombre']}",
            "description": (
                f"🔬 **Nombre científico:** *{ave['cientifico']}*\n"
                f"🧭 **Presencia en España:** {ave['tipo']}\n"
                f"🏡 **Hábitat:** {ave['habitat']}\n"
                f"🍽️ **Alimentación:** {ave['comida']}\n\n"
                f"💡 **Curiosidad:** {ave['dato']}"
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
