import os
import sys
import platform
import zipfile
import urllib.request
import shutil
import subprocess

# Настройки плагинов
PLUGINS_DATA = {
    "1": {
        "name": "RentSteam",
        "url": "https://cloclo55.cloud.mail.ru/public/VhsD/VtvkZKfeE/RentSteam%20%282%29.zip",
        "zip_name": "RentSteam.zip"
    },
    "2": {
        "name": "VipRoblox",
        "url": "https://cloclo55.cloud.mail.ru/public/xSae/rp8jzzZjz/VipRoblox_multi.zip",
        "zip_name": "VipRoblox_multi.zip"
    }
}

PLUGINS_DIR = "plugins"
VENV_NAMES = ["venv", ".venv", "pyvenv", "env"]

def get_os():
    return platform.system().lower()

def find_venv():
    """Ищет виртуальное окружение в текущей директории."""
    system = get_os()
    current_dir = os.getcwd()
    
    for name in VENV_NAMES:
        venv_path = os.path.join(current_dir, name)
        if os.path.isdir(venv_path):
            if system == "windows":
                python_exe = os.path.join(venv_path, "Scripts", "python.exe")
            else:
                python_exe = os.path.join(venv_path, "bin", "python")
            
            if os.path.exists(python_exe):
                return python_exe
    return None

def download_file(url, filename):
    print(f"[*] Скачивание {filename}...")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename)
        print(f"[+] Файл {filename} успешно скачан.")
        return True
    except Exception as e:
        print(f"[-] Ошибка при скачивании {filename}: {e}")
        return False

def install_plugin(plugin_key):
    plugin = PLUGINS_DATA[plugin_key]
    zip_name = plugin["zip_name"]
    
    if not os.path.exists(zip_name):
        if not download_file(plugin["url"], zip_name):
            return

    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)

    print(f"[*] Распаковка {zip_name} в {PLUGINS_DIR}...")
    try:
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(PLUGINS_DIR)
        print(f"[+] Плагин {plugin['name']} установлен.")
    except Exception as e:
        print(f"[-] Ошибка при распаковке: {e}")

def run_pip_install(python_bin, requirements_path):
    """Запускает установку зависимостей через конкретный python."""
    print(f"[*] Установка зависимостей через {python_bin}...")
    try:
        subprocess.run([python_bin, "-m", "pip", "install", "-r", requirements_path], check=True)
        print("[+] Зависимости успешно установлены.")
    except Exception as e:
        print(f"[-] Ошибка при установке зависимостей: {e}")

def main():
    system = get_os()
    print(f"=== Универсальный установщик плагинов ({system}) ===")
    
    # Поиск виртуального окружения
    venv_python = find_venv()
    if venv_python:
        print(f"[+] Найдено виртуальное окружение: {os.path.dirname(os.path.dirname(venv_python))}")
        target_python = venv_python
    else:
        print("[!] Виртуальное окружение не найдено в текущей папке.")
        print(f"[*] Будет использован системный Python: {sys.executable}")
        target_python = sys.executable

    print("\nВыберите плагин для установки:")
    print("1. RentSteam")
    print("2. VipRoblox")
    print("3. Установить оба")
    choice = input("Введите номер (1/2/3): ").strip()

    to_install = []
    if choice == "1":
        to_install = ["1"]
    elif choice == "2":
        to_install = ["2"]
    elif choice == "3":
        to_install = ["1", "2"]
    else:
        print("[-] Неверный выбор.")
        return

    for key in to_install:
        install_plugin(key)

    # Путь к файлу зависимостей из инструкции
    req_source = "requirements win.txt" if system == "windows" else "requirements lin.txt"
    req_path = os.path.join("Инструкция к плагинам", req_source)

    if os.path.exists(req_path):
        # Для Windows дополнительно обновляем локальный requirements.txt как в гайде
        if system == "windows":
            shutil.copy(req_path, "requirements.txt")
            print("[+] Файл requirements.txt обновлен.")
        
        run_pip_install(target_python, req_path)
    else:
        print(f"[!] Файл {req_path} не найден. Пропуск установки зависимостей.")

    # Специфичные шаги для Windows
    if system == "windows" and os.path.exists("Setup.bat"):
        print("[*] Запуск Setup.bat...")
        subprocess.run(["cmd", "/c", "Setup.bat"])

    print("\n[Установка завершена]")
    if system == "linux" and venv_python:
        print(f"Совет: Для запуска бота используйте: {venv_python} main.py (или другой стартовый файл)")

if __name__ == "__main__":
    main()