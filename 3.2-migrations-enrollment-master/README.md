# Шаблон пайлайна для интеграции с ЛМС

### Как работает?

1. Тегрирует запуск пайпалйна с SOLUTION_ID
2. Клонирует репозиторий студента git@git.yandex-academy.ru:$ENROLLMENT_REPO_PATH/$REPO_NAME.git
3. Запускает тестовый пайпалйн test.gitlab-ci.yml который запускай run_test.py и reporter.py
