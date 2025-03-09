Команды для работы с проектом:

    Для настройки среды (запуск скрипта):
     - bash setup_venv.bash

    Для генерации файлов ship_model_pb_2.py, содержащий классы представляющие сообщения на основе схемы protobuf в файле ship_model.proto и файл ship_model_pb_2.pyб содержащий инструменты для работы с grpc:
     - python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ships_model.proto

    Для запуска клиента с помощью ./ (соответствующих версий):
     - chmod +x reporting_client.py
     - ./reporting_client.py 17 45 40.0409 -29 00 28.118

    Для обработки миграций с помощью alemblic:

        Мигрировать к версии в добавлением колонки speed:
          - alembic upgrade add_speed

        Откатиться на 1 миграию:
          - alembic downgrade -1

        просмотреть историю миграций:
          - alembic history --verbose

        Проверить наличие колонки speed используй запрос:
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'spaceships' AND column_name = 'speed';
            или
            SELECT *
            FROM spaceships;