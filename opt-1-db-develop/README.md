# Домашние задание "Архитектура Кода"

## Введение

У нас есть онлайн аптека, которая позволяет покупать
- обычные (безрецептурные, в том числе простые товары вроде воды, которые к препаратам отношения не имеют),
- рецептурные (доступны любому врачу, либо пользователю у которого есть рецепт),
- специальные - доступны только для врачей конкретных специальностей например - товары для анестезиологов можно продавать только анестизиологам).

Создан отдельный сервис проверки корзины - на вход приходит запрос, который содержит id пользователя и список товаров, а в ответ выдается список позиций по которым есть проблемы. Данные о товарах и пользователях хранятся в локальной базе данных.

В сервисе есть обработчик запроса типа GET принимающий следующие парметры:

- `user_id` - Integer (айди врача или пользователя, он сквозной, т.е уникальный в рамках всей системы)
- `item_id` - список строковых значений вида `type_id` где: `type` - строковое описание типа товара, `id` - числовой идентификатор товара

Пример товара - `special_123`, `special` - тип, `123` - id, валидность структуры товара - гарантируется, валидность типа и идентификатора - нет, то есть
может прилететь товар вида ab12_qwerty.

`user_id` - гарантированно int, наличие в базе - не гаранитровано.

Пример запроса:
```curl
http://localhost:8080/check?user_id=123&item_id=special_26&item_id=common_25
```


Вся нужная информация будет лежать в базе данных.

> **Необходимы для инициализации базы данных в папке ./postgresql
> Схема нарисована в pharmacy_er.png, лежит там же где и readme, настоятельно рекомендую начать с ее изучения**.

Пользователи относятся к двум категориям - обычные пользователи и врачи, лежат в разных таблицах с разными схемами. Определение того, кем является пользователь уже есть в коде. Также уже есть добавление рецептов пользователя из таблицы рецептов.

Определение и проверка корректности входных данных(соответствует ли айдишник формату `type_id` и тому подобное уже есть). Получение товаров из базы также есть.

Категории товаров - обычные, рецептурные, специальные .

Обычные товары - `common`<br>
Рецептурные - `receipt`<br>
Специальные товары - тип `special`<br>

Товары хранятся в разных таблицах. Определить, где искать товар можно по типу (`special/common/receipt`). Из базы получается значение по id (целочисленная часть).

Список рецептов по пользователям реализован через промежуточную таблицу, связывающую рецептурные товары и пользователей.

В таблице специальных товаров описано к какой сфере они относятся (например, товары доступные к покупке только хирургам или только анестезиологам).

<details>
<summary>

**Запросы к базе (Обязательно посмотри!):**

</summary>


### Запрос для получения продуктов([ссылка на код](src/models/product.cpp#L41)):
```
SELECT * FROM code_architecture.{}_item WHERE id = $1;
```
Тут вместо `{}` подставляется один из трех типов товаров: `special/common/receipt`, а вместо `$1` подставляется уже отделенный от типа целочисленный id продукта.


### Запрос для получения обычных пользователей([ссылка на код](src/models/common_user.cpp#L28)):
```
SELECT * FROM code_architecture.user_account WHERE id = $1;
```
Тут вместо `$1` подставляется id пользователя. Если что-то получаем, значит человек- обычный пользователь.


### Запрос для получения рецептов пользователей([ссылка на код](src/models/common_user.cpp#L37)):
```
SELECT * FROM code_architecture.receipt WHERE user_id = $1;
```
Тут вместо `$1` подставляется id пользователя. Получаем список рецептов пользователя.


### Запрос для получения врачей([ссылка на код](src/models/common_user.cpp#L54)):
```
SELECT * FROM code_architecture.doctor_account WHERE id = $1;
```
Тут вместо `$1` подставляется id пользователя. Если что-то получаем, значит человек- врач. А получаем в том числе специальность врача.


</details>

**Возможные ситуации описаны ниже.**



Структура ответа:

```
200 OK
[
    {
        "item_id": string,
        "problem": string
    }
]
```

Формат `item_id` - такой же как на входе,  например, `common_123`. Если с товаром все окей, и с пользователем все окей, то ничего не возвращается. В ответ вписываются только проблемные товары и их причины.


**Обработка краевых случаев**

Для каждого вида ошибки использовать свой код в ответе.

Коды ошибок для ответов:


| Ошибка                                                                             |    Код ответа  (problem)    |
|------------------------------------------------------------------------------------|:---------------------------:|
| Ошибка парсинга входных данных                                                     |         WRONG_DATA          |
| Товар не найден (тип пользователя не важен)                                        |       ITEM_NOT_FOUND        |
| Пользователь не найден, товар можно продать                                        |           NO_USER           |
| Пользователь найден, товар рецептурный, у пользователя нет рецепта                 |         NO_RECEIPT          |
| Пользователь найден, товар спец. назначения                                        |       ITEM_IS_SPECIAL       |
| Пользователь врач, товар специальный, но не совпал по сфере работы врача           | ITEM_SPECIAL_WRONG_SPECIFIC |


##  Что надо сделать?

Необходимо описать стратегии валидации товаров - проверка рецептурных, проверка специальных товаров, и проверка простых товаров в зависимости от типа пользователя: врач или обычный пользователь.

Перед написанием стратегии валидации рекомендую ознакомится с Введением и с **Кодом задания**.

Сейчас в функциях IsProductValid намеренно неверная реализация. Исправьте ее и напишите свою.

**Про тесты**

Необходимым условием сдачи домашнего задания являются пройденые тесты. Также тесты помогут вам разобраться, что надо исправить в исходном коде.

## Download and Build

To create your own userver-based service follow the following steps:

1. Press the green "Use this template button" at the top of this github page
2. Clone the service `git clone your-service-repo && cd your-service-repo`
3. Feel free to tweak, adjust or fully rewrite the source code of your service.


## Makefile

Makefile contains typicaly useful targets for development:

* `make build-debug` - debug build of the service with all the assertions and sanitizers enabled
* `make build-release` - release build of the service with LTO
* `make test-debug` - does a `make build-debug` and runs all the tests on the result
* `make test-release` - does a `make build-release` and runs all the tests on the result
* `make service-start-debug` - builds the service in debug mode and starts it
* `make service-start-release` - builds the service in release mode and starts it
* `make` or `make all` - builds and runs all the tests in release and debug modes
* `make format` - autoformat all the C++ and Python sources
* `make clean-` - cleans the object files
* `make dist-clean` - clean all, including the CMake cached configurations
* `make install` - does a `make build-release` and runs install in directory set in environment `PREFIX`
* `make install-debug` - does a `make build-debug` and runs install in directory set in environment `PREFIX`
* `make docker-COMMAND` - run `make COMMAND` in docker environment
* `make docker-build-debug` - debug build of the service with all the assertions and sanitizers enabled in docker environment
* `make docker-test-debug` - does a `make build-debug` and runs all the tests on the result in docker environment
* `make docker-start-service` - does a `make install` and runs service in docker environment
* `make docker-start-service-debug` - does a `make install-debug` and runs service in docker environment
* `make docker-clean-data` - stop docker containers and clean database data

Edit `Makefile.local` to change the default configuration and build options.


## License

The original template is distributed under the [Apache-2.0 License](https://github.com/userver-framework/userver/blob/develop/LICENSE)
and [CLA](https://github.com/userver-framework/userver/blob/develop/CONTRIBUTING.md). Services based on the template may change
the license and CLA.
