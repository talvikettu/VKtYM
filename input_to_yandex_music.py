from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://music.yandex.ru")

# 🔐 логин вручную
time.sleep(55)

with open("tracks.txt", "r", encoding="utf-8") as f:
    tracks = f.readlines()

for track in tracks:
    track = track.strip()
    if not track:
        continue

    # 🔍 поиск
    search = driver.find_element(By.TAG_NAME, "input")
    search.clear()
    search.send_keys(track)
    search.send_keys(Keys.ENTER)

    time.sleep(3)

    try:
        # 🥇 первый трек из результатов поиска
        first_track = driver.find_elements(
            By.CSS_SELECTOR,
            '.HorizontalCardContainer_root__YoAAP'
        )[0]

        # ❤️ кнопка Like именно этого трека
        like_btn = first_track.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Like"]'
        )

        # 👀 прокрутка
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            like_btn
        )

        # 🖱️ надёжный клик
        driver.execute_script("arguments[0].click();", like_btn)

        print(f"✔ Добавлен: {track}")

    except Exception as e:
        with open("failed_tracks.txt", "a", encoding="utf-8") as fail_file:
            fail_file.write(track + "\n")
        print(f"❌ Не удалось добавить: {track}")

driver.quit()