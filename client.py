import json
from typing import ClassVar, Optional

from aiohttp import ClientSession, TCPConnector

from abstract_client import AbstractInteractionClient, InteractionResponseError
from dotenv import dotenv_values

env = dotenv_values(".env")


class ClientCloudpayments(AbstractInteractionClient):
    CONNECTOR: ClassVar[TCPConnector] = TCPConnector(ssl=False)

    REQUEST_TIMEOUT: ClassVar[Optional[float]] = 10
    CONNECT_TIMEOUT: ClassVar[Optional[float]] = 600

    SERVICE: ClassVar[str] = env['SERVICE_URL']
    BASE_URL: ClassVar[str] = env['BASE_URL']
    RELATIVE_URL: ClassVar[str] = env['RELATIVE_URL']
    REQUEST_RETRY_TIMEOUTS = (0.1, 0.2, 0.4)

    YANDEX_APP_KEY: ClassVar[str] = env['YANDEX_APP_KEY']
    CARD_DATA: dict

    async def yandex_auth(self, client_session: ClientSession, response_type: str = "code") -> None:
        """Client auth & redirect to pay service "payments/cards/charge"
        response_type - for debug redirect to yandex page with code
        """

        params = {
            "client_id": self.YANDEX_APP_KEY,
            "response_type": response_type
        }

        response = await client_session.get(url=self.SERVICE, params=params)

        if response.status != 200:
            raise InteractionResponseError(
                status_code=response.status,
                method=response.method,
                service=self.SERVICE,
                params=params
            )

        print("Yandex auth:", response.status)

    async def get_crypto(self, client_session: ClientSession) -> None:
        """
        1. The client is redirected to the card data entry page & create a cryptogram
        2. Client receives the code
        example code: 9919675
        """

        # card_data_form = {}
        # url = "redirected service payment url" this url set in Yandex app service
        # await client_session.post(url=url, data=card_data_form)

        # hardcode CARD_DATA from card data entry page
        with open('fixtures') as card:
            self.CARD_DATA = json.loads(card.read())

    async def service_payment(self, client_session: ClientSession) -> None:
        """
        :return: {"Success":false,"Message": "Терминал не найден"} because need PublicId for Cloudpayments API
        """
        endpoint_url = self.endpoint_url(base_url_override=self.BASE_URL, relative_url=self.RELATIVE_URL)
        response = await client_session.post(url=endpoint_url, data=self.CARD_DATA)
        answer = await response.text()
        if response.status != 200:
            raise InteractionResponseError(
                status_code=response.status,
                method=response.method,
                service=endpoint_url,
                message=answer
            )

        print("Service payment status:", response.status)
        print("Service payment response:", answer)
