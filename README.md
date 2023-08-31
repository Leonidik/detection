## Detection project

Содержание: detection_project_folder  
  - server
  - README.md  
  - requirements.txt  

Установка:  
  - cd detection_project_folder  
  - virtualenv env  
  - source env/bin/activate  
  - pip install -r requirements.txt
  - Скачать содержимое папки get_video по ссылке  
  - Скопировать папку media (с содержимым) по ссылке  
  https://drive.google.com/drive/folders/1C4cSx95pDNDICYw3qLyEcqMKRcDG8u3o?usp=sharing  
и перенести ее в папку проекта: detection/server/ (detection/server/media)  
  
Запуск:
  - cd detection_project_folder  
  - virtualenv env  
  - source env/bin/activate  
  - cd server  
  - python manage.py runserver  
  - http://127.0.0.1:8000/
  
После певого завуска в директории server появится файл yolov5x.pt  
   






