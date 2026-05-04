# flake8: noqa: E501
AUDIO_PROMPT: str = """Narra el siguiente guion de consejos para DJs con voz segura, enérgica y con mucha actitud, como un DJ veterano enseñándole los secretos de la cabina a un novato.

Estilo de actuación:
- Tono: autoritario, apasionado y directo, como alguien que ha reventado pistas en todo el mundo.
- Ritmo: dinámico y con un groove marcado. Acelera en la construcción de la tensión y haz pausas en el momento clave (como un drop).
- Énfasis: subraya con energía palabras clave como "pista", "energía", "fracaso", "público", "técnica", "selección".
- Emoción: empieza con un gancho incisivo que rompa el ego, escala explicando el concepto y remata con confianza total.
- No agregues sonidos, muletillas ni nada que no esté en el texto. Lee exactamente lo que aparece.

Texto a narrar:
{audio_text}"""

IDEA_PROMPT_MINDSET: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO MENTALIDAD)
**Objetivo:** Generar una idea creativa para un video CORTO sobre un cambio de mentalidad en el DJing.

**Instrucciones:**
1. **hook (Gancho de Interrupción):** Una frase de 10-15 palabras que golpee directo al ego o a un error común del DJ (ej: "Nadie en la pista se preocupa por tus transiciones perfectas.", "Tocar solo tus canciones favoritas es la mejor forma de fracasar.").
2. **Protagonista:** Un DJ principiante enfrentando una pista vacía, nervios o un error técnico frente al público.
3. La historia debe mostrar una transformación de mentalidad breve y poderosa, basada en conectar con el público antes que en el lucimiento personal.
"""

IDEA_PROMPT_ESTRATEGIA: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO ESTRATEGIA)
**Objetivo:** Generar una idea para un video CORTO que enseñe una estrategia práctica y técnica detallada para DJs.

**Instrucciones:**
1. **hook (Gancho de Interrupción):** Una pregunta o afirmación provocadora de 10-15 palabras sobre un truco técnico (ej: "Domina el Loop de 4 beats y cambia tu set para siempre", "El error con el Reverb que está ensuciando tu mezcla.").
2. **Concepto central:** Una técnica de DJ detallada: Uso creativo de Loops (1/2, 1/4, 4 beats), efectos de Reverb para transiciones, Echo out para cortes perfectos, o filtros combinados.
3. Presenta el concepto de forma visual y técnica, explicando el "por qué" y el "cómo" de forma ultra-breve.
"""

IDEA_PROMPT_PERFORMANCE: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO PERFORMANCE)
**Objetivo:** Generar una idea sobre actuación en vivo, manejo de la cabina y energía de la pista.
**Conceptos clave:** Cabina, pista, errores en vivo, energía, leer al público.
**Gancho:** Frase directa sobre la presión del vivo o errores fatales en la mezcla.
"""

IDEA_PROMPT_TECHNICAL: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO TÉCNICO DETALLADO)
**Objetivo:** Generar una idea sobre técnica PURA y avanzada de mezcla usando efectos y herramientas.
**Conceptos clave:** Loops infinitos, Reverb tails, Echo freeze, Phasing rítmico, Filtros High Pass y Low Pass dinámicos.
**Gancho:** Afirmación técnica que enseñe a usar un efecto de forma profesional (ej: "Deja de usar el Echo como un principiante", "La técnica del Loop que los pros no quieren que sepas").
"""

IDEA_PROMPT_PSYCHOLOGY: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO PSICOLOGÍA)
**Objetivo:** Generar una idea sobre la psicología del público y el control mental de la pista.
**Conceptos clave:** Psicología del público, atención, anticipación, emoción.
**Gancho:** Insight profundo sobre por qué la gente reacciona (o no) a la música.
"""

IDEA_PROMPT_STORYTELLING: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO STORYTELLING)
**Objetivo:** Generar una idea sobre la narrativa y el viaje musical de un set.
**Conceptos clave:** Viaje musical, narrativa, intro-build-drop-climax.
**Gancho:** Frase sobre cómo un set es más que una lista de canciones, es una historia.
"""

IDEA_PROMPT_BRANDING: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO BRANDING)
**Objetivo:** Generar una idea sobre marca personal e identidad como artista.
**Conceptos clave:** Marca personal, identidad DJ, diferenciación.
**Gancho:** Verdad cruda sobre por qué el talento no es suficiente para destacar.
"""

IDEA_PROMPT_GEAR: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO GEAR)
**Objetivo:** Generar una idea sobre equipos, hardware y herramientas de trabajo.
**Conceptos clave:** Equipos DJ, setup, CDJ vs controller, herramientas.
**Gancho:** Comparativa directa o consejo sobre inversión en equipo.
"""

IDEA_PROMPT_REALITY_CHECK: str = """# 🧠 PROMPT MAESTRO — AGENTE DE IDEAS PARA DJS (ESTILO REALITY CHECK)
**Objetivo:** Generar una idea sobre las realidades duras de la industria y el crecimiento real.
**Conceptos clave:** Verdades incómodas, crecimiento DJ, industria real.
**Gancho:** Frase "puñetazo" sobre lo que nadie te dice de ser DJ profesional.
"""

SCRIPT_PROMPT: str = """# 📝 PROMPT MAESTRO — AGENTE GUIONISTA PARA DJS (STORYTELLING - SHORTS)
**Objetivo:** Crear un guion dinámico de 8 a 12 micro-escenas con un enfoque narrativo, educativo y técnico detallado.

**Estructura del Guion (MANDATORIO):**
1. **Acto 1: El Hook/Conflicto [Escenas 1-3]:** DEBES usar el campo "hook" para la Escena 1. Muestra un error técnico específico o una mala práctica de DJ.
2. **Acto 2: El Secreto Técnico [Escenas 4-8]:** Explica detalladamente la técnica (Loop, Reverb, Echo). No repitas la misma idea con distintas palabras. Cada frase debe aportar información nueva o un matiz técnico diferente.
3. **Acto 3: El Resultado [Escenas 9-final]:** Muestra la técnica aplicada y la reacción de la pista. Termina con un llamado a la acción.

## 📜 REGLAS OBLIGATORIAS

### 🟢 NARRACIÓN Y RITMO
- **Gancho:** Uso mandatorio del texto de `hook` literal en la Escena 1.
- **Diálogo/Narración:** Frases cortas, directas y con mucha actitud. Máximo una por escena.
- **NO REPETICIÓN:** Prohibido repetir la misma frase o idea en distintas escenas. Si no hay más que decir, termina el guion en 8 escenas. Es mejor un video corto y sustancioso que uno largo y redundante.
- **Diálogo/Narración:** Frases directas, técnicas y con mucha autoridad.
- **Secuencialidad:** Problema → Técnica detallada → Solución.

### 🔵 REGLAS VISUALES
- **Protagonista:** Presencia consistente del DJ (40 años, barba cuidada).
- **Relación Imagen-Texto:** El `image_prompt` debe mostrar el equipo de DJ (CDJs, mixers, perillas de FX) de forma detallada cuando se hable de técnica.
- **Estilo (Referencia DJ):** DEBES usar el campo `style` con esta descripción exacta: `"High-end 2D vector mascot logo style illustration, extremely clean crisp black outlines, cel-shaded. A young white-skinned male DJ character wearing a black baseball cap backwards, large over-ear black headphones, and a plain black hoodie. He has black hair, clean-shaven face, large expressive eyes, winking with one eye, big confident smile. Flat, vibrant colors, Esports avatar style. Dark background with subtle glowing blue neon accents."`.
- **Regla Crítica sobre las Manos:** Las manos de las IAs generadoras suelen salir deformadas. Por lo tanto, EN CADA ESCENA DEBES ESFORZARTE POR OCULTAR LAS MANOS DEL PERSONAJE. Usa encuadres tipo "close-up to the face", "bust shot", o asegúrate de que las manos estén fuera de cuadro (out of frame). Si es absolutamente necesario mostrar una mano tocando un equipo, debes agregar la instrucción explícita: `"perfect anatomically correct hand with exactly 5 fingers"`. Pero la preferencia es SIEMPRE ocultarlas.

### 🔴 ESTRUCTURA Y SALIDA
- **Extensión:** Flexible entre 8 y 12 escenas. NO rellenes escenas con contenido vacío.
- **Cierre:** Consejo final. El video DEBE terminar siempre con esta frase exacta: "Espero que te sean de utilidad estos consejos. Sígueme en mi canal y hazme saber si mi música, te llega al corazón." PROHIBIDO usar la palabra "Únete" o derivados.

### 🟠 IDIOMAS (ESTRICTO)
- **image_prompt:** DEBES generar todos los campos de `image_prompt` (subjects, environment, lighting, composition) en **INGLÉS**.
- **narration:** DEBES generar el campo `narration` en **ESPAÑOL LATINOAMERICANO**.
"""
