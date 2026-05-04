# DJ-Content-Automation-Engine 🎧

Un framework potente y modular diseñado para automatizar la creación de videos profesionales (Shorts y Reels) específicamente para DJs y artistas. Este proyecto utiliza una arquitectura de **Herramientas y Pipelines** para orquestar servicios de IA de última generación (Groq, Pollinations, Whisper) en productos de video de alta calidad.

---

## ⚡ Novedades y Mejoras Recientes
Hemos transformado el motor original en una solución especializada para DJs con las siguientes mejoras:

*   **Migración a Groq**: Generación de guiones e ideas ultra-rápida y coherente.
*   **Integración con Pollinations.ai**: Generación de imágenes artísticas de alta calidad sin las limitaciones de cuota de servicios tradicionales.
*   **Pipeline de Audio y Subtítulos de Alta Precisión**:
    *   Soporte completo para **Whisper.cpp** en Windows con re-muestreo automático a 16kHz.
    *   **Corrección gramatical inteligente**: El sistema corrige automáticamente errores de pronunciación/transcripción (como "lusto" por "listo") y limpia caracteres especiales corruptos en cierres ("Únete a mí").
    *   **Sincronización Extendida**: El último bloque de subtítulos se mantiene un segundo extra para asegurar que la última palabra sea legible.
*   **Robustez Anti-Errores**: El sistema detecta automáticamente archivos JSON de Whisper corruptos o mal codificados, los elimina y los regenera automáticamente sin detener el pipeline.
*   **Consistencia de Personaje**: Sistema de prompts unificado para mantener la apariencia de un DJ de 40-42 años con barba y estilo visual webcomic profesional en todos los videos.
*   **Control de Flujo Inteligente**: Posibilidad de pausar la creación de nuevas ideas aleatorias para priorizar el procesamiento de la cola de ideas pendientes (`PENDING`, `SCRIPT_GENERATED` o `IMAGES_GENERATED`).


---

## 🚀 Capacidades Principales

1.  **Generación de Guiones Narrativos**: Crea historias que conectan emocionalmente con la audiencia, no solo tips técnicos.
2.  **Multicategoría DJ**: 9 categorías especializadas (Mindset, Performance, Técnica, Psicología, Storytelling, Branding, Equipos, Reality Check y Estrategia).
3.  **Producción Completa en 7 Pasos**: Desde la idea hasta el video final con música y subtítulos.
4.  **Estilo Visual Premium**: Ilustraciones digitales 2D con iluminación cinematográfica y estética de cómic moderno.
5.  **Sincronización Precisa**: Audio narrado y subtítulos perfectamente alineados con las escenas visuales.

---

## 🛠️ Stack Tecnológico
- **Lenguaje**: Python 3.11+
- **IA de Texto**: [Groq](https://groq.com/) (Llama 3 / Mixtral)
- **IA de Imagen**: [Pollinations.ai](https://pollinations.ai/)
- **IA de Audio (TTS)**: Google Gemini TTS (Voz: Fenrir)
- **Transcripción**: [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) (Local, rápido, offline)
- **Motor de Video**: [FFmpeg](https://ffmpeg.org/)
- **Persistencia**: Seguimiento de ciclo de vida basado en CSV

---

## 🏃 Cómo Usarlo (Guía Rápida)

### 1. Instalación
```bash
# Instalar dependencias
poetry install

# Configurar variables de entorno en .env (renombrar .env.example)
AI_PROVIDER=groq
GEMINI_API_KEY=tu_llave_aqui
OPENAI_API_KEY=tu_llave_aqui
GROQ_API_KEY=tu_llave_aqui
IMAGE_PROVIDER=pollinations
```

### 2. Ejecutar el Pipeline Completo
Para generar videos de forma infinita (o procesar ideas pendientes):
```bash
make icg-s-all
```

### 3. Procesar Ideas Específicas
Si quieres que el sistema cree un video sobre un tema específico:
1. Abre `flows/image_content_generator/out_short/ideas_tracking.csv`.
2. Agrega una nueva línea: `ID, Tu Título, PENDING, Categoría`.
   * Ejemplo: `100, El secreto de los drops, PENDING, DJAdviceHandler_TechnicalDJIdea`
3. Ejecuta el pipeline y el sistema la procesará primero.

---

## 📂 Estructura del Pipeline (7 Pasos)

| Paso | Método | Descripción |
| :--- | :--- | :--- |
| **1** | `step1_generate_story` | Genera la idea y el guion completo (JSON). Prioriza ideas `PENDING`. |
| **2** | `step2_generate_images` | Genera una imagen por escena basada en el guion. |
| **3** | `step3_generate_audios` | Genera la narración de voz y alinea el audio. |
| **4** | `step4_generate_videos` | Ensambla imágenes y audio en clips de escena. |
| **5** | `step5_generate_subtitles` | Transcribe y añade subtítulos (con auto-corrección "DJ"). |
| **6** | `step6_add_background_music` | Mezcla música de fondo aleatoria con la voz. |
| **7** | `step7_rename_final_video` | Renombra el archivo final con el título de la idea. |

---

## 🎨 Categorías de Contenido Disponibles

- **Mindset**: Transformación mental del DJ.
- **Strategy**: Estrategias prácticas de carrera.
- **Performance**: Manejo de cabina, energía y errores en vivo.
- **Technical**: EQ, phrasing, drops y mezcla armónica.
- **Psychology**: Psicología del público y anticipación.
- **Storytelling**: El viaje musical y la narrativa del set.
- **Branding**: Marca personal e identidad de artista.
- **Gear**: Equipos, controladores vs CDJs.
- **Reality Check**: Verdades incómodas de la industria.

---

## 📂 Estructura del Proyecto
- `flows/image_content_generator/`: El motor principal de generación de contenido.
- `tools/`: Componentes atómicos (FFmpeg, Whisper, Groq, Pollinations).
- `out_short/`: Carpeta donde se guardan los videos y assets generados.
- `resource/`: Música de fondo y referencias de estilo.

---

## ⚠️ Notas Técnicas Importantes

- **Cuotas de Gemini TTS**: El modelo `gemini-2.5-flash-tts` tiene un límite estricto de **10 peticiones diarias** en el plan gratuito. Si el pipeline se detiene con error 429, deberás esperar al reinicio de cuota.
- **Requisitos de Whisper**: Es obligatorio que el ejecutable `whisper-cli.exe` esté accesible en la ruta configurada. El sistema utiliza el modelo `base` por defecto para un balance óptimo entre velocidad y precisión.
- **Codificación en Windows**: Para evitar caracteres raros en los subtítulos, el motor limpia activamente secuencias no-UTF8 generadas por la salida de consola de Whisper.

---
*Desarrollado con pasión para la comunidad DJ.* 🎧🔥

Dj Poche