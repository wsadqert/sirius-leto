# Приложение для проведения цифровых лабораторных работ по физике

[![wakatime](https://wakatime.com/badge/user/ede740b4-c066-46b1-94e3-8631a44edbbc/project/018b0187-680c-48ce-b3d4-16bcf0fbf84e.svg)](https://wakatime.com/badge/user/ede740b4-c066-46b1-94e3-8631a44edbbc/project/018b0187-680c-48ce-b3d4-16bcf0fbf84e)
[![GoogleDrive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1-Oqx2IdPqcgg-u9oRI-xCeQbWxEPKi7N?usp=drive_link)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wsadqert/sirius-leto)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

Текущий прогресс по задачам вы можете отслеживать на [Github Issues](https://github.com/) и [YouGile](https://ru.yougile.com/board/rmuccfl32i52).

## Варианты запуска

К сожалению, мы не успели реализовать совместную работу общего графического интерфейса с `matplotlib`, поэтому временно есть только возможность отдельного запуска одного и другого.

**Внимание:** временно поддерживается Python только версии 3.12. Для его установки необходимо скачать любую поддерживаемую версию с сайта [https://www.python.org/downloads/](https://www.python.org/downloads/).

Для запуска программы необходимо сначала склонировать [репозиторий](https://github.com/wsadqert/sirius-leto) с GitHub на локальный компьютер, создать виртуальное окружение (по желанию, но рекомендуется), установить все [зависимости](https://github.com/wsadqert/sirius-leto/network/dependencies).

Для подготовки к запуску программы необходимо выполнить следующее:
```bash
git clone https://github.com/wsadqert/sirius-leto.git
cd sirius-leto
python -m venv venv/
./Scripts/activate.bat
pip install -r requirements.txt
```
Далее, для запуска программы с графическим интерфейсом введите:
```bash
python ./main_gui.py
```
А для непосредственного запуска лаборатории выполните:
```bash
python ./main.py
```

Готовые бинарные сборки вы можете найти на странице [Releases](https://github.com/wsadqert/sirius-leto/releases/). При желании вы можете самостоятельно скомпилировать исходный код в исполняемый файл. Специально для этого были подготовлены файлы `build.ps1` и `build.bat`. Любой из них достаточно просто выполнить, они делают одно и то же.

Для просмотра скомпилированной документации необходимо запустить HTTP-сервер:
```bash
cd ./docs/server
python -m http.server 8888
```
Либо можете воспользоваться аналогичным пакетом [http-server](https://www.npmjs.com/package/http-server?activeTab=readme) из NPM:
```bash
npm install -g http-server
http-server . -p 8888
```
Порт можно поменять на своё усмотрение, главное – не забыть его изменить и в URL-адресе. Для открытия документации введите в адресной строке браузера одну из следующих ссылок:

- [http://localhost:8888](http://localhost:8888)
- [http://127.0.0.1:8888](http://127.0.0.1:8888)

## Issues

Все известные баги вы можете отслеживать на [соответствующей странице проекта](https://github.com/wsadqert/sirius-leto/issues) на GitHub.

## Файловая структура:

Каждая лаборатория будет иметь так называемый ID, состоящий из латинских букв, цифр и специальных символов. Идентификаторы уникальны, то есть 2 разные лаборатории не могут иметь одинаковые идентификаторы. Может использоваться условное обозначение `<lab_ID>`

- [`assets/`](assets_README.md) - хранилище ресурсов.

- `datastore/` - папка со сгенерированными данными и ничего больше.
    - `datastore/<lab_ID>/*.*` - сгенерированный датасет. Может иметь немалый объём, да и не представляет ценности с точки зрения версионирования, поэтому такие файлы не будут доступны через github, вместо них будут файлы-"заглушки".
    - `datastore/<lab_ID>/__data_placeholder.txt` - файл-"заглушка" с текстом [Lorem Ipsum](https://www.lipsum.com/).
    - `datastore/<lab_ID>/README.md` - `Markdown`-файл, описывающий структуру данных в конкретном датасете.


- `src/` - папка со всеми исходниками. Недопустимо помещать исходники в другие папки (исключением является директория `src_drafts/`, которая описана ниже)
    - `src/<lab_ID>/README.md` - содержит информацию о конкретной лаборатории (описание, теоретическое обоснование, входные/получаемые данные, полезные ссылки и т.д.)
    - `src/<lab_ID>/__init__.py` - определяет, что папку `src/<lab_ID>/` можно использовать как библиотеку. Обязательно содержит только один доступный извне объект -  функцию `start(...)`.
    - `general/` - содержит файлы, такие как списки констант и базовые математические расчёты, которые необходимы для работы всем (или многим нескольким) лабораториям.


- `src_drafts/` - здесь помещены исходники, которые временно не используются. Обычно, здесь будет находиться. Так, здесь могут находиться куски кода со StackOverFlow или заготовки будущих лабораторий.


- `main.py` - основной файл, содержащий все доступные лаборатории. Именно он должен выполняться, когда пользователь захочет воспользоваться приложением.
