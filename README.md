# Фреймворк для экосистемы Intera.SPACE

Предназначен для ускорения разработки MVP (минимальная рабочиая версия) микросервисов для экосистемы intera.space. Содержит общий шаблон, общую статику и некоторые вспомоготальные модули.

## Изменения в settings.py

Для использования фреймоврка необходимо добавить приложение `django_sy_framework.base` в `INSTALLED_APPS`

## Блоки общего шаблона

Подключение общего шаблона: `{% extends 'base/base.html' %}`

Имеют разное значение для разных страниц микросервиса:
- description - seo-описание страницы
- keywords - ключевые слова страницы
- page_title - заголовок страницы (отбражается в названии вкладки браузера)
- title - заголовок страницы (отображается на странице)
- content - содержимое страницы
- end_of_body - здесь, обычно, располагают скрипты

Имеют одинаковое значение для всех страниц микросервиса:
- site_title - заголовок сайта
- start_of_head - содержимое в начале тега HEAD. Обычно здесь размещаются скрипты для сбора статистики посещения сайта
- menu_items_microservice - навигационное меню микросервиса. Каждый пункт подключается так: `{% include "base/menu_microservice" with url_name="" url_title="" %}`
- source_code_link - ссылка на исходный код микросервиса. В формате `<a href="ссылка" target="_blank">Наименование (обычно - GitHub)</a>`
- menu_microservice_name - название навигационного меню микросервиса

## Обязательные шаблоны микросервиса, использующего фреймворк

В микросервисе обязательно присутствие следующих шаблонов, которые используются фреймворком:

- `pages/intro.html` - главная страница, в которую разработчик микросервиса помещает вводную информацию о микросервисе
- `template.html` - основной шаблон микросервиса, наследуемый от `base/base.html`