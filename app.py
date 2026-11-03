from flask import Flask, render_template_string
from urllib.parse import quote
import json
import urllib.request
import urllib.error

app = Flask(__name__, static_folder="imagenes", static_url_path="/imagenes")

# ============================================================
# CATALOGO DE PRODUCTOS
# Completá los tamaños y precios cuando tengas la información.
# ============================================================

PRODUCTOS = [{
        "id": "Whey-Pro-Nutrilab",
        "nombre": "Whey Pro (Nutrilab Supplements)",
        "categoria": "Proteínas",
        "descripcion": "Proteína en polvo de alta calidad con fórmula Gourmet, ideal para el soporte muscular y la recuperación después del entrenamiento.",
        "detalle": "Aporta 40g de proteína por porción, 5.5g de BCAA y 4.5g de Glutamina. Contiene EAA y NEAA para un soporte completo. Fácil de mezclar con agua o leche. Modo de uso: Consumir 1 porción al día, preferentemente post-entrenamiento.",
        "imagen": "Whey-Pro-Nutrilab.jpg",
        "presentaciones": [
            {"tamano": "1 kg", "precio": None}, 
            {"tamano": "2 kg", "precio": None}
        ]
       },
        {
        "id": "Nervomax",
        "nombre": "Nervomax capsulas",
        "categoria": "Energía y Rendimiento",
        "descripcion": "Fórmula premium con 10 activos para mejorar tu concentración, reducir el cansancio y apoyar el sistema nervioso.",
        "detalle": "Contiene Vitaminas B12, B3 y B12. Modo de uso: Tomar 2 cápsulas al día, preferentemente antes de las principales comidas.",
        "imagen": "Nervomax.jpg",
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
    {
        "id": "Calcio-de-Ostra",
        "nombre": "calcio-ostras 500mg",
        "categoria": "Salud Ósea", 
        "descripcion": "Fuente natural de calcio de alta calidad para mantener huesos y dientes fuertes.",
        "detalle": "Contribuye al mantenimiento de huesos y dientes. Apoya el funcionamiento del organismo y el sistema inmunológico. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "calcio-ostras.jpg",
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
    {
        "id": "Carti-Calcio",
        "nombre": "Carti-Cálcio (Cartílago de Tiburón + Calcio de Ostra)",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula natural que combina cartílago de tiburón y calcio de ostra para fortalecer huesos y mejorar la flexibilidad articular.",
        "detalle": "Aporta calcio esencial para huesos fuertes y ayuda a mantener el buen funcionamiento de las articulaciones. Contribuye a la regeneración del tejido cartilaginoso. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "carti-calcio.jpg",
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
    {
        "id": "Colageno-Vitamina-C",
        "nombre": "Colágeno con Vitamina C",
        "categoria": "Belleza y Piel",
        "descripcion": "Fórmula 100% natural que mejora la elasticidad y firmeza de la piel, reduce arrugas y fortalece uñas y cabello.",
        "detalle": "Contiene colágeno y Vitamina C extra para una piel más luminosa. Hidrata desde adentro, combate la flacidez y favorece la producción de colágeno natural. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "Colageno-Vitamina-C.jpg",
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    }
    ,
        {
        "id": "Colageno-Hidrolizado-Prof",
        "nombre": "Colágeno Hidrolizado (CPure)",
        "categoria": "Belleza y Piel",
        "descripcion": "Complemento con Vitaminas A y C que apoya la salud de la piel, contribuye al cuidado del cabello y las uñas.",
        "detalle": "Fórmula 0% Azúcar, Lactosa, Gluten y Sodio. Ideal para tu rutina de bienestar diario. Contiene 150 cápsulas.",
        "imagen": "colageno-hidrolisado.jpg",
        "presentaciones": [
            {"tamano": "150 cápsulas", "precio": None}
        ]
    },
        {
        "id": "Colageno-Tipo2-Videira",
        "nombre": "Colágeno Tipo 2 + Ácido Hialurónico (Videira7)",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula avanzada con MSM, Vitaminas C y D, y Calcio. Cuidado completo para tus articulaciones y piel.",
        "detalle": "El Colágeno Tipo II no hidrolizado ayuda a mantener la estructura y función de las articulaciones. El Ácido Hialurónico auxilia en la hidratación y elasticidad de la piel. Modo de uso: Ingerir 2 cápsulas al día, preferentemente con las comidas.",
        "imagen": "colageno-tipo-2.jpg",
        "presentaciones": [
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
        {
        "id": "Curcuma-Magnesio-Colageno",
        "nombre": "Cúrcuma + Magnesio + Colágeno Tipo II",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula 100% natural que ayuda a disminuir la inflamación, aliviar el dolor articular y mejorar la movilidad.",
        "detalle": "Contiene Cúrcuma (antiinflamatorio natural), Colágeno Tipo II (protege y regenera el cartílago) y Magnesio (apoya huesos, músculos y sistema nervioso). Sin gluten, sin TACC, 0% grasas trans. Modo de uso: 2 cápsulas al día.",
        "imagen": "curcuma.jpg", 
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "100 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
        {
        "id": "Lipo-Xtreme",
        "nombre": "Lipo Xtreme (Termogénico)",
        "categoria": "Quema Grasa",
        "descripcion": "Termogénico en cápsulas que aumenta la quema de grasa, reduce el apetito e incrementa la energía.",
        "detalle": "Favorece la definición muscular y mejora el metabolismo. Contiene cafeína, té verde y aminoácidos. Modo de uso: Según indicación del entrenador o profesional.",
        "imagen": "lipo-xtreme.jpg", 
        "presentaciones": [
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
        {
        "id": "Mio-Inositol",
        "nombre": "Mio-Inositol + Cromo y Vitaminas",
        "categoria": "Salud Hormonal",
        "descripcion": "Fórmula avanzada que mejora la sensibilidad a la insulina, favorece el equilibrio hormonal y es útil en el SOP.",
        "detalle": "Contiene Mio-Inositol, Picolinato de Cromo, Zinc y Vitaminas B1, B6, D3 y K2. Ayuda a regular los ciclos menstruales, controlar el peso y la glucosa, y apoya la salud mental y cardiovascular. Modo de uso: 2 cápsulas al día.",
        "imagen": "MIO-INOSITOL.jpg", 
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "100 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
        {
        "id": "Saude-da-Mulher",
        "nombre": "Saúde da Mulher (Salud de la Mujer)",
        "categoria": "Salud Hormonal",
        "descripcion": "Suplemento integral diseñado para acompañar a la mujer en cada etapa, brindando bienestar, equilibrio y energía.",
        "detalle": "Ayuda a regular las hormonas y el ciclo menstrual. Fortalece el sistema inmunológico, aumenta la energía, contribuye a la salud ósea y muscular, y mejora la salud de la piel, cabello y uñas. Modo de uso: 2 cápsulas al día.",
        "imagen": "Saude-da-Mulher.jpg", 
        "presentaciones": [
            {"tamano": "120 cápsulas", "precio": None},
            {"tamano": "100 cápsulas", "precio": None},
            {"tamano": "60 cápsulas", "precio": None}
        ]
    },
            {
        "id": "NutriDaily-B12",
        "nombre": "NutriDaily Vitamina B12 (Masticable)",
        "categoria": "Vitaminas y Minerales",
        "descripcion": "Suplemento en comprimidos masticables sabor frutas rojas, con alto contenido de Vitamina B12 (Metilcobalamina). 100% Vegano.",
        "detalle": "Aporta energía y vitalidad, reduce el cansancio y la fatiga. Favorece el funcionamiento del sistema nervioso e inmunológico, y contribuye a la formación de glóbulos rojos. Sin azúcares ni colorantes. Modo de uso: Tomar 1 comprimido masticable al día.",
        "imagen": "NutriDaily-B12.jpg", 
        "presentaciones": [
            {"tamano": "60 comprimidos", "precio": None}
        ]
    },
            
]

WHATSAPP_NUMBER = "595981715613"

N8N_WEBHOOK_URL = "https://n8n-service-1xpn.onrender.com/webhook/6e23d744-e828-4a90-981d-c91d6b4a537d"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SUPLEMENTEX | Tu bienestar, a tu ritmo</title>

    <meta name="description"
        content="Descubrí suplementos de nutrición y entrenamiento en SUPLEMENTEX.">

    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap"
        rel="stylesheet">

    <style>
        :root {
            --fondo: #050810;
            --tarjeta: #0c1322;
            --naranja: #ff6900;
            --azul: #00cfff;
            --texto: #f4f7ff;
            --texto-secundario: #aab7cc;
            --borde: #1b2c45;
        }

        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            background: var(--fondo);
            color: var(--texto);
            font-family: 'Inter', sans-serif;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        img {
            max-width: 100%;
        }

        header {
            position: sticky;
            top: 0;
            z-index: 10;
            background: rgba(5, 8, 16, .96);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--borde);
        }

        .contenedor {
            width: min(1180px, 92%);
            margin: auto;
        }

        .barra {
            min-height: 82px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .logo {
            color: white;
            font-size: 23px;
            font-weight: 900;
            letter-spacing: 1px;
            white-space: nowrap;
        }

        .logo span {
            color: var(--azul);
        }

        nav {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        nav a {
            color: #cbd5e1;
            font-size: 14px;
            transition: color .2s;
        }

        nav a:hover {
            color: var(--azul);
        }

        .acciones-header {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .icono-header {
            color: white;
            font-size: 18px;
        }

        .icono-header:hover {
            color: var(--azul);
        }

        #contador {
            display: inline-flex;
            background: var(--azul);
            color: #031018;
            border-radius: 50%;
            min-width: 23px;
            height: 23px;
            justify-content: center;
            align-items: center;
            font-size: 12px;
            font-weight: 900;
        }

        .hero {
            padding: 75px 0;
            background:
                radial-gradient(circle at 80% 30%,
                rgba(0,207,255,.15), transparent 40%),
                radial-gradient(circle at 20% 80%,
                rgba(255,105,0,.15), transparent 40%);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 45px;
            align-items: center;
        }

        .etiqueta {
            color: var(--azul);
            font-weight: 700;
            letter-spacing: 1px;
            font-size: 13px;
        }

        h1 {
            font-size: clamp(38px, 5vw, 62px);
            line-height: 1.08;
            margin: 18px 0;
        }

        h2 {
            font-size: 30px;
            margin-top: 0;
            margin-bottom: 10px;
        }

        h3 {
            margin-top: 0;
        }

        p {
            color: var(--texto-secundario);
            line-height: 1.7;
        }

        .naranja {
            color: var(--naranja);
        }

        .boton {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 9px;
            background: var(--naranja);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 22px;
            margin-top: 12px;
            text-decoration: none;
            font-weight: 700;
            cursor: pointer;
            font-family: inherit;
            transition: .2s;
        }

        .boton:hover {
            background: #e05e00;
            transform: translateY(-2px);
        }

        .boton-secundario {
            background: #14243a;
            border: 1px solid var(--azul);
            color: var(--azul);
        }

        .boton-secundario:hover {
            background: #1b3450;
        }

        .ilustracion {
            min-height: 320px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 18px;
            background: linear-gradient(145deg, #131b2e, #090d16);
            border: 1px solid var(--borde);
            border-radius: 22px;
            padding: 25px;
        }

        .tarro {
            width: 130px;
            height: 190px;
            border-radius: 12px 12px 20px 20px;
            background: linear-gradient(90deg, #101827, #26344a, #0b101a);
            border: 2px solid #334155;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            box-shadow: 0 12px 35px #0008;
            padding: 10px;
        }

        .tarro strong {
            color: white;
            font-size: 17px;
        }

        .tarro span {
            color: var(--azul);
            font-size: 12px;
            font-weight: 800;
            margin-top: 8px;
        }

        .tarro small {
            color: #cbd5e1;
            font-size: 10px;
            margin-top: 10px;
        }

        section {
            padding: 55px 0;
        }

        .subtitulo {
            border-left: 4px solid var(--azul);
            padding-left: 13px;
            margin-bottom: 28px;
        }

        .rejilla {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 20px;
        }

        .tarjeta {
            min-width: 0;
            background: linear-gradient(155deg, #111d31, #080d18);
            border: 1px solid var(--borde);
            border-radius: 16px;
            padding: 22px;
            transition: .2s;
        }

        .tarjeta:hover {
            transform: translateY(-5px);
            border-color: var(--azul);
            box-shadow: 0 12px 30px #0005;
        }

        .icono {
            color: var(--azul);
            font-size: 32px;
            margin-bottom: 15px;
        }

        .producto-imagen {
            height: 190px;
            background: #080b12;
            border: 1px solid rgba(0,207,255,.12);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            color: var(--azul);
            font-size: 20px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 18px;
            padding: 8px;
        }

        .producto-imagen img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .precio {
            color: var(--azul);
            font-size: 19px;
            font-weight: 900;
            margin: 15px 0;
        }

        .beneficios {
            background: #0d121c;
            border-top: 1px solid var(--borde);
            border-bottom: 1px solid var(--borde);
        }

        .beneficio {
            padding: 8px;
        }

        .contacto {
            background: linear-gradient(110deg, #101b30, #111726);
            border: 1px solid var(--borde);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }

        footer {
            background: #06080d;
            border-top: 1px solid var(--borde);
            padding: 30px 0;
            text-align: center;
        }

        /* MODAL DE PRODUCTOS */

        .modal {
            display: none;
            position: fixed;
            inset: 0;
            z-index: 100;
            background: rgba(0,0,0,.82);
            justify-content: center;
            align-items: center;
            padding: 15px;
            overflow-y: auto;
        }

        .modal.activo {
            display: flex;
        }

        .modal-contenido {
            width: min(650px, 100%);
            max-height: 95vh;
            overflow-y: auto;
            background: #0c1322;
            border: 1px solid var(--azul);
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 20px 60px #000a;
            position: relative;
        }

        .cerrar-modal {
            position: absolute;
            right: 18px;
            top: 15px;
            border: none;
            background: transparent;
            color: white;
            font-size: 26px;
            cursor: pointer;
        }

        .modal-imagen {
            height: 190px;
            background: #080b12;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            margin-bottom: 20px;
            color: var(--azul);
            font-size: 23px;
            font-weight: 900;
        }

        .modal-imagen img {
            height: 100%;
            width: 100%;
            object-fit: contain;
        }

        .campo {
            margin: 18px 0;
        }

        .campo label {
            display: block;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .campo select,
        .campo input {
            width: 100%;
            padding: 13px;
            background: #080d18;
            color: white;
            border: 1px solid #30415b;
            border-radius: 9px;
            font-size: 15px;
        }

        .total-producto {
            font-size: 22px;
            color: var(--azul);
            font-weight: 900;
            margin: 20px 0;
        }

        .botones-modal {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .botones-modal button {
            flex: 1;
        }

        /* CARRITO */

        .carrito {
            margin-top: 28px;
            padding: 22px;
            background: #080d18;
            border: 1px solid var(--borde);
            border-radius: 15px;
        }

        .item-carrito {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--borde);
            padding: 14px 0;
        }

        .item-carrito:last-child {
            border-bottom: none;
        }

        .eliminar {
            background: #451b20;
            color: #ff8b8b;
            border: none;
            border-radius: 7px;
            padding: 8px 12px;
            cursor: pointer;
        }

        .cantidad-controles {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .cantidad-controles button {
            background: #14243a;
            color: var(--azul);
            border: 1px solid var(--borde);
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
        }

        @media (max-width: 850px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .rejilla {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            nav {
                gap: 12px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .barra {
                flex-wrap: wrap;
                padding: 15px 0;
            }
        }

        @media (max-width: 520px) {
            .rejilla {
                grid-template-columns: 1fr;
            }

            nav {
                width: 100%;
                order: 3;
            }

            .acciones-header {
                margin-left: auto;
            }

            .ilustracion {
                min-height: 250px;
                gap: 10px;
                padding: 12px;
            }

            .tarro {
                width: 105px;
                height: 155px;
            }

            .contacto {
                padding: 22px 14px;
            }

            .modal-contenido {
                padding: 20px 15px;
            }
        }
    </style>
</head>

<body>

<header>
    <div class="contenedor barra">

        <a class="logo" href="#inicio">
            SUPLEMENT<span>EX</span>
        </a>

        <nav aria-label="Navegación principal">
            <a href="#inicio">Inicio</a>
            <a href="#categorias">Categorías</a>
            <a href="#productos">Productos</a>
            <a href="#contacto">Contacto</a>
        </nav>

        <div class="acciones-header">
            <a class="icono-header" href="#productos">
                <i class="fa-solid fa-magnifying-glass"></i>
            </a>

            <a class="icono-header" href="#carrito">
                <i class="fa-solid fa-bag-shopping"></i>
            </a>

            <span id="contador">0</span>
        </div>

    </div>
</header>

<main>

    <!-- PORTADA -->

    <section class="hero" id="inicio">
        <div class="contenedor hero-grid">

            <div>
                <p class="etiqueta">
                    <i class="fa-solid fa-bolt"></i>
                    SUPLEMENTEX - PREMIUM SUPPLEMENTS
                </p>

                <h1>
                    Tu bienestar,<br>
                    <span class="naranja">a tu ritmo.</span>
                </h1>

                <p>
                    Suplementos de nutrición para acompañar tus objetivos,
                    con asesoramiento personalizado.
                </p>

                <a class="boton" href="#productos">
                    Ver productos
                    <i class="fa-solid fa-arrow-right"></i>
                </a>
            </div>

            <div class="ilustracion">
                <div class="tarro">
                    <strong>CREATINE</strong>
                    <span>MONOHYDRATE</span>
                </div>

                <div class="tarro" style="height:220px">
                    <strong>WHEY</strong>
                    <span>PROTEIN</span>
                    <small>SUPLEMENTEX</small>
                </div>
            </div>

        </div>
    </section>

    <!-- CATEGORIAS -->

    <section id="categorias">
        <div class="contenedor">

            <div class="subtitulo">
                <h2>Categorías principales</h2>
                <p>Encontrá el suplemento ideal para vos.</p>
            </div>

            <div class="rejilla">

                <div class="tarjeta">
                    <i class="fa-solid fa-jar icono"></i>
                    <h3>Proteínas</h3>
                    <p>Opciones para complementar tu alimentación.</p>
                </div>

                <div class="tarjeta">
                    <i class="fa-solid fa-cubes icono"></i>
                    <h3>Creatinas</h3>
                    <p>Productos para acompañar tu entrenamiento.</p>
                </div>

                <div class="tarjeta">
                    <i class="fa-solid fa-capsules icono"></i>
                    <h3>Aminoácidos</h3>
                    <p>Consultá las opciones disponibles.</p>
                </div>

                <div class="tarjeta">
                    <i class="fa-solid fa-bottle-water icono"></i>
                    <h3>Accesorios</h3>
                    <p>Artículos para tus actividades deportivas.</p>
                </div>

            </div>
        </div>
    </section>

    <!-- BENEFICIOS -->

    <section class="beneficios">
        <div class="contenedor rejilla">

            <div class="beneficio">
                <i class="fa-solid fa-shield-halved icono"></i>
                <h3>Productos</h3>
                <p>Consultá por disponibilidad y características.</p>
            </div>

            <div class="beneficio">
                <i class="fa-solid fa-truck-fast icono"></i>
                <h3>Envíos</h3>
                <p>Consultá las opciones de entrega.</p>
            </div>

            <div class="beneficio">
                <i class="fa-solid fa-headset icono"></i>
                <h3>Asesoramiento</h3>
                <p>Atención personalizada para tus consultas.</p>
            </div>

            <div class="beneficio">
                <i class="fa-solid fa-lock icono"></i>
                <h3>Atención directa</h3>
                <p>Consultá antes de realizar tu pedido.</p>
            </div>

        </div>
    </section>

    <!-- PRODUCTOS -->

    <section id="productos">
        <div class="contenedor">

            <div class="subtitulo">
                <h2>Productos destacados</h2>
                <p>Seleccioná un producto para conocer sus presentaciones.</p>
            </div>

            <div class="rejilla">

                {% for producto in productos %}

                <article class="tarjeta">

                    <div class="producto-imagen">

                        {% if producto.imagen %}
                        <img
                            src="{{ url_for('static', filename=producto.imagen) }}"
                            alt="{{ producto.nombre }}"
                            loading="lazy"
                        >
                        {% else %}
                        {{ producto.nombre }}
                        {% endif %}

                    </div>

                    <h3>{{ producto.nombre }}</h3>

                    <p>{{ producto.descripcion }}</p>

                    <div class="precio">Consultar precio</div>

                    <button class="boton"
                            type="button"
                            onclick="abrirProducto('{{ producto.id }}')">
                        Ver producto
                        <i class="fa-solid fa-arrow-right"></i>
                    </button>

                </article>

                {% endfor %}

            </div>

            <!-- CARRITO -->

            <div class="carrito" id="carrito">

                <h2>
                    <i class="fa-solid fa-bag-shopping"></i>
                    Tu selección
                </h2>

                <div id="lista-carrito">
                    <p>Todavía no seleccionaste productos.</p>
                </div>

                <h3 id="total-carrito" class="total-producto">
                    Total: A confirmar
                </h3>

                <div class="botones-modal">
                    <button class="boton"
                            onclick="enviarWhatsApp('compra')">
                        <i class="fa-brands fa-whatsapp"></i>
                        Comprar por WhatsApp
                    </button>

                    <button class="boton boton-secundario"
                            onclick="enviarWhatsApp('consulta')">
                        Consultar
                    </button>
                </div>

                <p class="nota">
                    Los precios y la disponibilidad se confirman por WhatsApp.
                </p>

            </div>

        </div>
    </section>

    <!-- CONTACTO -->

    <section id="contacto">
        <div class="contenedor">

            <div class="contacto">

                <h2>¿Necesitás orientación?</h2>

                <p>
                    Estamos para ayudarte a conocer nuestros productos
                    y resolver tus consultas.
                </p>

                <button class="boton"
                        onclick="enviarOrientacion()">
                    <i class="fa-brands fa-whatsapp"></i>
                    Necesito orientación
                </button>

            </div>

        </div>
    </section>

</main>

<footer>
    <div class="contenedor">

        <h3>SUPLEMENT<span class="naranja">EX</span></h3>

        <p>Tu bienestar, a tu ritmo.</p>
        <p>Asunción, Paraguay</p>

    </div>
</footer>

<!-- VENTANA DE DETALLES DEL PRODUCTO -->

<div class="modal" id="modal-producto">

    <div class="modal-contenido">

        <button class="cerrar-modal"
                onclick="cerrarProducto()"
                aria-label="Cerrar">
            &times;
        </button>

        <div id="modal-imagen" class="modal-imagen"></div>

        <h2 id="modal-nombre"></h2>

        <p id="modal-categoria"></p>

        <p id="modal-descripcion"></p>

        <p id="modal-detalle"></p>

        <div class="campo">

            <label for="presentacion">
                Seleccioná una presentación
            </label>

            <select id="presentacion"
                    onchange="actualizarPrecio()">
            </select>

        </div>

        <div class="campo">

            <label for="cantidad-producto">
                Cantidad
            </label>

            <input
                type="number"
                id="cantidad-producto"
                value="1"
                min="1"
                max="99"
                onchange="actualizarPrecio()"
            >

        </div>

        <div class="total-producto" id="precio-modal">
            Precio: A confirmar
        </div>

        <div class="botones-modal">

            <button class="boton"
                    onclick="agregarSeleccion()">
                <i class="fa-solid fa-cart-plus"></i>
                Agregar a mi selección
            </button>

            <button class="boton boton-secundario"
                    onclick="cerrarProducto()">
                Cancelar
            </button>

        </div>

    </div>

</div>

<script>

    // PRODUCTOS RECIBIDOS DESDE PYTHON

    const productos = {{ productos | tojson }};
    
    const WHATSAPP_NUMBER = {{ WHATSAPP_NUMBER | tojson }};
    const WHATSAPP_CONFIGURADO = true;

    let productoActual = null;
    let carrito = [];


    // FORMATO DE MONEDA

    function formatoPrecio(valor) {

        return new Intl.NumberFormat("es-PY", {
            style: "currency",
            currency: "PYG",
            maximumFractionDigits: 0
        }).format(valor);

    }


    // ABRIR DETALLE DEL PRODUCTO

    function abrirProducto(id) {

        productoActual = productos.find(
            producto => producto.id === id
        );

        if (!productoActual) {
            return;
        }

        document.getElementById("modal-nombre").textContent =
            productoActual.nombre;

        document.getElementById("modal-categoria").textContent =
            productoActual.categoria;

        document.getElementById("modal-descripcion").textContent =
            productoActual.descripcion;

        document.getElementById("modal-detalle").textContent =
            productoActual.detalle;

        const imagen = document.getElementById("modal-imagen");

        if (productoActual.imagen) {

            imagen.innerHTML = "";

            const img = document.createElement("img");

            img.src = "/imagenes/" + encodeURIComponent(
                productoActual.imagen
            );

            img.alt = productoActual.nombre;

            imagen.appendChild(img);

        } else {

            imagen.textContent = productoActual.nombre;

        }

        const selector = document.getElementById("presentacion");

        selector.innerHTML = "";

        const presentaciones = productoActual.presentaciones || [];

        presentaciones.forEach((presentacion, indice) => {

            const opcion = document.createElement("option");

            opcion.value = indice;

            if (presentacion.tamano) {

                opcion.textContent = presentacion.tamano;

            } else {

                opcion.textContent = "Presentación a confirmar";

            }

            selector.appendChild(opcion);

        });

        if (presentaciones.length === 0) {

            const opcion = document.createElement("option");

            opcion.value = "-1";
            opcion.textContent = "Presentación a confirmar";

            selector.appendChild(opcion);

        }

        document.getElementById("cantidad-producto").value = 1;

        actualizarPrecio();

        document.getElementById("modal-producto").classList.add("activo");

    }


    // CERRAR VENTANA

    function cerrarProducto() {

        document.getElementById("modal-producto").classList.remove("activo");

        productoActual = null;

    }


    // ACTUALIZAR PRECIO AUTOMATICAMENTE

    function actualizarPrecio() {

        if (!productoActual) {
            return;
        }

        const selector = document.getElementById("presentacion");

        const indice = Number(selector.value);

        const cantidad = Math.max(
            1,
            Number(document.getElementById("cantidad-producto").value) || 1
        );

        const presentacion = productoActual.presentaciones[indice];

        const precioElemento = document.getElementById("precio-modal");

        if (!presentacion || presentacion.precio === null ||
            presentacion.precio === undefined) {

            precioElemento.textContent = "Precio: A confirmar";

            return;

        }

        const total = presentacion.precio * cantidad;

        precioElemento.textContent =
            "Total: " + formatoPrecio(total);

    }


    // AGREGAR PRODUCTO AL CARRITO

    function agregarSeleccion() {

        if (!productoActual) {
            return;
        }

        const indice = Number(
            document.getElementById("presentacion").value
        );

        const presentacion =
            productoActual.presentaciones[indice] || {
                tamano: "Presentación a confirmar",
                precio: null
            };

        const cantidad = Math.max(
            1,
            Number(document.getElementById("cantidad-producto").value) || 1
        );

        const existente = carrito.find(item =>
            item.id === productoActual.id &&
            item.tamano === (presentacion.tamano || "Presentación a confirmar")
        );

        if (existente) {

            existente.cantidad += cantidad;

        } else {

            carrito.push({

                id: productoActual.id,

                nombre: productoActual.nombre,

                tamano: presentacion.tamano ||
                    "Presentación a confirmar",

                precio: presentacion.precio,

                cantidad: cantidad

            });

        }

        actualizarCarrito();

        cerrarProducto();

    }


    // MOSTRAR CARRITO

    function actualizarCarrito() {

        const lista = document.getElementById("lista-carrito");

        const contador = document.getElementById("contador");

        const totalElemento = document.getElementById("total-carrito");

        lista.innerHTML = "";

        let cantidadTotal = 0;

        let total = 0;

        let precioPendiente = false;

        if (carrito.length === 0) {

            lista.innerHTML =
                "<p>Todavía no seleccionaste productos.</p>";

            contador.textContent = "0";

            totalElemento.textContent = "Total: A confirmar";

            return;

        }

        carrito.forEach((item, indice) => {

            cantidadTotal += item.cantidad;

            const subtotal = item.precio === null
                ? null
                : item.precio * item.cantidad;

            if (subtotal === null) {

                precioPendiente = true;

            } else {

                total += subtotal;

            }

            const elemento = document.createElement("div");

            elemento.className = "item-carrito";

            const informacion = document.createElement("div");

            const nombre = document.createElement("strong");

            nombre.textContent = item.nombre;

            const detalle = document.createElement("p");

            detalle.textContent =
                item.tamano + " | Cantidad: " + item.cantidad;

            const precio = document.createElement("p");

            precio.textContent = subtotal === null
                ? "Precio a confirmar"
                : formatoPrecio(subtotal);

            informacion.appendChild(nombre);

            informacion.appendChild(detalle);

            informacion.appendChild(precio);

            const controles = document.createElement("div");

            controles.className = "cantidad-controles";

            const disminuir = document.createElement("button");

            disminuir.textContent = "-";

            disminuir.onclick = () => cambiarCantidad(indice, -1);

            const aumentar = document.createElement("button");

            aumentar.textContent = "+";

            aumentar.onclick = () => cambiarCantidad(indice, 1);

            const eliminar = document.createElement("button");

            eliminar.textContent = "Eliminar";

            eliminar.className = "eliminar";

            eliminar.onclick = () => eliminarProducto(indice);

            controles.appendChild(disminuir);

            controles.appendChild(aumentar);

            controles.appendChild(eliminar);

            elemento.appendChild(informacion);

            elemento.appendChild(controles);

            lista.appendChild(elemento);

        });

        contador.textContent = cantidadTotal;

        if (precioPendiente) {

            totalElemento.textContent =
                "Total: " + formatoPrecio(total) + " + precios a confirmar";

        } else {

            totalElemento.textContent =
                "Total: " + formatoPrecio(total);

        }

    }


    // CAMBIAR CANTIDAD DESDE EL CARRITO

    function cambiarCantidad(indice, cambio) {

        carrito[indice].cantidad += cambio;

        if (carrito[indice].cantidad <= 0) {

            carrito.splice(indice, 1);

        }

        actualizarCarrito();

    }


    // ELIMINAR PRODUCTO

    function eliminarProducto(indice) {

        carrito.splice(indice, 1);

        actualizarCarrito();

    }


    // PREPARAR MENSAJE PARA WHATSAPP

    function prepararMensaje(tipo) {

        let mensaje = "";

        if (tipo === "compra") {

            mensaje = "Hola, quiero realizar un pedido en SUPLEMENTEX.\\n\\n";

        } else {

            mensaje = "Hola, quisiera consultar sobre estos productos de SUPLEMENTEX.\\n\\n";

        }

        carrito.forEach(item => {

            mensaje +=
                "- " + item.nombre +
                "\\n  Presentación: " + item.tamano +
                "\\n  Cantidad: " + item.cantidad;

            if (item.precio !== null) {

                mensaje +=
                    "\\n  Subtotal: " +
                    formatoPrecio(item.precio * item.cantidad);

            } else {

                mensaje += "\\n  Precio: A confirmar";

            }

            mensaje += "\\n\\n";

        });

        mensaje += "Quedo atento/a. ¡Gracias!";

        return mensaje;

    }


    // ABRIR WHATSAPP

    function enviarWhatsApp(tipo) {

        if (carrito.length === 0) {

            alert("Primero agregá algún producto a tu selección.");

            return;

        }

        if (WHATSAPP_CONFIGURADO === false) {

            alert("Primero configurá tu número de WhatsApp en app.py.");

            return;

        }

        const mensaje = prepararMensaje(tipo);

        const url = "https://wa.me/" + WHATSAPP_NUMBER +
            "?text=" + encodeURIComponent(mensaje);

        window.open(url, "_blank", "noopener,noreferrer");

    }


    // ORIENTACION POR WHATSAPP

    function enviarOrientacion() {

        if (WHATSAPP_CONFIGURADO === false) {

            alert("Primero configurá tu número de WhatsApp en app.py.");

            return;

        }

        const mensaje =
            "Hola, necesito orientación sobre los productos de SUPLEMENTEX.";

            const url = "https://wa.me/" + WHATSAPP_NUMBER +
            "?text=" + encodeURIComponent(mensaje);

            const ventana = window.open(url, "_blank");

            if (!ventana) {
            alert("El navegador bloqueó la ventana. Permití las ventanas emergentes.");
            }
        }

    


    // CERRAR MODAL AL HACER CLIC FUERA

    document.getElementById("modal-producto").addEventListener(
        "click",
        function(event) {

            if (event.target === this) {

                cerrarProducto();

            }

        }
    );

</script>

</body>
</html>
"""
@app.route("/")
def home():
    
    numero_configurado = (
        WHATSAPP_NUMBER =="595981715613"
        and WHATSAPP_NUMBER.isdigit()
    )

    return render_template_string(
        HTML_TEMPLATE,
        productos=PRODUCTOS,
        WHATSAPP_NUMBER=WHATSAPP_NUMBER,
        WHATSAPP_CONFIGURADO=numero_configurado
    )


if __name__ == "__main__":

    print("SUPLEMENTEX disponible en https://suplementex.onrender.com/")

    app.run(debug=True, port=5000)
    
    
