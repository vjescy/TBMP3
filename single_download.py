import yt_dlp

# 🔗 Wklej tutaj link do filmu z YouTube
youtube_url = input("Podaj link do YouTube: ").strip()

# 📁 Nazwa folderu docelowego
output_folder = "mp3_z_youtube"

# Konfiguracja yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f"{output_folder}/%(title).80s.%(ext)s",  # nazwa pliku = tytuł.mp3
    'quiet': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Pobierz plik
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([youtube_url])
        print("✅ Pobrano jako MP3")
    except Exception as e:
        print(f"❌ Błąd: {e}")

