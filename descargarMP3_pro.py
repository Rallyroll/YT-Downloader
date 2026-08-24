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

# Configuración de yt-dlp: Autor y Álbum (Solo si existe)
ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    
    # Opciones de Carátula (Cover Art)
    'writethumbnail': True, 
    'convert-thumbnails': 'jpg', 
    
    # **CORRECCIÓN CLAVE 1:** Define explícitamente el campo 'album'.
    # Usamos %(album|)s, que significa: usa el valor de 'album', o nada si está vacío.
    # El campo 'artist' (Autor) se añade por defecto si 'metadatatofile' está activo.
    'metadata_from_field': {'album': '%(album|)s'},

    # Esta opción es necesaria para que yt-dlp lea y escriba las variables.
    'metadatatofile': True,
    'fragment_retries': 10,
    
    'postprocessors': [
        {
            # CONVIERTE EL AUDIO EXTRAÍDO A MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            # **CORRECCIÓN CLAVE 2:** El post-procesador FFmpegMetadata ya no
            # necesita argumentos, pues la configuración de metadatos se hizo arriba.
            'key': 'FFmpegMetadata',
        },
        {
            # INCRUSTA LA MINIATURA COMO CARÁTULA
            'key': 'EmbedThumbnail',  
        }
    ],
    
    # RUTA A FFMPEG (importante para la conversión y la incrustación)
    'ffmpeg_location': os.getenv('FFMPEG_PATH'), 
}

# Descargar audio
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print(f"\n--- Iniciando descarga y conversión con metadatos corregidos para: {url} ---\n")
    info = ydl.extract_info(url, download=True)
    
    # Obtiene el título para el mensaje final
    if 'entries' in info and info.get('webpage_url_basename') != 'list':
        title = info['entries'][0].get('title', 'Canción de Playlist') if info.get('entries') else 'Playlist'
    else:
        title = info.get('title', 'Archivo de Audio')

    mp3_path_ejemplo = os.path.join(output_dir, f"{title}.mp3")
    
print(f"\n✅ Proceso completado exitosamente.")
print(f"La música (con metadatos corregidos) está en la carpeta: {output_dir}")
print(f"Archivo generado en: {mp3_path_ejemplo}")