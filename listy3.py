import re

# Wczytaj oryginalną listę


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
