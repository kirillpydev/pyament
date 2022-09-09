import asyncio

from client import ClientCloudpayments

client = ClientCloudpayments()


async def get_pay():
    async with client.create_session() as client_session:
        await client.yandex_auth(client_session=client_session)
        await client.get_crypto(client_session=client_session)
        await client.service_payment(client_session=client_session)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_pay())
