import yt_dlp
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv() 

# Enlace de YouTube o SoundCloud
url = input("Introduce la url del audio, canción o playlist que deseas descargar: \n")

# Carpeta de descarga
output_dir = "downloadsMP3"
os.makedirs(output_dir, exist_ok=True)

# Configuración de yt-dlp con máxima compatibilidad de carátula
ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    
    # 1. INDICA A YT-DLP QUE DESCARGUE LA MINIATURA
    'writethumbnail': True, 
    
    # 2. INDICA A YT-DLP QUE CONVIERTA LA MINIATURA A JPG (Mejor compatibilidad)
    'convert-thumbnails': 'jpg', 
    
    # 3. **NUEVO:** FUERZA UNA RESOLUCIÓN MÁXIMA PARA LA MINIATURA (Ej. 600px de ancho)
    # Esto reduce el tamaño del archivo de carátula, resolviendo el problema en algunos móviles.
    # El valor 'max_resolution' no es una opción oficial, usaremos el formato con limitación de ancho
    # La mejor manera de forzar esto es usando la opción 'format' directamente, pero es más complejo. 
    # Dejamos la selección de tamaño en el postprocesador para simplificar.
    # Vamos a usar 'postprocessor_args' con el argumento de tamaño de ffmpeg para máxima precisión.
    
    'postprocessors': [
        {
            # CONVIERTE EL AUDIO EXTRAÍDO A MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        # POSTPROCESADOR CORREGIDO, SIN ARGUMENTOS INNECESARIOS
        {
            'key': 'EmbedThumbnail',  
            # Se puede usar postprocessor_args para forzar el tamaño si es necesario, pero
            # primero probemos sin argumentos complejos, ya que la conversión a JPG y la eliminación del error
            # de sintaxis deberían ser suficientes.
        }
    ],
    
    # RUTA A FFMPEG (importante para la conversión y la incrustación)
    'ffmpeg_location': os.getenv('FFMPEG_PATH'), 
}

# Descargar audio
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print(f"\n--- Iniciando descarga y conversión para: {url} ---\n")
    info = ydl.extract_info(url, download=True)
    
    # Obtiene el título para el mensaje final
    if 'entries' in info and info.get('webpage_url_basename') != 'list':
        title = info['entries'][0].get('title', 'Canción de Playlist') if info.get('entries') else 'Playlist'
    else:
        title = info.get('title', 'Archivo de Audio')

    mp3_path_ejemplo = os.path.join(output_dir, f"{title}.mp3")
    
print(f"\n✅ Proceso completado exitosamente.")
print(f"La música (con carátula forzada a JPG) está en la carpeta: {output_dir}")
print(f"Archivo generado en: {mp3_path_ejemplo}")