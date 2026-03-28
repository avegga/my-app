from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

out_path = Path('user_guide.docx')

paragraphs = [
    ('Пользовательское описание приложения «Загрузка фактов»', True),
    ('1. Назначение приложения', False),
    ('Приложение предназначено для загрузки CSV-файлов с фактами, проверки корректности данных, просмотра справочников и выполнения анализа производительности и простоев.', False),
    ('2. Запуск', False),
    ('1) Запустите локальный сервер командой: python main.py', False),
    ('2) Откройте в браузере: http://127.0.0.1:8000/RP_10.html', False),
    ('3. Вкладки интерфейса', False),
    ('- Загрузка фактов: импорт CSV, отображение корректных строк и ошибок, сохранение результата.', False),
    ('- Справочник: просмотр personal.csv, works.csv, norma.csv; редактирование norma_prostoy.csv с сохранением изменений.', False),
    ('- Анализ: разделы Простои, Производ, Производ (мин), Рейтинг, Приход/Уход с фильтрами.', False),
    ('- Настройки: выбор и добавление маршрута к папке БД.', False),
    ('4. Формат входного CSV', False),
    ('Файл должен содержать минимум 3 строки: заголовки, типы, далее данные. Разделитель полей: точка с запятой (;).', False),
    ('Поддерживаемая валидация типов: string/text, datetime/date, integer, decimal/float/double, boolean.', False),
    ('5. Работа с ошибками', False),
    ('Ошибки показываются в нижней таблице: номер строки, описание, фрагмент и подсказка по исправлению.', False),
    ('6. Сохранение результатов', False),
    ('Кнопка Сохранить формирует файл вида success_data_YYYYMMDD_HHMMSS.csv.', False),
    ('7. Работа со справочниками', False),
    ('Для чтения и записи справочников сначала выберите маршрут БД во вкладке Настройки.', False),
    ('Нормы простоя (norma_prostoy.csv) редактируются в таблице и сохраняются кнопкой Сохранить изменения.', False),
    ('8. Аналитика', False),
    ('Доступны фильтры по сотруднику, году, месяцу, работе, часу и дате.', False),
    ('Для режима простоев задайте Часы с и Часы по в формате ЧЧ:ММ:СС и нажмите Отобразить.', False),
    ('9. Ограничения', False),
    ('Для прямой работы с папкой БД рекомендуется браузер с поддержкой showDirectoryPicker.', False),
]


def p_xml(text, bold=False):
    t = escape(text)
    if bold:
        return f'<w:p><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
    return f'<w:p><w:r><w:t xml:space="preserve">{t}</w:t></w:r></w:p>'

body = ''.join(p_xml(t, b) for t, b in paragraphs)

document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" mc:Ignorable="w14 w15 wp14">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
      <w:cols w:space="708"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>
'''

content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
'''

rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'''

core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>Пользовательское описание приложения</dc:title>
  <dc:creator>GitHub Copilot</dc:creator>
</cp:coreProperties>
'''

app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
'''

with ZipFile(out_path, 'w', ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types)
    zf.writestr('_rels/.rels', rels)
    zf.writestr('docProps/core.xml', core)
    zf.writestr('docProps/app.xml', app)
    zf.writestr('word/document.xml', document_xml)

print('Created', out_path.resolve())
