import re
import os
import requests
import time
import yt_dlp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

# Konfiguracja przeglądarki headless
options = Options()
options.headless = True
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# Otwórz stronę
def generate_list(id):

    url = f"https://tbmp3.pl/audycje/audycja.php?audycja={id}"
    driver.get(url)
    time.sleep(3)

    # Pobierz pełny tekst strony
    page_text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    url = f"https://tbmp3.pl/audycje/audycja.php?audycja={id}"
    # Wyciągnij linie zaczynające się od liczby i kropki (np. 1. Pink Floyd – Time)
    lines = page_text.splitlines()
    numbered_lines = [line.strip() for line in lines if re.match(r"^\d+\.\s", line.strip())]

    # Zapisz do pliku
    with open("lista_audycji.txt", "w", encoding="utf-8") as f:
        f.write(f"🎵 Lista pozycji z audycji {id}:\n\n")
        for line in numbered_lines:
            f.write(line + "\n")

    print(f"✅ Gotowe! Zapisano {len(numbered_lines)} linii do pliku 'lista_audycji_726.txt'.")

def leading_zero():
    with open("lista_audycji.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Wzorzec: np. 1. Komentarz Tomasza
    pattern = re.compile(r"^(\d+)\.\s+(.+)$")
    sygnaly = []
    komentarze = []
    utwory = []
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            num = int(match.group(1))
            content = match.group(2)
            # Sformatowany numer: 01., 02., ..., 10., ...
            formatted_num = f"{num:02d}. {content}"
            if content.lower().startswith("sygnał"):
                sygnaly.append(formatted_num)
            elif content.lower().startswith("komentarz"):
                komentarze.append(formatted_num)
            else:
                utwory.append(formatted_num)
    # Zapisz do plików
    with open("sygnaly.txt", "w", encoding="utf-8") as f:
        for line in sygnaly:
            f.write(line + "\n")
    with open("komentarze.txt", "w", encoding="utf-8") as f:
        for line in komentarze:
            f.write(line + "\n")
    with open("utwory.txt", "w", encoding="utf-8") as f:
        for line in utwory:
            f.write(line + "\n")
    print("✅ Gotowe! Wszystkie pliki mają poprawioną numerację do dwóch cyfr.")

def download_comms():
    # Ścieżka do pliku z komentarzami
    with open("komentarze.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    suffix = "1986/1986-05-19_RMR_"
    base_url = "https://tbmp3.pl/files/"
    output_folder = "pobrane_komentarze"

    os.makedirs(output_folder, exist_ok=True)

    for line in lines:
        match = re.match(r"^(\d{2})\.", line.strip())  # dopasuj numer z przodu (np. 03.)
        if match:
            number = match.group(1)
            remote_path = f"{suffix}{number}.mp3"
            url = base_url + remote_path

            # Użyj tylko nazwy pliku bez folderu "1986/"
            local_filename = os.path.basename(f'{number} Komentarz.mp3')  # => 1986-05-19_RMR_12.mp3
            local_path = os.path.join(output_folder, local_filename)

            print(f"Pobieram {url}...")
            response = requests.get(url)
            if response.status_code == 200 or response.status_code == 206:
                with open(local_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Zapisano do {local_path}")
            else:
                print(f"⚠️ Błąd {response.status_code}: nie udało się pobrać {url}")

def download_songs():
    # Ścieżka do pliku z utworami
    # Wczytaj plik z utworami
    with open("utwory.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_folder = "pobrane_utwory"
    os.makedirs(output_folder, exist_ok=True)

    # Konfiguracja yt-dlp
    ydl_opts_base = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    for line in lines:
        match = re.match(r"^(\d{2})\.\s+(.*)", line.strip())  # np. 02. Nazwa utworu
        if match:
            index = match.group(1)
            title = match.group(2)

            # Przygotuj nazwę pliku mp3
            safe_title = re.sub(r'[^\w\s\-_()]', '', title).strip().replace(" ", "_")
            filename = f"{index}_{safe_title}.mp3"
            filepath = os.path.join(output_folder, filename)

            # yt-dlp config dla konkretnego pliku
            ydl_opts = ydl_opts_base.copy()
            ydl_opts['outtmpl'] = filepath

            print(f"🔍 Szukam i pobieram: {title}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([f"ytsearch1:{title}"])
                    print(f"✅ Zapisano: {filename}")
                except Exception as e:
                    print(f"❌ Błąd przy pobieraniu '{title}': {e}")


if __name__ == "__main__":
    id = "232"
    generate_list(id)
    leading_zero()
    download_comms()
    download_songs()
    print(1)#Genereate list of songs and comms