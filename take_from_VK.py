from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://vk.com/audios515257817?section=all"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(url)

# ⏳ логинишься вручную
time.sleep(20)

# 🔁 прокрутка до конца
last_height = 0
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 🧠 вытаскиваем данные через JS
tracks = driver.execute_script("""
let result = [];
document.querySelectorAll('.audio_row').forEach(row => {
    let title = row.querySelector('.audio_row__title_inner');
    let artist = row.querySelector('.audio_row__performers');
    if (title && artist) {
        result.push(artist.innerText + " — " + title.innerText);
    }
});
return result;
""")

with open("tracks.txt", "w", encoding="utf-8") as f:
    for t in tracks:
        f.write(t + "\n")

driver.quit()
print(f"✔ Сохранено треков: {len(tracks)}")

with open("tracks.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

lines = [line.rstrip("\n") for line in lines][::-1]

with open("tracks.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Сохранена последовательность треков")