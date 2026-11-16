import argparse
import time
from urllib.parse import urlparse
from urllib.request import urlopen


parser = argparse.ArgumentParser(description="Измерить скорость скачивания")
parser.add_argument("url", help="HTTP или HTTPS адрес файла")
args = parser.parse_args()

address = urlparse(args.url)
if address.scheme not in ("http", "https") or not address.netloc:
    parser.error("укажите полный HTTP или HTTPS адрес")

times = []
total_bytes = 0

for number in range(1, 11):
    start = time.perf_counter()

    try:
        with urlopen(args.url, timeout=30) as response:
            while chunk := response.read(1024 * 1024):
                total_bytes += len(chunk)
    except OSError as error:
        raise SystemExit(f"Запрос {number} не удался: {error}") from error

    times.append(time.perf_counter() - start)

total_seconds = sum(times)
print(f"Среднее время запроса: {total_seconds / 10:.2f} с")
print(f"Скачано: {total_bytes / 1_000_000:.2f} МБ")
print(f"Скорость скачивания: {total_bytes / total_seconds / 1_000_000:.2f} МБ/с")
