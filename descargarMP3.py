import yt_dlp
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv() 

print(f"\n\x1b[46m \x1b[1m \x1b[30"+"~~~~~~ YT DOWNLOADER ~~~~~~"+"\x1b[0m\n")

# Enlace de YouTube o SoundCloud
url = input("Introduce la url del audio, canción o playlist que deseas descargar: \n")

# Carpeta de descarga
output_dir = "downloadsMP3"
os.makedirs(output_dir, exist_ok=True)

# Configuración de yt-dlp: Autor y Álbum (Solo si existe)
ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': os.getenv('FFMPEG_PATH'),  # Asegúrate de que ffmpeg esté en tu PATH
    'fragment_retries': 10,
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
print(f"La música está en la carpeta:"+"\x1b[34m\x1b[1m "+ output_dir+"\x1b[0m")
print(f"Archivo generado en:"+"\x1b[35m\x1b[1m "+ mp3_path_ejemplo+"\x1b[0m")