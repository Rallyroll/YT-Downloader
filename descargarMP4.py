import yt_dlp
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv() 

# Enlace de YouTube
url = input("Introduce la url del video o playlist que deseas descargar: \n")

# Pedir resolución deseada (ej. 480). Si se deja vacío, se usará 480 como máximo
res_input = input("Introduce la resolución deseada en píxeles (ej. 480) o deja vacío para usar 480: ").strip()
try:
    res = int(res_input) if res_input else 480
except ValueError:
    print("Entrada inválida, usando 480p por defecto")
    res = 480

# Carpeta de descarga
output_dir = "downloadsMP4"
os.makedirs(output_dir, exist_ok=True)

# Configuración de yt-dlp para descargar video en formato MP4
# Usamos height<=res para limitar la resolución máxima (p. ej. 480)
format_str = f"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
ydl_opts = {
    'format': format_str,
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
    'ffmpeg_location': os.getenv('FFMPEG_PATH'),  #! Asegúrate de que ffmpeg esté en tu PATH
}

# Descargar video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    title = info.get('title', None)
    webm_path = os.path.join(output_dir, f"{title}.webm")

# Convertir a MP4
mp4_path = os.path.join(output_dir, f"{title}.mp4")

print(f"✅ Descarga completada. Archivo (si se convirtió) -> {mp4_path}")