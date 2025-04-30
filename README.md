
# Проект: API Registration: Points System Project Description

## Цель

Цель данного проекта — разработка системы баллов с использованием FastAPI. Система позволяет пользователям регистрироваться, получать баллы, передавать их между пользователями, проверять баланс, участвовать в рынке, а также управлять пользователями через административную панель.

## Описание решения

Решение представляет собой приложение на базе FastAPI, которое реализует функциональность системы баллов. Включает регистрацию пользователей с начальным балансом в 100 баллов, передачу баллов между пользователями, проверку баланса, а также создание и принятие заявок на рынке. Также предусмотрены административные функции для управления пользователями и пополнения баланса.

### Точки входа в заявку

Пользователи могут зарегистрироваться в системе, создавая учётную запись с начальным балансом в 100 баллов. После этого им доступны функции перевода баллов, проверки баланса, а также возможности участвовать в рынке.

### Анкета нативной заявки

Каждый пользователь должен пройти процедуру регистрации, указав необходимые данные для создания учётной записи, после чего он получит 100 баллов на свой счёт.

### Выдача (подходящие мастера)

Система автоматически предоставляет пользователям доступ к функционалу перевода баллов, проверки баланса и участия в рыночных заявках, а также отображает пользователям список доступных лидеров на основе их баланса.

### Заказ

В рамках рыночной функции, пользователи могут создавать заявки для предложения товаров или услуг, а другие пользователи могут их принимать, используя свои баллы для оплаты.

### Участие объявлений в Заявках

Возможность для пользователей размещать объявления в рамках рыночных заявок для покупки и продажи товаров или услуг, что предоставляет систему для обмена баллами между пользователями.

### Текущий эксперимент

Проект использует эксперименты в развертывании Docker-контейнеров для проверки и улучшения производительности приложения, а также для тестирования различных конфигураций.

## Схема высокоуровневой архитектуры


## 1. **User Registration Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/register`

**Description:**

Allows users to register and create an account with an initial balance of 100 points.

---

## 2. **User Login Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/login`

**Description:**

Allows users to log in by providing their credentials. Returns an authentication token for future requests.

---

## 3. **Points Transfer Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/transfer`

**Description:**

Allows users to transfer points to another user. Ensures the user has enough points before transferring.

---

## 4. **Check User Balance Endpoint**

**HTTP Method:** `GET`

**Endpoint:** `/balance`

**Description:**

Allows users to check their current balance of points.

---

## 5. **Marketplace Listing Creation Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/marketplace/listings`

**Description:**

Allows users to create a marketplace listing offering products or services in exchange for points.

---

## 6. **Accept Marketplace Listing Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/marketplace/accept`

**Description:**

Allows users to accept a marketplace listing and transfer points to the seller.

---

## 7. **Admin User Management Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/admin/users/manage`

**Description:**

Allows administrators to manage user accounts, including adding points or suspending accounts.

---

## 8. **Admin Balance Top-Up Endpoint**

**HTTP Method:** `POST`

**Endpoint:** `/admin/top-up`

**Description:**

Allows administrators to top up the balance of a user by adding points to their account.

---

This is the more concise version of the API endpoints in markdown format. If you need to save this as a `.md` file, let me know!

##### Вы сказали:

сделай что-то на русском, напрмер названия, слово методы и тд

###### ChatGPT сказал:

Here’s the updated version of the API endpoints in markdown format with the terms translated into Russian:

---

# Эндпоинты API

## 1. **Эндпоинт регистрации пользователя**

**Метод HTTP:** `POST`

**Эндпоинт:** `/register`

**Описание:**

Позволяет пользователям зарегистрироваться и создать учетную запись с начальным балансом в 100 баллов.

---

## 2. **Эндпоинт входа пользователя**

**Метод HTTP:** `POST`

**Эндпоинт:** `/login`

**Описание:**

Позволяет пользователям войти в систему, предоставив свои учетные данные. Возвращает токен аутентификации для дальнейших запросов.

---

## 3. **Эндпоинт перевода баллов**

**Метод HTTP:** `POST`

**Эндпоинт:** `/transfer`

**Описание:**

Позволяет пользователям переводить баллы другому пользователю. Проверяет наличие достаточного количества баллов перед переводом.

---

## 4. **Эндпоинт проверки баланса пользователя**

**Метод HTTP:** `GET`

**Эндпоинт:** `/balance`

**Описание:**

Позволяет пользователям проверять текущий баланс баллов.

---

## 5. **Эндпоинт создания объявления на рынке**

**Метод HTTP:** `POST`

**Эндпоинт:** `/marketplace/listings`

**Описание:**

Позволяет пользователям создать объявление на рынке для обмена товаров или услуг на баллы.

---

## 6. **Эндпоинт принятия объявления на рынке**

**Метод HTTP:** `POST`

**Эндпоинт:** `/marketplace/accept`

**Описание:**

Позволяет пользователям принять объявление на рынке и перевести баллы продавцу.

---

## 7. **Эндпоинт управления пользователями для администратора**

**Метод HTTP:** `POST`

**Эндпоинт:** `/admin/users/manage`

**Описание:**

Позволяет администраторам управлять учетными записями пользователей, включая добавление баллов или приостановку учетных записей.

---

## 8. **Эндпоинт пополнения баланса для администратора**

**Метод HTTP:** `POST`

**Эндпоинт:** `/admin/top-up`

**Описание:**

Позволяет администраторам пополнить баланс пользователя, добавив баллы на его счет.
