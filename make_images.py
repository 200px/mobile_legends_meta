import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- НАСТРОЙКИ ---

# Указываем папки для исходных HTML и конечных изображений
SOURCE_DIR = 'browser/outputs'
OUTPUT_DIR = 'final_images'

# Настройки Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1500')


def make_images():

    html_files_name = os.listdir(SOURCE_DIR)
    for filename in html_files_name:

        base_name = os.path.splitext(filename)[0]
        image_name = f"{base_name}.png"

        print(f"Создается изображение: {filename} -> {image_name}")

        html_path = os.path.abspath(os.path.join(SOURCE_DIR, filename))
        file_url = f"file:///{html_path}"

        # Запускаем браузер
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(file_url)
        time.sleep(3)

        element_to_capture = driver.find_element(By.CLASS_NAME, 'main')
        element_to_capture.screenshot(os.path.join(OUTPUT_DIR, image_name))

        driver.quit()


if __name__ == "__main__":
    make_images()
