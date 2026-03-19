import http.server
import socketserver
import threading
import webbrowser
from functools import partial
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
ENTRY_FILE = "RP_10.html"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    app_dir = Path(__file__).resolve().parent
    entry_path = app_dir / ENTRY_FILE

    if not entry_path.exists():
        raise FileNotFoundError(f"Не найден файл интерфейса: {entry_path}")

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(app_dir))

    # Отдаем файлы из папки проекта, чтобы страница выглядела и работала 1:1 как в RP_10.html.
    with ReusableTCPServer((HOST, PORT), handler) as httpd:
        httpd_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        httpd_thread.start()

        url = f"http://{HOST}:{PORT}/{ENTRY_FILE}"
        print(f"Сервер запущен: {url}")
        print("Для остановки нажмите Ctrl+C")

        webbrowser.open(url)

        try:
            httpd_thread.join()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
            httpd.shutdown()


if __name__ == "__main__":
    main()
