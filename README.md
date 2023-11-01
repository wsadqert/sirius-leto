# Приложение для проведения цифровых лабораторных работ по физике

[![wakatime](https://wakatime.com/badge/user/ede740b4-c066-46b1-94e3-8631a44edbbc/project/018b0187-680c-48ce-b3d4-16bcf0fbf84e.svg)](https://wakatime.com/badge/user/ede740b4-c066-46b1-94e3-8631a44edbbc/project/018b0187-680c-48ce-b3d4-16bcf0fbf84e)
[![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1-Oqx2IdPqcgg-u9oRI-xCeQbWxEPKi7N?usp=drive_link)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wsadqert/sirius-leto)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

## Issues

Все известные баги вы можете отслеживать на [соответствующей странице проекта](https://github.com/wsadqert/sirius-leto/issues) на GitHub.

[![GitHub](https://img.shields.io/badge/Issues-100000?style=for-the-badge&logo=GitHub&logoColor=white&labelColor=black&color=black)](https://github.com/wsadqert/sirius-leto/issues)

## Файловая структура:

<span style="color:yellow">Если что-то не сходится, это ок. В таком случае стоит чекнуть первые строчки файла `.gitignore`. Если там ничего подходящего нет, значит структура файлов уже поменялась, а обновить `README.md` и документацию не успели, и стоит просто подождать (или самому взять, дописать ^_^ и сделать pull request) </span>.

- [`datastore/`](datastore) - папка со сгенерированными данными и ничего больше.
  - `datastore/<lab_ID>/` - имена подпапок — это так называемые ID лабораторий. Они уникальны, то есть 2 разные лаборатории не могут иметь одинаковые идентификаторы.
    - `datastore/<lab_ID>/*/` - папки содержать различные вариации лаборатории, но формат данных обычно у них одинаковый. Подробности уточнять в соответствующем readme.
    - `datastore/<lab_ID>/data.dat` - сгенерированный датасет. Может иметь немалый объём, да и не представляет ценности с точки зрения версионирования, поэтому такие файлы не будут доступны через github, вместо них будут файлы-"заглушки" с именем 
    - `datastore/<lab_ID>/__data_placeholder.txt` и содержанием типа [Lorem Ipsum](https://www.lipsum.com/).
    - `datastore/<lab_ID>/README.md` - readme-файл, описывающий структуру данных в конкретном датасете.


- [`src/`](src) - папка со всеми исходниками. Недопустимо помещать исходники в другие папки (исключением является директория [`src_drafts`](src_drafts), которая описана ниже)
  - `src/<lab_ID>/` - имена подпапок — это ID лабораторий. 
    - `src/<lab_ID>/README.md` - содержит информацию о конкретной лаборатории (описание, входные/получаемые данные, полезные ссылки и т.д.)
    - `src/<lab_ID>/__init__.py` - определяет, что папку `src/<lab_ID>/` можно использовать как библитеку. Должен содержать функцию `start(...)`.
  - [`src/general/`](src/general) - содержит файлы, такие как списки констант и базовые математические расчёты, которые необходимы для работы всем (или многим нескольким) лабораториям.


- [`src_drafts/`](src_drafts) - здесь помещены исходники, которые временно не являются необходимыми. Так, здесь могут находиться куски кода со StackOverFlow или заготовки будущих лабораторий.
  - `src_drafts/<lab_ID>/` - имена подпапок — это ID лабораторий.


- [`.editorconfig`](.editorconfig) - как следует из названия, конфигурационный файл для редактора. Формат [EditorConfig](https://editorconfig.org/) является универсальным, и поддерживается большинством сред разработки. <b> Не следует изменять без необходимости. </b> При публикации на github наличие файла не гарантируется.
- [`.gitignore`](.gitignore) - думаю, не нуждается в комментариях (здесь же все люди шарят за git, правда?).
- [`main.py`](main.py) - основной файл, содержащий все доступные лаборатории. Именно он должен выполняться, когда пользователь захочет воспользоваться приложением.
