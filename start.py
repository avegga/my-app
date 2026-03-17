Сделаю каркас максимально похожего приложения на Python в одном скрипте (GUI + логика загрузки/отображения/ошибок), а потом при необходимости вместе дотюним детали под твою БД и формат файлов. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/168548725/4e66afca-19e8-4abf-bff5-4f88a26acf42/RP_10.html?AWSAccessKeyId=ASIA2F3EMEYEUCIKGSME&Signature=U1ErADG63Xn5uOsUaHDrxT7AMvg%3D&x-amz-security-token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJHMEUCIB%2FyqQrpFxrxV5cON111CewY8CfEVAWbhV9%2FcR9Ic6wXAiEAyBPhdqd1K2P9RQMD%2BDOH%2B5%2Bq4ynHs3YptxQqP8excdAq%2FAQI8v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDK1Rey28YPoE0OPDWSrQBDXRtnb%2F0OunSv04w9lA7%2F4DsGT1kqKRh0OrfR9AJ3nCe%2BmsAxYVl3S7SKD1PzZWRjB0Z1BTYkIf9klMjhvKckgqs5aQWU37KP%2Bk1xQmt4xJFt7wgkOxTWCr987V1eaIjktLGjHqVJnkPm85ANJJrG6aSwPB4iXsmQLfgAXeSFgN%2FWMyOyXDUO1RVnVvYMLeve0oTKl%2BFSdi%2B73Vx5dVquPqqW0ZN9JHoH9Yl42eGN6vm5lH3BD8iN%2BmlFP2vnj718qux%2FWo4MAOPqNkssYG9bLvm810YS1McQZz%2BxohmsMiAD9dq8xLEYo8KAOaNUpo6XbwmznkOFeyciuUltBsQuJ20J%2FSyYSMS28k0Hdx45Wikw4J7jFZFfDtYkJRiWp3DiW0npvTxoqLqdXk2hJ27RoYCB0hZP2HOG20lVNM2OG76qQrdptKJ5UMMTy4uc8Dhi8sibOUuL2rAAHM%2BEN%2BLGaOIeHw0mojd8McZE2J7zDHQG5GtqlTmcFqfwhacjzMXyDN1Vc2lf6Lnr2a%2BNIu4sA%2BKiFIoIpEU0OeE2LpqZcHI1XynXEo5BTFJ549wBa3R8onaUsMS2XN6H4jmGwXpHIekJzfDo4FQA%2B6zn6z%2FsTf3gV%2FOL3Ba8a83x4x%2B5aVDcApIQKpz14Zs9D82ZRNYmAIiBHoifuULzEQGatseH9rBaqe0bL9hRGxrrBKz%2BtLKqAalIAle1b5WDOuIqRQ9UfBxoaP3C%2BbzO2pO1jW5UeYY0dET6N%2B13sIygBW1NrOYkw09L2TwDnonGMvYoNnj48w7pTmzQY6mAGFF8Xmo6414anJL%2BdpOyZJTvNe0PXHqX%2FJE%2F7tUNg6FhHKR8HHon8W72as4VSpYyxNxz4yqKZEDjJP2qzCFAeOjex8JoIHWsLWQNdIwo8pzpQrD%2BH8DAD2wISSwsYGRIKuSwWbya4nIPeCJANvtr%2BayylpjF6NG4AnsZ5toJtgmY27JRp3MS%2BkdChSAMbN98pgHXkDTknRAA%3D%3D&Expires=1773769527)

Ниже однос криптовый пример на PyQt5 (можно заменить на PySide6, если нужно). Он реализует:

- Главное окно «Система управления фактами» с вкладками.
- Вкладка «Загрузка фактов»: выбор файла, таблица «Результаты загрузки», таблица «Ошибки загрузки».
- Вкладка «Справочник»: выбор типа справочника, выбор «маршрута к БД», кнопки «Загрузить/Сохранить/Очистить», таблица данных.
- Заглушечную бизнес‑логику (чтение CSV/Excel, валидация, эмуляция ошибок).

```python
import sys
import os
import csv
from typing import List, Tuple

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QMessageBox, QHeaderView, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt


class FactsLoaderTab(QWidget):
    """
    Вкладка 'Загрузка фактов':
    - Выбор файла
    - Таблица 'Результаты загрузки'
    - Таблица 'Ошибки загрузки'
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Загрузка фактов")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Блок выбора файла
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        btn_choose_file = QPushButton("Выбрать файл")
        btn_choose_file.clicked.connect(self.choose_file)

        btn_load = QPushButton("Загрузить")
        btn_load.clicked.connect(self.load_facts)

        file_layout.addWidget(QLabel("Файл:"))
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(btn_choose_file)
        file_layout.addWidget(btn_load)

        main_layout.addLayout(file_layout)

        # Таблица результатов загрузки
        results_group = QGroupBox("Результаты загрузки")
        results_layout = QVBoxLayout()
        self.results_label = QLabel("0 записей")
        self.results_table = QTableWidget(0, 0)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(self.results_label)
        results_layout.addWidget(self.results_table)
        results_group.setLayout(results_layout)

        main_layout.addWidget(results_group)

        # Таблица ошибок
        errors_group = QGroupBox("Ошибки загрузки")
        errors_layout = QVBoxLayout()
        self.errors_label = QLabel("0 ошибок")

        self.errors_table = QTableWidget(0, 3)
        self.errors_table.setHorizontalHeaderLabels(["Строка", "Описание ошибки", "Данные"])
        self.errors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        errors_layout.addWidget(self.errors_label)
        errors_layout.addWidget(self.errors_table)
        errors_group.setLayout(errors_layout)

        main_layout.addWidget(errors_group)

        main_layout.addStretch()

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл с фактами",
            "",
            "CSV файлы (*.csv);;Все файлы (*.*)"
        )
        if file_path:
            self.current_file = file_path
            self.file_path_edit.setText(file_path)

    def load_facts(self):
        if not self.current_file:
            QMessageBox.warning(self, "Файл не выбран", "Выберите файл для загрузки.")
            return

        try:
            rows, header = self._read_csv(self.current_file)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения файла", str(e))
            return

        # Простая эмуляция валидации: строки с пустыми полями считаем ошибочными
        valid_rows, errors = self._validate_rows(rows)

        self._fill_results_table(valid_rows, header)
        self._fill_errors_table(errors)

    def _read_csv(self, path: str) -> Tuple[List[List[str]], List[str]]:
        rows = []
        header = []
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for i, row in enumerate(reader):
                if i == 0:
                    header = row
                else:
                    rows.append(row)
        return rows, header

    def _validate_rows(self, rows: List[List[str]]):
        valid = []
        errors = []
        for idx, row in enumerate(rows, start=2):  # 2, т.к. 1 строка - заголовок
            if any(cell.strip() == "" for cell in row):
                errors.append((idx, "Пустое поле", ";".join(row)))
            else:
                valid.append(row)
        return valid, errors

    def _fill_results_table(self, rows: List[List[str]], header: List[str]):
        self.results_table.clear()
        if not rows:
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            self.results_label.setText("0 записей")
            return

        self.results_table.setRowCount(len(rows))
        self.results_table.setColumnCount(len(rows[0]))
        self.results_table.setHorizontalHeaderLabels(header)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.results_table.setItem(r, c, QTableWidgetItem(value))

        self.results_label.setText(f"{len(rows)} записей")

    def _fill_errors_table(self, errors: List[Tuple[int, str, str]]):
        self.errors_table.setRowCount(len(errors))
        for r, (line, msg, data) in enumerate(errors):
            self.errors_table.setItem(r, 0, QTableWidgetItem(str(line)))
            self.errors_table.setItem(r, 1, QTableWidgetItem(msg))
            self.errors_table.setItem(r, 2, QTableWidgetItem(data))
        self.errors_label.setText(f"{len(errors)} ошибок")


class ReferenceTab(QWidget):
    """
    Вкладка 'Справочник':
    - Выбор справочника (Персонал, Операции, Нормативы, Смены, Графики работы)
    - Выбор маршрута к БД
    - Кнопки Загрузить / Сохранить / Очистить
    - Таблица данных
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_route = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Справочник")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Строка выбора справочника
        form_box = QGroupBox("Справочники")
        form_layout = QFormLayout()

        self.combo_ref = QComboBox()
        self.combo_ref.addItems([
            "Персонал",
            "Операции",
            "Нормативы",
            "Смены",
            "Графики работы"
        ])

        form_layout.addRow("Справочник:", self.combo_ref)

        # Маршрут к БД (в примере будет путь к файлу/каталогу)
        route_layout = QHBoxLayout()
        self.route_edit = QLineEdit()
        self.route_edit.setReadOnly(True)
        btn_choose_route = QPushButton("Добавить маршрут БД")
        btn_choose_route.clicked.connect(self.choose_route)
        route_layout.addWidget(self.route_edit)
        route_layout.addWidget(btn_choose_route)

        form_layout.addRow("Маршрут к БД:", route_layout)

        form_box.setLayout(form_layout)
        main_layout.addWidget(form_box)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.btn_load = QPushButton("Загрузить")
        self.btn_save = QPushButton("Сохранить")
        self.btn_clear = QPushButton("Очистить")

        self.btn_load.clicked.connect(self.load_from_db)
        self.btn_save.clicked.connect(self.save_to_db)
        self.btn_clear.clicked.connect(self.clear_table)

        buttons_layout.addWidget(self.btn_load)
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # Таблица данных справочника
        self.table = QTableWidget(0, 0)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        main_layout.addStretch()

    def choose_route(self):
        # Упростим: пусть это путь к CSV для каждого справочника
        folder = QFileDialog.getExistingDirectory(self, "Выберите каталог БД")
        if folder:
            self.current_route = folder
            self.route_edit.setText(folder)

    def _get_current_ref_filename(self) -> str:
        """
        Для простоты считаем, что в каталоге лежат файлы:
        - персонал.csv
        - операции.csv
        - нормативы.csv
        - смены.csv
        - графики_работы.csv
        """
        if not self.current_route:
            return ""

        name = self.combo_ref.currentText()
        name_map = {
            "Персонал": "personal.csv",
            "Операции": "operations.csv",
            "Нормативы": "normatives.csv",
            "Смены": "shifts.csv",
            "Графики работы": "schedules.csv"
        }
        filename = name_map.get(name, "data.csv")
        return os.path.join(self.current_route, filename)

    def load_from_db(self):
        if not self.current_route:
            QMessageBox.warning(self, "Маршрут не выбран", "Выберите маршрут к БД.")
            return

        path = self._get_current_ref_filename()
        if not os.path.exists(path):
            # Нет файла — считаем, что пусто
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            QMessageBox.information(self, "Нет данных", "Файл справочника не найден, таблица очищена.")
            return

        try:
            rows, header = self._read_csv(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения", str(e))
            return

        self._fill_table(rows, header)

    def save_to_db(self):
        if not self.current_route:
            QMessageBox.warning(self, "Маршрут не выбран", "Выберите маршрут к БД.")
            return

        path = self._get_current_ref_filename()
        try:
            self._write_csv(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", str(e))
            return

        QMessageBox.information(self, "Сохранено", f"Данные сохранены в {path}")

    def clear_table(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

    def _fill_table(self, rows: List[List[str]], header: List[str]):
        self.table.clear()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(value))

    def _read_csv(self, path: str) -> Tuple[List[List[str]], List[str]]:
        rows = []
        header = []
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for i, row in enumerate(reader):
                if i == 0:
                    header = row
                else:
                    rows.append(row)
        return rows, header

    def _write_csv(self, path: str):
        rows = []
        cols = self.table.columnCount()
        header = []
        for c in range(cols):
            item = self.table.horizontalHeaderItem(c)
            header.append(item.text() if item else f"col{c+1}")

        for r in range(self.table.rowCount()):
            row = []
            for c in range(cols):
                item = self.table.item(r, c)
                row.append(item.text() if item else "")
            rows.append(row)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(header)
            writer.writerows(rows)


class SettingsTab(QWidget):
    """
    Заглушка под 'Настройки'.
    Можно расширить под твои реальные настройки.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title_label = QLabel("Настройки")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        layout.addWidget(QLabel("Здесь можно добавить параметры подключения, форматы файлов и др."))
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления фактами")
        self.resize(1000, 700)

        tabs = QTabWidget()
        tabs.addTab(FactsLoaderTab(), "Загрузка фактов")
        tabs.addTab(ReferenceTab(), "Справочник")
        tabs.addTab(SettingsTab(), "Настройки")

        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```

Если хочешь максимально точно повторить оригинал, напиши:

1) На чём это ПО работает сейчас (HTML у тебя, но сервер/JS/БД?). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/168548725/4e66afca-19e8-4abf-bff5-4f88a26acf42/RP_10.html?AWSAccessKeyId=ASIA2F3EMEYEUCIKGSME&Signature=U1ErADG63Xn5uOsUaHDrxT7AMvg%3D&x-amz-security-token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJHMEUCIB%2FyqQrpFxrxV5cON111CewY8CfEVAWbhV9%2FcR9Ic6wXAiEAyBPhdqd1K2P9RQMD%2BDOH%2B5%2Bq4ynHs3YptxQqP8excdAq%2FAQI8v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDK1Rey28YPoE0OPDWSrQBDXRtnb%2F0OunSv04w9lA7%2F4DsGT1kqKRh0OrfR9AJ3nCe%2BmsAxYVl3S7SKD1PzZWRjB0Z1BTYkIf9klMjhvKckgqs5aQWU37KP%2Bk1xQmt4xJFt7wgkOxTWCr987V1eaIjktLGjHqVJnkPm85ANJJrG6aSwPB4iXsmQLfgAXeSFgN%2FWMyOyXDUO1RVnVvYMLeve0oTKl%2BFSdi%2B73Vx5dVquPqqW0ZN9JHoH9Yl42eGN6vm5lH3BD8iN%2BmlFP2vnj718qux%2FWo4MAOPqNkssYG9bLvm810YS1McQZz%2BxohmsMiAD9dq8xLEYo8KAOaNUpo6XbwmznkOFeyciuUltBsQuJ20J%2FSyYSMS28k0Hdx45Wikw4J7jFZFfDtYkJRiWp3DiW0npvTxoqLqdXk2hJ27RoYCB0hZP2HOG20lVNM2OG76qQrdptKJ5UMMTy4uc8Dhi8sibOUuL2rAAHM%2BEN%2BLGaOIeHw0mojd8McZE2J7zDHQG5GtqlTmcFqfwhacjzMXyDN1Vc2lf6Lnr2a%2BNIu4sA%2BKiFIoIpEU0OeE2LpqZcHI1XynXEo5BTFJ549wBa3R8onaUsMS2XN6H4jmGwXpHIekJzfDo4FQA%2B6zn6z%2FsTf3gV%2FOL3Ba8a83x4x%2B5aVDcApIQKpz14Zs9D82ZRNYmAIiBHoifuULzEQGatseH9rBaqe0bL9hRGxrrBKz%2BtLKqAalIAle1b5WDOuIqRQ9UfBxoaP3C%2BbzO2pO1jW5UeYY0dET6N%2B13sIygBW1NrOYkw09L2TwDnonGMvYoNnj48w7pTmzQY6mAGFF8Xmo6414anJL%2BdpOyZJTvNe0PXHqX%2FJE%2F7tUNg6FhHKR8HHon8W72as4VSpYyxNxz4yqKZEDjJP2qzCFAeOjex8JoIHWsLWQNdIwo8pzpQrD%2BH8DAD2wISSwsYGRIKuSwWbya4nIPeCJANvtr%2BayylpjF6NG4AnsZ5toJtgmY27JRp3MS%2BkdChSAMbN98pgHXkDTknRAA%3D%3D&Expires=1773769527)
2) Какой формат файлов фактов и справочников (CSV/Excel, разделители, кодировка, структура). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/168548725/4e66afca-19e8-4abf-bff5-4f88a26acf42/RP_10.html?AWSAccessKeyId=ASIA2F3EMEYEUCIKGSME&Signature=U1ErADG63Xn5uOsUaHDrxT7AMvg%3D&x-amz-security-token=IQoJb3JpZ2luX2VjECoaCXVzLWVhc3QtMSJHMEUCIB%2FyqQrpFxrxV5cON111CewY8CfEVAWbhV9%2FcR9Ic6wXAiEAyBPhdqd1K2P9RQMD%2BDOH%2B5%2Bq4ynHs3YptxQqP8excdAq%2FAQI8v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDK1Rey28YPoE0OPDWSrQBDXRtnb%2F0OunSv04w9lA7%2F4DsGT1kqKRh0OrfR9AJ3nCe%2BmsAxYVl3S7SKD1PzZWRjB0Z1BTYkIf9klMjhvKckgqs5aQWU37KP%2Bk1xQmt4xJFt7wgkOxTWCr987V1eaIjktLGjHqVJnkPm85ANJJrG6aSwPB4iXsmQLfgAXeSFgN%2FWMyOyXDUO1RVnVvYMLeve0oTKl%2BFSdi%2B73Vx5dVquPqqW0ZN9JHoH9Yl42eGN6vm5lH3BD8iN%2BmlFP2vnj718qux%2FWo4MAOPqNkssYG9bLvm810YS1McQZz%2BxohmsMiAD9dq8xLEYo8KAOaNUpo6XbwmznkOFeyciuUltBsQuJ20J%2FSyYSMS28k0Hdx45Wikw4J7jFZFfDtYkJRiWp3DiW0npvTxoqLqdXk2hJ27RoYCB0hZP2HOG20lVNM2OG76qQrdptKJ5UMMTy4uc8Dhi8sibOUuL2rAAHM%2BEN%2BLGaOIeHw0mojd8McZE2J7zDHQG5GtqlTmcFqfwhacjzMXyDN1Vc2lf6Lnr2a%2BNIu4sA%2BKiFIoIpEU0OeE2LpqZcHI1XynXEo5BTFJ549wBa3R8onaUsMS2XN6H4jmGwXpHIekJzfDo4FQA%2B6zn6z%2FsTf3gV%2FOL3Ba8a83x4x%2B5aVDcApIQKpz14Zs9D82ZRNYmAIiBHoifuULzEQGatseH9rBaqe0bL9hRGxrrBKz%2BtLKqAalIAle1b5WDOuIqRQ9UfBxoaP3C%2BbzO2pO1jW5UeYY0dET6N%2B13sIygBW1NrOYkw09L2TwDnonGMvYoNnj48w7pTmzQY6mAGFF8Xmo6414anJL%2BdpOyZJTvNe0PXHqX%2FJE%2F7tUNg6FhHKR8HHon8W72as4VSpYyxNxz4yqKZEDjJP2qzCFAeOjex8JoIHWsLWQNdIwo8pzpQrD%2BH8DAD2wISSwsYGRIKuSwWbya4nIPeCJANvtr%2BayylpjF6NG4AnsZ5toJtgmY27JRp3MS%2BkdChSAMbN98pgHXkDTknRAA%3D%3D&Expires=1773769527)

Тогда адаптирую скрипт под твою реальную схему данных и бизнес‑правила (валидация, типы ошибок, поля справочников), чтобы он был практически один в один по функционалу.