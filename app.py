from flask import Flask, render_template_string
from urllib.parse import quote
import json
import urllib.request
import urllib.error

app = Flask(__name__, static_folder="imagenes", static_url_path="/imagenes")


# ============================================================
# CATALOGO DE PRODUCTOS
# ============================================================ 
PRODUCTOS = [  {
        "id": "Creatina-Monohidratada-Pura",
        "nombre": "Creatina Monohidratada 100% Pura (Sabor Neutro)",
        "categoria": "Creatinas",
        "descripcion": "Creatina monohidratada de alta calidad en polvo, 100% pura y sabor neutro. Lleva tu entrenamiento al siguiente nivel aumentando tu energía, fuerza y rendimiento.",
        "detalle": "Peso líquido: 300g. Beneficios: Aumenta la fuerza y la masa muscular, mejora el rendimiento físico y la resistencia, favorece la concentración y la memoria, ayuda en la recuperación muscular después del entrenamiento e incrementa la producción de energía en las células musculares. Ideal para deportistas, fitness y personas activas. Modo de uso: Mezclar 1 medida (5g) con agua o tu bebida favorita.",
        "imagen": "Creatina-Monohidratada-Pura.jpg",
        "presentaciones": [{"tamano": "300 g (Sabor Neutro)", "precio": None}]
    },  
    {
        "id": "Testrol-Up-Next-Level",
        "nombre": "Testrol Up Next Level (Profit Laboratorios)",
        "categoria": "Salud Masculina",
        "descripcion": "Fórmula superior diseñada para apoyar la energía, la fuerza y el rendimiento físico y mental. Tu mejor versión cada día.",
        "detalle": "Super concentrado en tabletas. Ciclo de 30 días (90 tabletas). Principales componentes: 450mg de Fenogreco (energía y testosterona), 500mg de Taurina (rendimiento y resistencia), 8.86mg de Boro (equilibrio hormonal y salud ósea) y 52.8mg de L-Citrulina/Arginina (circulación, oxigenación y rendimiento). Beneficios: Aumenta la energía, favorece la masa muscular, apoya la producción natural de testosterona, mejora la concentración y fortalece el sistema inmunológico.",
        "imagen": "Testrol-Up-Next-Level.jpg",
        "presentaciones": [{"tamano": "90 Tabletas - Ciclo de 30 días", "precio": None}]
    },
    {
        "id": "Vit-C-Zinco-Profit",
        "nombre": "Vit-C + Zinco (Profit Laboratorios)",
        "categoria": "Vitaminas y Minerales",
        "descripcion": "La combinación perfecta de Vitamina C y Zinc para fortalecer tus defensas, aumentar la energía y proteger tus células del daño oxidativo.",
        "detalle": "Contiene 60 cápsulas. Cada porción aporta 1000mg de Ácido Ascórbico (Vitamina C) y 11mg de Zinc. Beneficios: Fortalece el sistema inmunológico, acción antioxidante, aumenta la energía y disminuye el cansancio, cuida la piel (favorece la producción de colágeno) y contribuye a la salud de huesos, músculos y articulaciones. Fácil de tomar.",
        "imagen": "Vit-C-Zinco-Profit.jpg",
        "presentaciones": [{"tamano": "60 Cápsulas", "precio": None}]
    }, 
    {
        "id": "Joint-Pro-Colageno-Tipo2",
        "nombre": "Joint Pro - Colágeno Tipo 2 (Profit)",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula avanzada con 40mg de Colágeno Tipo 2 y 6 Vitaminas para proteger tus articulaciones, mejorar la movilidad y fortalecer huesos, cabello y uñas.",
        "detalle": "Contiene 60 cápsulas (Peso líquido: 27g). Beneficios: Protege las articulaciones y disminuye el desgaste articular, mejora la flexibilidad y libertad de movimiento, fortalece los huesos, reduce la inflamación y alivia molestias articulares. El colágeno tipo 2 también aporta a la salud y elasticidad de la piel. Fórmula 0% Lactosa, Gluten, Azúcar y Gordura. Contiene Vitaminas A, C, D, E, B1 y B6. Modo de uso: Consumir según indicación profesional.",
        "imagen": "Joint-Pro-Colageno-Tipo2.jpg",
        "presentaciones": [{"tamano": "60 Cápsulas", "precio": None}]
    },
    {
        "id": "Whey-Protein-My-Nutrition",
        "nombre": "Whey Protein (My Nutrition) - Sabor Vainilla Caramel",
        "categoria": "Proteínas",
        "descripcion": "Proteína 100% de suero de alta calidad (Calidad Premium) con absorción rápida. Baja en carbohidratos y enriquecida con aminoácidos esenciales. Sabor Vainilla Caramel.",
        "detalle": "Presentación: 1 kg (2.2 Lb) - Rinde 25 servicios (porción de 40g). Perfil nutricional por servicio: 30g de Proteína, 6748 mg de BCAA, 5050 mg de Glutamina, 14154 mg de EAA (Aminoácidos Esenciales) y 15846 mg de NEAA. Beneficios: Aumenta y conserva la masa muscular, mejora la recuperación post-entrenamiento, es de fácil digestión y aporta aminoácidos esenciales. Sin azúcar añadida, sin gluten, bajo en grasas y cero grasas trans. Modo de uso: Mezclar 1 medida (40g) con 200-250 ml de agua o leche. Consumir 1-2 veces al día.",
        "imagen": "Whey-Protein-My-Nutrition.jpg",
        "presentaciones": [{"tamano": "1 kg (2.2 LB) - 25 Servicios - Sabor Vainilla Caramel", "precio": None}]
    },
    {
        "id": "Premium-Whey-New-Made",
        "nombre": "Premium Whey (New Made) - Sabor Vainilla",
        "categoria": "Proteínas",
        "descripcion": "Proteína de suero de alta calidad (Made in USA) que aumenta la masa muscular, mejora el rendimiento y fortalece el sistema inmunológico. Sabor Vainilla.",
        "detalle": "Presentación de 1 kg (2.2 Lb) - Rinde 25 servicios. Cada servicio (1 porción) aporta 30g de Proteína y 1,67g de BCAA. Beneficios: Aumenta la masa muscular, da energía y resistencia para entrenar mejor, fortalece el sistema inmunológico (rico en vitaminas y minerales), cuida huesos y articulaciones, y apoya la recuperación muscular. Ideal para hombres y mujeres. Modo de uso: Mezclar 1 porción con agua o leche.",
        "imagen": "Premium-Whey-New-Made.jpg",
        "presentaciones": [{"tamano": "1 kg (2.2 LB) - 25 Servicios - Sabor Vainilla", "precio": None}]
    }, 
    {
        "id": "Cuts-Powder",
        "nombre": "Cuts Powder (Quema Grasa y Nootrópico)",
        "categoria": "Quema Grasa",
        "descripcion": "Tu aliado en el entrenamiento. Fórmula avanzada en polvo que acelera el metabolismo, aumenta la energía y mejora el enfoque mental y el rendimiento.",
        "detalle": "Fórmula Metabólica, Nootrópica, Diurética y Estimulante. Beneficios: Ayuda a acelerar el metabolismo y favorece la pérdida de grasa corporal. Aumenta la energía y la resistencia. Mejora el enfoque, la concentración y la función cognitiva. Apoya la función tiroidea estimulando el metabolismo. Potencia la resistencia y la fuerza. Sin azúcar (según formulación). Presentación: 383g. Rinde varios días de uso. Modo de uso: Mezclar 1 medida con agua, ideal antes del entrenamiento.",
        "imagen": "Cuts-Powder.jpg",
        "presentaciones": [{"tamano": "383 g", "precio": None}]
    },
    {
        "id": "L-Arginine-GH-Star",
        "nombre": "L-Arginine GH (Star Nutrition) - 150g",
        "categoria": "Aminoácidos",
        "descripcion": "L-Arginina 100% pura en polvo. Fórmula de alto rendimiento diseñada para aumentar la energía, la resistencia y mejorar el flujo sanguíneo.",
        "detalle": "Contiene 38 aminoácidos. Beneficios: Aumenta la energía y la resistencia, favorece el rendimiento físico y mental, mejora la circulación sanguínea y apoya la producción de óxido nítrico (ideal para la congestión muscular). Sin gluten y sin T.A.C.C. (Sin TACC). Presentación: 150 gramos (rinde 39 servicios). Modo de uso: Mezclar 1 servicio con agua o bebida favorita.",
        "imagen": "L-Arginine-GH-Star.jpg",
        "presentaciones": [{"tamano": "150 g - 39 Servicios", "precio": None}]
    },
    {
        "id": "Creatina-Macrophytus",
        "nombre": "Creatina Monohidratada (Macrophytus) - 300g",
        "categoria": "Creatinas",
        "descripcion": "Creatina monohidratada 100% pura, sin sabor y sin aditivos. La opción más limpia para aumentar tu fuerza, energía y masa muscular.",
        "detalle": "Contenido neto: 300g. Beneficios: Aumenta la fuerza muscular para rendir más en tus entrenamientos, favorece el rendimiento físico y mental, y potencia el crecimiento y la recuperación muscular. Sin gluten, sin aditivos, sin sodio y cero azúcar. Modo de uso: Mezclar 1 medida (5g) con agua o tu bebida favorita.",
        "imagen": "Creatina-Macrophytus.jpg",
        "presentaciones": [{"tamano": "300 g", "precio": None}]
    },  
    {
        "id": "Bold-Buns-Creatine-Boost-celulitis",
        "nombre": "Bold Buns Creatine Boost-celulitis(Línea Femenina)",
        "categoria": "Creatinas",
        "descripcion": "Fórmula exclusiva para mujeres: Más músculo, menos celulitis. Combina creatina para el rendimiento con colágeno para una piel más firme y elástica. Sabor Frutilla.",
        "detalle": "Por porción: 1g de BCAA (recuperación y rendimiento), 2.5g de Colágeno en péptidos (piel más firme y elástica), 5g de Creatina (más fuerza y masa muscular) y 1g de L-Glutamina (apoya la recuperación y el sistema inmune). Ayuda a reducir la celulitis, aporta más energía y resistencia. Contiene 30 servicios. Modo de uso: Mezclar 1 porción con agua, preferentemente después del entrenamiento.",
        "imagen": "Bold-Buns-Creatine-Boost-celulitis.jpg",
        "presentaciones": [{"tamano": "30 Servicios - Sabor Frutilla", "precio": None}]
    },
    {
        "id": "Bold-Buns-Creatine-Boost",
        "nombre": "Bold Buns Creatine Boost (Línea Femenina)",
        "categoria": "Creatinas",
        "descripcion": "Fórmula exclusiva para mujeres: Más músculo, menos celulitis. Combina creatina para el rendimiento con colágeno para una piel más firme y elástica. Sabor Frutilla.",
        "detalle": "Por porción: 1g de BCAA (recuperación y rendimiento), 2.5g de Colágeno en péptidos (piel más firme y elástica), 5g de Creatina (más fuerza y masa muscular) y 1g de L-Glutamina (apoya la recuperación y el sistema inmune). Contiene 30 servicios. Modo de uso: Mezclar 1 porción con agua, preferentemente después del entrenamiento.",
        "imagen": "Bold-Buns-Creatine-Boost.jpg",
        "presentaciones": [{"tamano": "30 Servicios - Sabor Frutilla", "precio": None}]
    },
    {
        "id": "FitWhey-Protein-Generation-Fit",
        "nombre": "FitWhey Protein (Generation Fit) - The Aesthetic Protein",
        "categoria": "Proteínas",
        "descripcion": "Proteína de alta calidad (Aislado + Hidrolizado + Concentrado) diseñada para apoyar el crecimiento muscular, acelerar la recuperación y complementar una alimentación balanceada. Keto Friendly.",
        "detalle": "Por porción (30g): 24g de Proteínas, 2g de Carbohidratos, 1.5g de Grasas totales, 110 kcal. Beneficios: Aumenta y mantiene la masa muscular, favorece la recuperación post-entreno, mejora el rendimiento físico y es de fácil digestión. Sin azúcar añadida, con BCAA's naturales y fácil disolución. Disponible en 2 sabores gourmet: Maracuyá Cheesecake y Super Cookies and Cream. Contiene 30 servicios por envase.",
        "imagen": "FitWhey-Protein-Generation-Fit.jpg",
        "presentaciones": [{"tamano": "Sabor Maracuyá Cheesecake - 30 Servicios", "precio": None}, {"tamano": "Sabor Super Cookies and Cream - 30 Servicios", "precio": None}]
    },
    {
        "id": "Mega-Max-SPX",
        "nombre": "Mega Max (SPX Nutrition) - Ganador de Peso",
        "categoria": "Ganadores de Peso",
        "descripcion": "El batido de tus sueños. Suplemento nutricional completo formulado para aumentar la masa muscular, aportar energía duradera y acelerar la recuperación.",
        "detalle": "Fórmula avanzada: Proteína de alta calidad, BCAA, Creatina, Carbohidratos complejos, Vitaminas y minerales. Beneficios: Aumenta la masa muscular, aporta energía duradera, mejora la recuperación, y da más fuerza y resistencia. Presentación: 2400g (5.3 LBS) - 60 servicios de 40g. Modo de uso: Mezclar 1 medida (40g) con 250-300 ml de agua o leche. Tomar 1 a 2 veces al día (después de entrenar o entre comidas).",
        "imagen": "Mega-Max-SPX.jpg",
        "presentaciones": [{"tamano": "2400g (5.3 LBS) - Sabor Cookies & Cream", "precio": None}, {"tamano": "2400g (5.3 LBS) - Sabor Frutilla", "precio": None}]
    }, 
    {
        "id": "MuscleStar-Second-Shift",
        "nombre": "MuscleStar Second Shift (Star Nutrition) - Vainilla",
        "categoria": "Proteínas",
        "descripcion": "La proteína que trabaja tan duro como tú. Fórmula post-entreno con electrolitos, diseñada para la recuperación y el crecimiento muscular después de entrenamientos intensos.",
        "detalle": "Aporta 35g de proteína por servicio (fórmula concentrada, hidrolizada y aislada de suero lácteo). Beneficios: Recuperación muscular rápida, aumento de fuerza y rendimiento, hidratación con electrolitos, apoyo al sistema inmunológico y crecimiento de masa muscular magra. Sin azúcar añadida y baja en grasas. Sabor: Vanilla Ice Cream. Modo de uso: Consumir post-entrenamiento.",
        "imagen": "MuscleStar-Second-Shift.jpg",
        "presentaciones": [{"tamano": "2 LB (907 g) - 30 Servicios", "precio": None}]
    },
    {
        "id": "Creatina-Swork",
        "nombre": "Creatina Monohidrato (Swork Nutrition) - 250g",
        "categoria": "Creatinas",
        "descripcion": "Creatina monohidratada de calidad premium (micronizada) para potenciar tu fuerza, rendimiento y masa muscular.",
        "detalle": "Contenido neto: 250g (50 servicios aprox.). Beneficios: Aumenta la fuerza y potencia muscular, mejora el rendimiento en entrenamientos de alta intensidad y favorece el aumento de masa muscular magra. Producto SIN TACC, sin gluten, bajo en grasas y cero grasas trans. Modo de uso: Mezclar 1 medida (5g) con agua o jugo, preferentemente antes o después del entrenamiento.",
        "imagen": "Creatina-Swork-250g.jpg",
        "presentaciones": [{"tamano": "250 g (50 servicios)", "precio": None}]
    }, 
    {
        "id": "Whey-Protein-Swork",
        "nombre": "Whey Proteín (Swork Nutrition) - Sabor Vainilla",
        "categoria": "Proteínas",
        "descripcion": "Proteína de suero de alta calidad (Calidad Premium) que favorece el crecimiento y reparación muscular. Sabor Vainilla, libre de gluten.",
        "detalle": "Por porción (según dosificación): 24g de Proteína, 13g de BCAA y 0g de Azúcares. Beneficios: Favorece el crecimiento y reparación muscular, ayuda a recuperar los músculos después del entrenamiento y aporta proteína de alta calidad para una mejor definición y rendimiento. Sin TACC, sin gluten, bajo en grasas y cero grasas trans. Modo de uso: Mezclar 1 porción con agua o leche.",
        "imagen": "Whey-Protein-Swork.jpg",
        "presentaciones": [{"tamano": "908 g (2 LBS) - Sabor Vainilla", "precio": None}]
    },  
    {
        "id": "Whey-Ripped-Extreme-Racers",
        "nombre": "Whey Ripped Extreme (Racers Labs)",
        "categoria": "Proteínas",
        "descripcion": "Proteína avanzada para resultados extremos. Formulada para apoyar el crecimiento muscular, la recuperación y la definición corporal. Sabor Frutilla.",
        "detalle": "Cada porción (33g) aporta: 24g de Proteínas, 0g de Grasas Trans, 280mg de L-Carnitina y 210mg de Garcinia Cambogia. Beneficios: Desarrollo muscular, mejora del rendimiento, apoya la definición (ayuda a quemar grasa), recuperación rápida y fórmula completa con vitaminas y minerales. Endulzado con Stevia. Modo de uso: Mezclar 1 porción (33g) con 200-250 ml de agua o leche. Tomar 1 a 2 veces al día, después de entrenar o entre comidas.",
        "imagen": "Whey-Ripped-Extreme-Racers.jpg",
        "presentaciones": [{"tamano": "1 kg (2.2 LB) - Sabor Frutilla", "precio": None}]
    },
    {
        "id": "Whey-Protein-Growth",
        "nombre": "Whey Protein True Mix Isolate (+growth)",
        "categoria": "Proteínas",
        "descripcion": "Proteína de suero de leche de alta calidad (mezcla de aislado y concentrado) que garantiza fuerza real y resultados reales. Sabor chocolate extra flavor.",
        "detalle": "Fórmula con alto contenido de proteínas por porción y fuente natural de BCAA. Beneficios: Favorece el desarrollo muscular, recuperación avanzada (reduce fatiga y dolor), aporta energía, es fácil de digerir y tiene bajo en azúcar (Sugar Free). Sin azúcar añadida. Materia prima importada de USA. Ideal para musculación, definición o mantenimiento. Modo de uso: Mezclar 1 scoop (aprox. 30 g) con 200-250 ml de agua o leche fría. Consumir 1 o 2 veces al día, preferentemente después de entrenar.",
        "imagen": "Whey-Protein-Growth.jpg",
        "presentaciones": [{"tamano": "Sabor Chocolate Extra Flavor", "precio": None}]
    },
    {
        "id": "Colageno-Creatina-Natural-Suppy",
        "nombre": "Colágeno + Creatina (Natural Suppy) - Sabor Frutilla",
        "categoria": "Creatinas",
        "descripcion": "Fórmula 2 en 1 que combina la fuerza de la creatina con los beneficios del colágeno. Ideal para apoyar el rendimiento deportivo y el cuidado integral del cuerpo.",
        "detalle": "Contenido neto: 250 gramos. Beneficios: Salud articular (apoya articulaciones, tendones y ligamentos), cuidado de piel, cabello y uñas, recuperación muscular post-ejercicio, y desarrollo de fuerza y músculo. Ideal para personas que entrenan, realizan actividad física o buscan complementar su nutrición diaria. Sabor: Frutilla.",
        "imagen": "Colageno-Creatina-Natural-Suppy.jpg",
        "presentaciones": [{"tamano": "250 g (Sabor Frutilla)", "precio": None}]
    },
    {
        "id": "Creatina-Gummy-Ekobe",
        "nombre": "Creatina en Gomas Ekobé (Chocolate Belga)",
        "categoria": "Creatinas",
        "descripcion": "La creatina más deliciosa y práctica. Gomitas sabor chocolate belga que ayudan a mejorar el rendimiento físico, la fuerza y la resistencia muscular.",
        "detalle": "Aporta 3g de creatina por porción. Beneficios: Aumenta la fuerza y potencia, mejora el rendimiento y la resistencia, favorece la recuperación muscular y aporta energía para tus entrenamientos. Fácil de consumir, cero azúcar y sin gluten. Contiene 60 gomas (Edición Limitada Falcão 12). Modo de uso: Consumir según la porción indicada al día.",
        "imagen": "Creatina-Gummy-Ekobe.jpg",
        "presentaciones": [{"tamano": "60 gomas (Sabor Chocolate Belga)", "precio": None}]
    },
    {
        "id": "Creatina-Gummy",
        "nombre": "Creatina Gummy (Sabor Uva Verde)",
        "categoria": "Creatinas",
        "descripcion": "La forma más práctica y deliciosa de tomar creatina. Gomitas sabor a uva verde que aportan fuerza, energía y rendimiento en cada porción.",
        "detalle": "Contiene 30 gomitas (3G de creatina por porción). Beneficios: Aumenta la fuerza y el rendimiento en entrenamientos de alta intensidad, reduce la fatiga, mejora la función cognitiva (concentración y memoria) y apoya el desarrollo muscular. Práctica y deliciosa, sin gluten y sin azúcar. Modo de uso: Tomar 3 gomitas al día o según orientación de un profesional.",
        "imagen": "Creatina-Gummy.jpg",
        "presentaciones": [{"tamano": "30 gomitas (Sabor Uva Verde)", "precio": None}]
    },
    {
        "id": "ENA-Creatina-Colageno",
        "nombre": "Creatina + Colágeno (ENA)",
        "categoria": "Creatinas",
        "descripcion": "Fórmula 2 en 1 que combina la fuerza de la creatina con los beneficios del colágeno. Tu cuerpo más fuerte y saludable, por dentro y por fuera.",
        "detalle": "Cada porción aporta 5g de Creatina, 5g de Colágeno y 800mg de Vitaminas (30 servicios). Beneficios: Aumenta la masa muscular y el rendimiento físico. Cuida las articulaciones, huesos y cartílagos. Mejora la elasticidad de la piel, el cabello y las uñas. Reduce la fatiga y fortalece el sistema inmunológico. Sin azúcar, sin gluten, sin colorantes ni conservantes artificiales. Sabor: Limón. Modo de uso: Mezclar 1 porción con agua.",
        "imagen": "ENA-Creatina-Colageno.jpg",
        "presentaciones": [{"tamano": "30 servicios - Sabor Limón", "precio": None}]
    }, 
    {
        "id": "Whey-Protein-Body-Advance",
        "nombre": "Whey Protein Gold Line (Body Advance)",
        "categoria": "Proteínas",
        "descripcion": "Proteína de suero de leche de alta calidad con fórmula avanzada. Contiene 48g de proteína por porción, ideal para el aumento y mantenimiento de la masa muscular.",
        "detalle": "Fórmula avanzada por porción: 48g de Proteína, 9.9g de BCAA's, 7g de Glutamina y 4g de Creatina. Beneficios: Aumento y mantenimiento de masa muscular, recuperación post-entrenamiento, fortalece el sistema inmunológico, mejora el rendimiento físico y apoya la pérdida de grasa corporal. Sin azúcar añadida, sin aspartamo ni conservantes artificiales. Sabor: Vainilla. Modo de uso: Mezclar 1 porción (según indicación) con agua o leche.",
        "imagen": "Whey-Protein-Body-Advance.jpg",
        "presentaciones": [{"tamano": "900 g (Sabor Vainilla)", "precio": None}]
    }, 
    {
        "id": "ENA-Ultra-Mass",
        "nombre": "ENA Ultra Mass (Vanilla Ice Cream)",
        "categoria": "Ganadores de Peso",
        "descripcion": "Suplemento diseñado para ganar masa muscular de calidad y aumentar el peso corporal de manera efectiva. Crecé en tamaño, fuerza y rendimiento.",
        "detalle": "Combina proteínas de alto valor biológico, carbohidratos y vitaminas esenciales. Cada porción (90g) aporta 25g de proteína, 75g de carbohidratos, 399 kcal, 19 vitaminas y minerales. Beneficios: Aumenta la masa muscular, mejora la fuerza y el rendimiento, aporta energía de larga duración y apoya la recuperación muscular. Libre de gluten. Proveedor oficial de la Unión Argentina de Rugby (UAR). Modo de uso: Mezclar 1 porción con agua o leche, ideal post-entrenamiento.",
        "imagen": "ENA-Ultra-Mass.jpg",
        "presentaciones": [{"tamano": "1,5 kg (1500 g) - Sabor Vainilla", "precio": None}]
    },
    {
        "id": "ENA-Whey-Protein-TrueMade",
        "nombre": "ENA Whey Protein TrueMade (Vainilla)",
        "categoria": "Proteínas",
        "descripcion": "Proteína de alto valor biológico (mezcla de Isolado + Concentrado) diseñada para aumentar la fuerza, el músculo y el rendimiento.",
        "detalle": "Aporta 25g de proteína y 6g de BCAA por porción. Contribuye al crecimiento y mantenimiento de la masa muscular, y a una rápida recuperación post-entreno. Apoya el sistema inmunológico. Sabor: Vainilla Ice Cream. Bajo en grasas y azúcares, sin gluten y libre de TACC. Proveedor oficial de la Unión Argentina de Rugby (UAR). Modo de uso: Mezclar 1 porción (según indicación) con agua o leche.",
        "imagen": "ENA-Whey-Protein-TrueMade.jpg",
        "presentaciones": [{"tamano": "2,05 LB (930 g) - 30 Servicios", "precio": None}]
    },
    {
        "id": "Creatina-Body-Advance",
        "nombre": "Creatina Monohidrato Micronizada (Body Advance)",
        "categoria": "Creatinas",
        "descripcion": "Suplemento dietario a base de Creatina Monohidratada en polvo. Fórmula micronizada de alta pureza para máxima fuerza y mejores resultados.",
        "detalle": "Beneficios clave: Aumenta la fuerza y potencia en entrenamientos de alta intensidad. Mejora el rendimiento físico en series cortas y explosivas. Contribuye a una recuperación más rápida y favorece el aumento de masa muscular magra. Sin azúcar ni colorantes artificiales. Modo de uso: Mezclar 1 medida (aprox. 5 g) con 200-300 ml de agua o bebida favorita. Consumir antes o después del entrenamiento. Contiene 60 servicios.",
        "imagen": "Creatina-Body-Advance.jpg",
        "presentaciones": [{"tamano": "300 g", "precio": None}]
    },
    {
        "id": "Whey-Cutter-SPX",
        "nombre": "Whey Cutter (SPX Nutrition)",
        "categoria": "Proteínas",
        "descripcion": "Proteína 100% Whey con el agregado del potente CLA (quemador de grasa y reductor de colesterol malo) y endulzada con Stevia.",
        "detalle": "Beneficios: Incremento de masa muscular (alta concentración de proteínas de suero lácteo esenciales para el desarrollo y reparación). Reducción de grasa corporal (incluye CLA que ayuda a mejorar la composición corporal). La stevia actúa como hipotensor y cardiotónico, regulando la tensión arterial. Sin carbohidratos añadidos.",
        "imagen": "Whey-Cutter-SPX.jpg",
        "presentaciones": [{"tamano": "1080g", "precio": None}]
    },
    {
        "id": "LiveFem-Nutrilab",
        "nombre": "Live Fem (Multivitamínico)",
        "categoria": "Vitaminas y Minerales",
        "descripcion": "Complejo multivitamínico y antioxidante diseñado especialmente para complementar la nutrición diaria de la mujer.",
        "detalle": "Aporta una nutrición equilibrada con vitaminas, minerales y fibras. Formulado con ingredientes de alta calidad como té verde, guaraná y ginseng. Diseñado para cubrir los aspectos básicos que toda mujer necesita durante el día.",
        "imagen": "LiveFem-Nutrilab.jpg",
        "presentaciones": [{"tamano": "250mg", "precio": None}]
    },
    {
        "id": "Whey-FEM-Nutrilab",
        "nombre": "Whey FEM (Nutrilab Supplements)",
        "categoria": "Proteínas",
        "descripcion": "Proteína especialmente formulada para la mujer. Combina el soporte muscular con nutrientes para la belleza y el bienestar celular.",
        "detalle": "Aporta 40g de proteína por porción para máxima recuperación muscular. Enriquecida con 2000% VD de Biotina (para piel, cabello y uñas), 1000% VD de Ácido Fólico (soporte metabólico) y 4190 mg de Leucina (desarrollo muscular). Modo de uso: Consumir 1 porción al día, preferentemente post-entrenamiento.",
        "imagen": "Whey-FEM-Nutrilab.jpg",
        "presentaciones": [{"tamano": "1 kg", "precio": None}]
    },
    {
        "id": "Vegetal-Protein-Isolate",
        "nombre": "Vegetal Protein Isolate (Gold Nutrition)",
        "categoria": "Proteínas",
        "descripcion": "Proteína aislada de origen 100% vegetal (arveja y arroz) con sabor a vainilla. Ideal para dietas veganas y vegetarianas.",
        "detalle": "Aporta 30g de proteína por porción, está enriquecida con Vitamina B12, contiene 0% azúcar y es libre de gluten, lactosa y soja. Modo de uso: Mezclar 1 porción (según el envase) con agua o bebida vegetal.",
        "imagen": "vegetal-protein-isolate.jpg",
        "presentaciones": [{"tamano": "1 kg", "precio": None}]
    },
    {
        "id": "Whey-Pro-Nutrilab",
        "nombre": "Whey Pro (Nutrilab Supplements)",
        "categoria": "Proteínas",
        "descripcion": "Proteína en polvo de alta calidad con fórmula Gourmet, ideal para el soporte muscular y la recuperación después del entrenamiento.",
        "detalle": "Aporta 40g de proteína por porción, 5.5g de BCAA y 4.5g de Glutamina. Contiene EAA y NEAA para un soporte completo. Fácil de mezclar con agua o leche. Modo de uso: Consumir 1 porción al día, preferentemente post-entrenamiento.",
        "imagen": "Whey-Pro-Nutrilab.jpg",
        "presentaciones": [{"tamano": "1 kg", "precio": None}, {"tamano": "2 kg", "precio": None}]
    },
    {
        "id": "Nervomax",
        "nombre": "Nervomax capsulas",
        "categoria": "Energía y Rendimiento",
        "descripcion": "Fórmula premium con 10 activos para mejorar tu concentración, reducir el cansancio y apoyar el sistema nervioso.",
        "detalle": "Contiene Vitaminas B12, B3 y B12. Modo de uso: Tomar 2 cápsulas al día, preferentemente antes de las principales comidas.",
        "imagen": "Nervomax.jpg",
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Calcio-de-Ostra",
        "nombre": "calcio-ostras 500mg",
        "categoria": "Salud Ósea", 
        "descripcion": "Fuente natural de calcio de alta calidad para mantener huesos y dientes fuertes.",
        "detalle": "Contribuye al mantenimiento de huesos y dientes. Apoya el funcionamiento del organismo y el sistema inmunológico. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "calcio-ostras.jpg",
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Carti-Calcio",
        "nombre": "Carti-Cálcio (Cartílago de Tiburón + Calcio de Ostra)",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula natural que combina cartílago de tiburón y calcio de ostra para fortalecer huesos y mejorar la flexibilidad articular.",
        "detalle": "Aporta calcio esencial para huesos fuertes y ayuda a mantener el buen funcionamiento de las articulaciones. Contribuye a la regeneración del tejido cartilaginoso. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "carti-calcio.jpg",
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Colageno-Vitamina-C",
        "nombre": "Colágeno con Vitamina C",
        "categoria": "Belleza y Piel",
        "descripcion": "Fórmula 100% natural que mejora la elasticidad y firmeza de la piel, reduce arrugas y fortalece uñas y cabello.",
        "detalle": "Contiene colágeno y Vitamina C extra para una piel más luminosa. Hidrata desde adentro, combate la flacidez y favorece la producción de colágeno natural. Modo de uso: Tomar 1 a 2 cápsulas al día.",
        "imagen": "Colageno-Vitamina-C.jpg",
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Colageno-Hidrolizado-Prof",
        "nombre": "Colágeno Hidrolizado (CPure)",
        "categoria": "Belleza y Piel",
        "descripcion": "Complemento con Vitaminas A y C que apoya la salud de la piel, contribuye al cuidado del cabello y las uñas.",
        "detalle": "Fórmula 0% Azúcar, Lactosa, Gluten y Sodio. Ideal para tu rutina de bienestar diario. Contiene 150 cápsulas.",
        "imagen": "colageno-hidrolisado.jpg",
        "presentaciones": [{"tamano": "150 cápsulas", "precio": None}]
    },
    {
        "id": "Colageno-Tipo2-Videira",
        "nombre": "Colágeno Tipo 2 + Ácido Hialurónico (Videira7)",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula avanzada con MSM, Vitaminas C y D, y Calcio. Cuidado completo para tus articulaciones y piel.",
        "detalle": "El Colágeno Tipo II no hidrolizado ayuda a mantener la estructura y función de las articulaciones. El Ácido Hialurónico auxilia en la hidratación y elasticidad de la piel. Modo de uso: Ingerir 2 cápsulas al día, preferentemente con las comidas.",
        "imagen": "colageno-tipo-2.jpg",
        "presentaciones": [{"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Curcuma-Magnesio-Colageno",
        "nombre": "Cúrcuma + Magnesio + Colágeno Tipo II",
        "categoria": "Huesos y Articulaciones",
        "descripcion": "Fórmula 100% natural que ayuda a disminuir la inflamación, aliviar el dolor articular y mejorar la movilidad.",
        "detalle": "Contiene Cúrcuma (antiinflamatorio natural), Colágeno Tipo II (protege y regenera el cartílago) y Magnesio (apoya huesos, músculos y sistema nervioso). Sin gluten, sin TACC, 0% grasas trans. Modo de uso: 2 cápsulas al día.",
        "imagen": "curcuma.jpg", 
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "100 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Lipo-Xtreme",
        "nombre": "Lipo Xtreme (Termogénico)",
        "categoria": "Quema Grasa",
        "descripcion": "Termogénico en cápsulas que aumenta la quema de grasa, reduce el apetito e incrementa la energía.",
        "detalle": "Favorece la definición muscular y mejora el metabolismo. Contiene cafeína, té verde y aminoácidos. Modo de uso: Según indicación del entrenador o profesional.",
        "imagen": "lipo-xtreme.jpg", 
        "presentaciones": [{"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Mio-Inositol",
        "nombre": "Mio-Inositol + Cromo y Vitaminas",
        "categoria": "Salud Hormonal",
        "descripcion": "Fórmula avanzada que mejora la sensibilidad a la insulina, favorece el equilibrio hormonal y es útil en el SOP.",
        "detalle": "Contiene Mio-Inositol, Picolinato de Cromo, Zinc y Vitaminas B1, B6, D3 y K2. Ayuda a regular los ciclos menstruales, controlar el peso y la glucosa, y apoya la salud mental y cardiovascular. Modo de uso: 2 cápsulas al día.",
        "imagen": "MIO-INOSITOL.jpg", 
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "100 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "Saude-da-Mulher",
        "nombre": "Saúde da Mulher (Salud de la Mujer)",
        "categoria": "Salud Hormonal",
        "descripcion": "Suplemento integral diseñado para acompañar a la mujer en cada etapa, brindando bienestar, equilibrio y energía.",
        "detalle": "Ayuda a regular las hormonas y el ciclo menstrual. Fortalece el sistema inmunológico, aumenta la energía, contribuye a la salud ósea y muscular, y mejora la salud de la piel, cabello y uñas. Modo de uso: 2 cápsulas al día.",
        "imagen": "Saude-da-Mulher.jpg", 
        "presentaciones": [{"tamano": "120 cápsulas", "precio": None}, {"tamano": "100 cápsulas", "precio": None}, {"tamano": "60 cápsulas", "precio": None}]
    },
    {
        "id": "NutriDaily-B12",
        "nombre": "NutriDaily Vitamina B12 (Masticable)",
        "categoria": "Vitaminas y Minerales",
        "descripcion": "Suplemento en comprimidos masticables sabor frutas rojas, con alto contenido de Vitamina B12 (Metilcobalamina). 100% Vegano.",
        "detalle": "Aporta energía y vitalidad, reduce el cansancio y la fatiga. Favorece el funcionamiento del sistema nervioso e inmunológico, y contribuye a la formación de glóbulos rojos. Sin azúcares ni colorantes. Modo de uso: Tomar 1 comprimido masticable al día.",
        "imagen": "NutriDaily-B12.jpg", 
        "presentaciones": [{"tamano": "60 comprimidos", "precio": None}]
    }
]

WHATSAPP_NUMBER = "595981715613"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SUPLEMENTEX | Tu bienestar, a tu ritmo</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --fondo: #050810; --tarjeta: #0c1322; --naranja: #ff6900; --azul: #00cfff;
            --texto: #f4f7ff; --texto-secundario: #aab7cc; --borde: #1b2c45;
        }
        * { box-sizing: border-box; scroll-behavior: smooth; }
        body { margin: 0; background: var(--fondo); color: var(--texto); font-family: 'Inter', sans-serif; }
        a { color: inherit; text-decoration: none; }
        img { max-width: 100%; }
        header { position: sticky; top: 0; z-index: 10; background: rgba(5, 8, 16, .96); backdrop-filter: blur(12px); border-bottom: 1px solid var(--borde); }
        .contenedor { width: min(1180px, 92%); margin: auto; }
        .barra { min-height: 82px; display: flex; align-items: center; justify-content: space-between; gap: 20px; }
        .logo { color: white; font-size: 23px; font-weight: 900; letter-spacing: 1px; white-space: nowrap; }
        .logo span { color: var(--azul); }
        nav { display: flex; align-items: center; gap: 24px; }
        nav a { color: #cbd5e1; font-size: 14px; transition: color .2s; }
        nav a:hover { color: var(--azul); }
        .acciones-header { display: flex; align-items: center; gap: 12px; }
        .icono-header { color: white; font-size: 18px; }
        .icono-header:hover { color: var(--azul); }
        #contador { display: inline-flex; background: var(--azul); color: #031018; border-radius: 50%; min-width: 23px; height: 23px; justify-content: center; align-items: center; font-size: 12px; font-weight: 900; }
        
        .hero {position: relative;
            width: 100%;
            height: auto; /* Importante para que no quede espacio abajo */
            background-size: cover; }
        .etiqueta { color: var(--azul); font-weight: 700; letter-spacing: 1px; font-size: 13px; }
        h1 { font-size: clamp(38px, 5vw, 62px); line-height: 1.08; margin: 18px 0; }
        h2 { font-size: 30px; margin-top: 0; margin-bottom: 10px; }
        h3 { margin-top: 0; }
        p { color: var(--texto-secundario); line-height: 1.7; }
        .naranja { color: var(--naranja); }
        .boton { display: inline-flex; align-items: center; justify-content: center; gap: 9px; background: var(--naranja); color: white; border: none; border-radius: 10px; padding: 14px 22px; margin-top: 12px; text-decoration: none; font-weight: 700; cursor: pointer; font-family: inherit; transition: .2s; }
        .boton:hover { background: #e05e00; transform: translateY(-2px); }
        .boton-secundario { background: #14243a; border: 1px solid var(--azul); color: var(--azul); }
        .boton-secundario:hover { background: #1b3450; }
        section { padding: 55px 0; }
        .subtitulo { border-left: 4px solid var(--azul); padding-left: 13px; margin-bottom: 28px; }
        .rejilla { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }
        .tarjeta { min-width: 0; background: linear-gradient(155deg, #111d31, #080d18); border: 1px solid var(--borde); border-radius: 16px; padding: 22px; transition: .2s; }
        .tarjeta:hover { transform: translateY(-5px); border-color: var(--azul); box-shadow: 0 12px 30px #0005; }
        .icono { color: var(--azul); font-size: 32px; margin-bottom: 15px; }
        .producto-imagen { height: 190px; background: #080b12; border: 1px solid rgba(0,207,255,.12); border-radius: 12px; display: flex; align-items: center; justify-content: center; overflow: hidden; color: var(--azul); font-size: 20px; font-weight: 900; text-align: center; margin-bottom: 18px; padding: 8px; }
        .producto-imagen img { width: 100%; height: 100%; object-fit: contain; }
        .precio { color: var(--azul); font-size: 19px; font-weight: 900; margin: 15px 0; }
        .contacto { background: linear-gradient(110deg, #101b30, #111726); border: 1px solid var(--borde); border-radius: 20px; padding: 30px; text-align: center; }
        footer { background: #06080d; border-top: 1px solid var(--borde); padding: 30px 0; text-align: center; }

        .modal { display: none; position: fixed; inset: 0; z-index: 100; background: rgba(0,0,0,.82); justify-content: center; align-items: center; padding: 15px; overflow-y: auto; }
        .modal.activo { display: flex; }
        .modal-contenido { width: min(650px, 100%); max-height: 95vh; overflow-y: auto; background: #0c1322; border: 1px solid var(--azul); border-radius: 18px; padding: 25px; box-shadow: 0 20px 60px #000a; position: relative; }
        .cerrar-modal { position: absolute; right: 18px; top: 15px; border: none; background: transparent; color: white; font-size: 26px; cursor: pointer; }
        .modal-imagen { height: 190px; background: #080b12; border-radius: 12px; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 20px; color: var(--azul); font-size: 23px; font-weight: 900; }
        .modal-imagen img { height: 100%; width: 100%; object-fit: contain; }
        .campo { margin: 18px 0; }
        .campo label { display: block; margin-bottom: 8px; font-weight: 700; }
        .campo select, .campo input { width: 100%; padding: 13px; background: #080d18; color: white; border: 1px solid #30415b; border-radius: 9px; font-size: 15px; }
        .total-producto { font-size: 22px; color: var(--azul); font-weight: 900; margin: 20px 0; }
        .botones-modal { display: flex; gap: 10px; flex-wrap: wrap; }
        .botones-modal button { flex: 1; }

        .carrito { margin-top: 28px; padding: 22px; background: #080d18; border: 1px solid var(--borde); border-radius: 15px; }
        .item-carrito { display: flex; justify-content: space-between; align-items: center; gap: 12px; border-bottom: 1px solid var(--borde); padding: 14px 0; }
        .item-carrito:last-child { border-bottom: none; }
        .eliminar { background: #451b20; color: #ff8b8b; border: none; border-radius: 7px; padding: 8px 12px; cursor: pointer; }
        .cantidad-controles { display: flex; align-items: center; gap: 8px; }
        .cantidad-controles button { background: #14243a; color: var(--azul); border: 1px solid var(--borde); padding: 5px 10px; border-radius: 6px; cursor: pointer; }

        @media (max-width: 850px) {
            .rejilla { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            nav { gap: 12px; flex-wrap: wrap; justify-content: center; }
            .barra { flex-wrap: wrap; padding: 15px 0; }
        }
        @media (max-width: 520px) {
            .rejilla { grid-template-columns: 1fr; }
            nav { width: 100%; order: 3; }
            .acciones-header { margin-left: auto; }
            .modal-contenido { padding: 20px 15px; }
        }
    </style>
</head>
<body>
<!-- 1. BARRA SUPERIOR (Con el diseño de tu foto) -->
<header style="background: #0e1624; padding: 0;">
    <div class="contenedor" style="display: flex; justify-content: space-between; align-items: center; min-height: 70px;">
        <!-- Logo -->
        <a href="#inicio" style="display: flex; align-items: center;">
            <img src="/imagenes/logo-suplementex2.png" alt="Logo" style="height: 80px;">
        </a>
        <!-- Menú -->
        <nav style="display: flex; gap: 25px; align-items: center;">
            <a href="#inicio" style="color: #fff; font-size: 14px; text-decoration: none; border-bottom: 2px solid #d4af37; padding-bottom: 5px;">
                <i class="fa-solid fa-house" style="color: #d4af37; margin-right: 5px;"></i> Inicio
            </a>
            <a href="#productos" style="color: #fff; font-size: 14px; text-decoration: none;">
                <i class="fa-solid fa-lock" style="color: #d4af37; margin-right: 5px;"></i> Productos <i class="fa-solid fa-chevron-down" style="font-size: 10px;"></i>
            </a>
            <a href="#contacto" style="color: #fff; font-size: 14px; text-decoration: none;">
                <i class="fa-solid fa-circle-question" style="color: #d4af37; margin-right: 5px;"></i> Contacto
            </a>
            <a href="#contacto" style="color: #fff; font-size: 14px; text-decoration: none;">
                <i class="fa-solid fa-circle-exclamation" style="color: #d4af37; margin-right: 5px;"></i> Nosotros
            </a>
        </nav>
        <!-- Iconos -->
        <div style="display: flex; gap: 15px; align-items: center;">
            <a href="#productos" style="color: #fff; font-size: 18px;"><i class="fa-solid fa-magnifying-glass"></i></a>
            <a href="#carrito" style="color: #fff; font-size: 18px; position: relative;">
                <i class="fa-solid fa-bag-shopping"></i>
                <span id="contador" style="background: #00bfff; color: #000; border-radius: 50%; width: 18px; height: 18px; display: flex; justify-content: center; align-items: center; font-size: 10px; font-weight: bold; position: absolute; top: -5px; right: -8px;">0</span>
            </a>
        </div>
    </div>
</header>

<main>
    <!-- 1. PORTADA -->
    <section id="inicio" style="position: relative; text-align: center; padding-bottom: 20px;">
        <img src="/imagenes/suplementex.jpg" alt="Portada" style="width: 100%; height: auto; display: block;">
        
        <!-- BOTÓN DORADO -->
        <div style="margin-top: -25px; position: relative; z-index: 10;">
            <a href="#productos" style="display: inline-block; background: linear-gradient(180deg, #f9d976 0%, #d4af37 100%); color: #000; font-weight: 900; font-size: 16px; padding: 12px 35px; border-radius: 50px; text-decoration: none; box-shadow: 0 5px 15px rgba(0,0,0,0.6); border: 2px solid #fff3c4;">
                <i class="fa-solid fa-cart-shopping"></i> Ver Productos
            </a>
        </div>
    </section>

    <!-- 2. BARRA DE BENEFICIOS -->
    <section style="background: #0a0f18; padding: 30px 0; border-top: 1px solid #1b2c45; border-bottom: 1px solid #1b2c45;">
        <div class="contenedor" style="display: grid; grid-template-columns: repeat(4, 1fr); text-align: center;">
            <div>
                <i class="fa-solid fa-shield-halved" style="color: #d4af37; font-size: 35px; margin-bottom: 10px;"></i>
                <h3 style="color: #fff; font-size: 16px; margin: 0;">Compra Segura</h3>
                <p style="color: #aab7cc; font-size: 12px; margin: 5px 0 0;">Tus datos protegidos</p>
            </div>
            <div>
                <i class="fa-solid fa-truck-fast" style="color: #d4af37; font-size: 35px; margin-bottom: 10px;"></i>
                <h3 style="color: #fff; font-size: 16px; margin: 0;">Envíos a todo el País</h3>
                <p style="color: #aab7cc; font-size: 12px; margin: 5px 0 0;">Rápido y confiable</p>
            </div>
            <div>
                <i class="fa-solid fa-headset" style="color: #d4af37; font-size: 35px; margin-bottom: 10px;"></i>
                <h3 style="color: #fff; font-size: 16px; margin: 0;">Asesoramiento</h3>
                <p style="color: #aab7cc; font-size: 12px; margin: 5px 0 0;">Estamos para ayudarte</p>
            </div>
            <div>
                <i class="fa-solid fa-star" style="color: #d4af37; font-size: 35px; margin-bottom: 10px;"></i>
                <h3 style="color: #fff; font-size: 16px; margin: 0;">Calidad Garantizada</h3>
                <p style="color: #aab7cc; font-size: 12px; margin: 5px 0 0;">Resultados reales</p>
            </div>
        </div>
    </section>

    <!-- 3. CATEGORÍAS (Las tarjetas de colores) -->
    <section id="categorias" style="padding-top: 30px;">
        <div class="contenedor">
            <div class="subtitulo">
                <h2>Categorías principales</h2>
                <p>Encontrá el suplemento ideal para vos.</p>
            </div>
            <div class="rejilla">
                <div class="tarjeta" onclick="filtrarCategoria('Proteínas')" style="cursor: pointer;">
                    <i class="fa-solid fa-jar icono"></i><h3>Proteínas</h3><p>Opciones para complementar tu alimentación.</p>
                </div>
                <div class="tarjeta" onclick="filtrarCategoria('Creatinas')" style="cursor: pointer;">
                    <i class="fa-solid fa-cubes icono"></i><h3>Creatinas</h3><p>Productos para acompañar tu entrenamiento.</p>
                </div>
                <div class="tarjeta" onclick="filtrarCategoria('Aminoácidos')" style="cursor: pointer;">
                    <i class="fa-solid fa-capsules icono"></i><h3>Aminoácidos</h3><p>Consultá las opciones disponibles.</p>
                </div>
                <div class="tarjeta" onclick="filtrarCategoria('Todos')" style="cursor: pointer; border-color: var(--naranja);">
                    <i class="fa-solid fa-list icono" style="color: var(--naranja);"></i><h3>Ver Todos</h3><p>Mostrar el catálogo completo.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. PRODUCTOS (¡Aquí vuelven a aparecer!) -->
    <section id="productos">
        <div class="contenedor">
            <div class="subtitulo">
                <h2>Productos destacados</h2>
                <p>Seleccioná un producto para conocer sus presentaciones.</p>
            </div>
            <div class="rejilla" id="lista-productos">
                {% for producto in productos %}
                <article class="tarjeta">
                    <div class="producto-imagen">
                        {% if producto.imagen %}
                        <img src="{{ url_for('static', filename=producto.imagen) }}" alt="{{ producto.nombre }}" loading="lazy">
                        {% else %}
                        {{ producto.nombre }}
                        {% endif %}
                    </div>
                    <h3>{{ producto.nombre }}</h3>
                    <p>{{ producto.descripcion }}</p>
                    <div class="precio">Consultar precio</div>
                    <button class="boton" type="button" onclick="abrirProducto('{{ producto.id }}')">
                        Ver producto <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </article>
                {% endfor %}
            </div>

            <!-- 5. CARRITO -->
            <div class="carrito" id="carrito">
                <h2><i class="fa-solid fa-bag-shopping"></i> Tu selección</h2>
                <div id="lista-carrito"><p>Todavía no seleccionaste productos.</p></div>
                <h3 id="total-carrito" class="total-producto">Total: A confirmar</h3>
                <div class="botones-modal">
                    <button type="button" class="boton" onclick="enviarWhatsApp('compra')">
                        <i class="fa-brands fa-whatsapp"></i> Comprar por WhatsApp
                    </button>
                    <button type="button" class="boton boton-secundario" onclick="enviarWhatsApp('consulta')">Consultar</button>
                </div>
                <p class="nota">Los precios y la disponibilidad se confirman por WhatsApp.</p>
            </div>
        </div>
    </section>

    <!-- 6. CONTACTO -->
    <section id="contacto">
        <div class="contenedor">
            <div class="contacto">
                <h2>¿Necesitás orientación?</h2>
                <p>Estamos para ayudarte a conocer nuestros productos y resolver tus consultas.</p>
                <button type="button" class="boton" onclick="enviarOrientacion()">
                    <i class="fa-brands fa-whatsapp"></i> Necesito orientación
                </button>
            </div>
        </div>
    </section>
</main>

<footer>
    <div class="contenedor" style="text-align: center; padding: 20px 0;">
        <h3>SUPLEMENT<span style="color: #d4af37;">EX</span></h3>
        <p style="color: #aab7cc; font-size: 12px;">Tu bienestar, a tu ritmo.</p>
    </div>
</footer>

<!-- VENTANA DE DETALLES DEL PRODUCTO (Modal) -->
<div class="modal" id="modal-producto">
    <div class="modal-contenido">
        <button class="cerrar-modal" onclick="cerrarModal()">&times;</button>
        <div class="modal-imagen" id="modal-imagen"></div>
        <h2 id="modal-nombre"></h2>
        <p id="modal-categoria" style="color: var(--azul); font-weight: 700; margin-top: -10px;"></p>
        <p id="modal-descripcion"></p>
        <div class="campo">
            <label for="modal-presentacion">Elegí una presentación:</label>
            <select id="modal-presentacion" onchange="actualizarPrecioModal()"></select>
        </div>
        <div class="campo">
            <label for="modal-cantidad">Cantidad:</label>
            <input type="number" id="modal-cantidad" value="1" min="1">
        </div>
        <div id="modal-detalle" style="font-size: 14px; color: #aab7cc; background: #080d18; padding: 15px; border-radius: 10px; margin: 15px 0; line-height: 1.6;"></div>
        <div class="total-producto" id="modal-total">Consultar precio</div>
        <div class="botones-modal">
            <button type="button" class="boton" onclick="agregarAlCarrito()">
                <i class="fa-solid fa-cart-plus"></i> Agregar
            </button>
            <button type="button" class="boton boton-secundario" onclick="consultarProductoWhatsApp()">
                <i class="fa-brands fa-whatsapp"></i> Consultar
            </button>
        </div>
    </div>
</div>

<!-- BOTÓN FLOTANTE -->
<a href="https://wa.me/{{ WHATSAPP_NUMBER }}" target="_blank" class="whatsapp-flotante" title="Escríbenos por WhatsApp" style="position: fixed; bottom: 25px; right: 25px; width: 60px; height: 60px; background: #25D366; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 6px 20px rgba(37, 211, 102, .5); z-index: 99; transition: transform .2s;">
    <i class="fa-brands fa-whatsapp"></i>
</a>

<script>
    const WHATSAPP_NUMBER = "{{ WHATSAPP_NUMBER }}";
    const PRODUCTOS = {{ productos|tojson }};
    let productoActual = null;
    let carrito = JSON.parse(localStorage.getItem('suplementex_carrito') || '[]');

    function abrirProducto(id) {
        const producto = PRODUCTOS.find(p => p.id === id);
        if (!producto) return;
        productoActual = producto;

        document.getElementById('modal-imagen').innerHTML = producto.imagen
            ? `<img src="/imagenes/${producto.imagen}" alt="${producto.nombre}">`
            : producto.nombre;
        document.getElementById('modal-nombre').textContent = producto.nombre;
        document.getElementById('modal-categoria').textContent = producto.categoria;
        document.getElementById('modal-descripcion').textContent = producto.descripcion;
        document.getElementById('modal-detalle').textContent = producto.detalle || '';
        document.getElementById('modal-cantidad').value = 1;

        const select = document.getElementById('modal-presentacion');
        select.innerHTML = '';
        producto.presentaciones.forEach((pres, i) => {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = pres.tamano + (pres.precio ? ` - ${pres.precio}` : '');
            select.appendChild(opt);
        });

        actualizarPrecioModal();
        document.getElementById('modal-producto').classList.add('activo');
    }

    function cerrarModal() {
        document.getElementById('modal-producto').classList.remove('activo');
    }

    function actualizarPrecioModal() {
        const idx = document.getElementById('modal-presentacion').value;
        const pres = productoActual.presentaciones[idx];
        document.getElementById('modal-total').textContent = pres.precio ? `${pres.precio}` : 'Consultar precio';
    }

    function agregarAlCarrito() {
        const idx = document.getElementById('modal-presentacion').value;
        const pres = productoActual.presentaciones[idx];
        const cantidad = parseInt(document.getElementById('modal-cantidad').value) || 1;

        const itemExistente = carrito.find(i => i.id === productoActual.id && i.presentacion === pres.tamano);
        if (itemExistente) {
            itemExistente.cantidad += cantidad;
        } else {
            carrito.push({
                id: productoActual.id,
                nombre: productoActual.nombre,
                presentacion: pres.tamano,
                precio: pres.precio || 'Consultar',
                cantidad: cantidad
            });
        }

        localStorage.setItem('suplementex_carrito', JSON.stringify(carrito));
        cerrarModal();
        renderCarrito();
        alert('✅ Producto agregado al carrito');
    }

    function renderCarrito() {
        const lista = document.getElementById('lista-carrito');
        const contador = document.getElementById('contador');

        if (carrito.length === 0) {
            lista.innerHTML = '<p>Todavía no seleccionaste productos.</p>';
            contador.textContent = '0';
            return;
        }

        lista.innerHTML = carrito.map((item, i) => `
            <div class="item-carrito">
                <div style="flex: 1;">
                    <strong>${item.nombre}</strong><br>
                    <small style="color: #aab7cc;">${item.presentacion}</small><br>
                    <span style="color: var(--azul);">${item.precio === 'Consultar' ? 'Consultar precio' : item.precio}</span>
                </div>
                <div class="cantidad-controles">
                    <button onclick="cambiarCantidad(${i}, -1)">−</button>
                    <span>${item.cantidad}</span>
                    <button onclick="cambiarCantidad(${i}, 1)">+</button>
                </div>
                <button class="eliminar" onclick="eliminarItem(${i})"><i class="fa-solid fa-trash"></i></button>
            </div>
        `).join('');

        contador.textContent = carrito.reduce((sum, i) => sum + i.cantidad, 0);
    }

    function cambiarCantidad(i, delta) {
        carrito[i].cantidad += delta;
        if (carrito[i].cantidad < 1) carrito[i].cantidad = 1;
        localStorage.setItem('suplementex_carrito', JSON.stringify(carrito));
        renderCarrito();
    }

    function eliminarItem(i) {
        carrito.splice(i, 1);
        localStorage.setItem('suplementex_carrito', JSON.stringify(carrito));
        renderCarrito();
    }

    function enviarWhatsApp(tipo) {
        if (carrito.length === 0) {
            alert('⚠️ Primero agregá productos al carrito.');
            return;
        }
        let mensaje = tipo === 'compra' ? '🛒 *NUEVO PEDIDO - SUPLEMENTEX*%0A%0A' : '💬 *CONSULTA DE PRODUCTOS - SUPLEMENTEX*%0A%0A';
        carrito.forEach((item, i) => {
            mensaje += `*${i + 1}.* ${item.nombre}%0A`;
            mensaje += `   📦 Presentación: ${item.presentacion}%0A`;
            mensaje += `   🔢 Cantidad: ${item.cantidad}%0A`;
            mensaje += `   💰 Precio: ${item.precio === 'Consultar' ? 'A confirmar' : item.precio}%0A%0A`;
        });
        mensaje += tipo === 'compra' ? '✅ Quiero confirmar este pedido. ¡Gracias!' : '❓ Necesito más información.';
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${mensaje}`, '_blank');
    }

    function consultarProductoWhatsApp() {
        const idx = document.getElementById('modal-presentacion').value;
        const pres = productoActual.presentaciones[idx];
        const msg = `💬 *CONSULTA - SUPLEMENTEX*%0A%0A*Producto:* ${productoActual.nombre}%0A*Presentación:* ${pres.tamano}%0A%0A¿Me pueden dar más información y precio?`;
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`, '_blank');
    }

    function enviarOrientacion() {
        const msg = '👋 Hola, necesito orientación para elegir un suplemento. ¿Me pueden ayudar?';
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
    }

    function filtrarCategoria(cat) {
        const cards = document.querySelectorAll('#lista-productos .tarjeta');
        cards.forEach(card => {
            if (cat === 'Todos' || card.dataset.categoria === cat) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
        document.getElementById('productos').scrollIntoView({ behavior: 'smooth' });
    }

    document.getElementById('modal-producto').addEventListener('click', function(e) {
        if (e.target === this) cerrarModal();
    });

    renderCarrito();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML_TEMPLATE,
        productos=PRODUCTOS,
        WHATSAPP_NUMBER=WHATSAPP_NUMBER
    )

if __name__ == "__main__":
    print("SUPLEMENTEX disponible en http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
