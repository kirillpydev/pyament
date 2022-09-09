# Тестовое задание на реализацию клиента к шлюзу Cloudpayments

Необходимо реализовать клиент на Python к [Cloudpayments API](https://developers.cloudpayments.ru/#api). В рамках задачи необходимо реализовать оплату по криптограмме (метод charge). Предполагается, что платежи будут проходить только [по токену Yandex Pay](https://developers.cloudpayments.ru/#platezhi-cherez-api-cloudpayments).

Требования:

- API клиента должно быть удобным для вызова из Python-кода.
- Реализовать аутентификацию запросов.
- Архитектура должна позволять добавлять остальные методы API.
- Рекомендуется использовать python >3.10,  marshmallow, marshmallow_dataclass, aiohttp >3.8.
- Реализация должна наследовать абстрактный класс `AbstractInteractionClient`.

___
- Реализация клиента **client.py**
- Пример использования экземпляра клиента **example.py**
- Пример переменных окружения
  ```
  YANDEX_APP_KEY=40cxbxxxxxfxxxbxbxdxxexfxxxxxxxx
  SERVICE_URL=https://oauth.yandex.ru/authorize
  BASE_URL=https://api.cloudpayments.ru/payments/
  RELATIVE_URL=charge
  ```
___

Для выполнения платежа необходимо получить токен в Yandex Pay и передать его в платежный шлюз CloudPayments.
![img.png](https://developers.cloudpayments.ru/images/scheme1-1d5affa2.png)

```
  async def yandex_auth(...):
      ...
```
Метод **yandex_auth()** аутентифицирует пользователя в Yandex Pay и перенаправляет по укзанному url в приложении. В нашем случае это страница `https://oauth.yandex.ru/verification_code`.
В продакшене это будет url со страницой ввода данных с карты.

![img.png](https://raw.githubusercontent.com/kirillpydev/pyament/1d2ea0c0495f502b95d065b5b7f2fb3759b5ad3b/img/yandex_redirect_url.png)

```
  async def get_crypto(...):
      ...
```
Метод **get_crypto()** получает криптограмму от Checkout-скрипта со страницы ввода данных с карты.

![img.png](https://raw.githubusercontent.com/kirillpydev/pyament/1d2ea0c0495f502b95d065b5b7f2fb3759b5ad3b/img/Checkout.png)

```
  async def yandex_auth(...):
      ...
```
Метод **service_payment()** отправляет POST запрос на конечную точку `https://api.cloudpayments.ru/payments/` с данными из примера:
```
  curl --location --request POST 'https://api.cloudpayments.ru/payments/charge' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "PublicId": "your_public_id",
      "Amount": 100,
      "Currency": "RUB",
      "Description": "A basket of oranges",
      "CardCryptogramPacket": "\"{\\\"type\\\":\\\"Yandex\\\",\\\"signedMessage\\\":\\\"{\\\\\\\"encryptedMessage\\\\\\\":\\\\\\\"xqpAiS2L71BZNgH514AQDwOVawJF4gHXF8P+ECIFRqFHlDMRtxHsO9hNQSeegSssRdDMlBIyOObY5dqI3iwX99UKYP6qFD+tKEYJQkUdiKyhZCwgUsVdHBlFQA+iiXVLf7DZ5WCIaHjpl4mckrGeDg4XGDIX4FB0BorLqocbDLcl0JZi2zzkNtn9FDLPSAs1qbTEMdb3TAS0iDAIkuAy5DGJ3+4Av9PWvIllW4LRdQ34rR8MPszJxq9Xagw/jeKUglyUERQgi5cnVWIB992yPh9UFgNuCQBc+JWLMzuOIKKxFiVK6VBSsuHpDWrSZqMolN6PIeNvETxQ34g+O/u4KiwWd3IG/pb5e0FYbzn/gWzlDSPsqNSuB713qZDHCI7eFB7h7iPTdk/Wd78Vv7Vlg4oVQdMWCbgSjtWDamKeq/OMiVDW5j36CebRQWxB8/XFj4nAInHIjoUUKsEQ5gf00n9/48RUNVCbRr6qykvsfnD0XP5V4OJOeIhAZN2CAgGxgrGC5MibfjAf+D/EnunHwOvtmI6KQAsGv9QgrRC8sxTeyk7OT9vUCzK2DIRDYyCtvloGalRq1PRdJWQX\\\\\\\",\\\\\\\"tag\\\\\\\":\\\\\\\"LTx6/HA9iWaZwbYaFN1j9aDOPp2PBlR2iBMUBQ7zyUg=\\\\\\\",\\\\\\\"ephemeralPublicKey\\\\\\\":\\\\\\\"BHHBcT4SvFgxMK14Oz3/dk/uiCL2m4jeTFDEcoYHXt5gAz2wFVEnvRD4fHArkbIOcry9nlUYHWgT4GicEl9qkXY=\\\\\\\"}\\\",\\\"protocolVersion\\\":\\\"ECv2\\\",\\\"signature\\\":\\\"MEUCICyyzWnCEf2iHlUszDzvbAx/qk/sLmbTaOWPVEq1hr29AiEA0lfZ85pCofYhxVX971Xtshysawi7+KEe8ZpPVlV/Md4=\\\",\\\"intermediateSigningKey\\\":{\\\"signedKey\\\":\\\"{\\\\\\\"keyValue\\\\\\\":\\\\\\\"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEqYNePt6BPgCv5JxfO9dF2vrSqmnp4Mhe/vF+XO+Devbs6/KVpVVoTD8LLcAo4TZh6IuODVnVpHrTObhg3HJVJA==\\\\\\\",\\\\\\\"keyExpiration\\\\\\\":\\\\\\\"1764950892000\\\\\\\"}\\\",\\\"signatures\\\":[\\\"MEQCIDRslMW7wNZbpqVw/dD7hDQh30hGhqfjfWTBvc7zAYJSAiAGAvjAslA2AxwdAEuOfacFr6DaE5yiiUuUtM6DUreZYg==\\\"]}}\""
}'
```
и получет результат запроса:
```
{"Success":false,"Message":"Терминал не найден"}
```
![img.png](https://github.com/kirillpydev/pyament/blob/img/img/auth.png?raw=true)