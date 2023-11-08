import aiohttp
from json import loads

class CrystalPay:
    def __init__(self, secret_key, login):
        """
        secret_key str: секретный ключ от кассы
        """
        self.__secret = secret_key
        self.__login = login

    async def __make_request(self, url, json_data, headers={"Content-Type": "application/json"}):
        """
        Функция, которая делает асинхронный запрос.

        Parameters:
        url str: ссылка на сайт
        json_data dict: данные в формате JSON для отправки
        headers dict: заголовки при запросе на сайт
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=headers) as response:
                return await response.text()
    
    async def method_list(self):
        """
        Получение информации о кассе
        """
        json_data = {"auth_login": self.__login, "auth_secret": self.__secret}
        return loads(await self.__make_request("https://api.crystalpay.io/v2/method/list/", json_data))

    async def cassa_balance(self, hide_empty=False):
        """
        Получение баланса с кассы

        hide_empty bool: скрывать или не скрывать пустые счета
        """
        json_data = {"auth_login": self.__login, "auth_secret": self.__secret, "hide_empty": hide_empty}
        return loads(await self.__make_request("https://api.crystalpay.io/v2/balance/info/", json_data))

    async def create_invoice(self, amount, type, lifetime, amount_currency="USD", required_method="BITCOIN", description=None, \
                             redirect_url=None, callback_url=None, extra=None, payer_details=None):
        """
        Функция которая выставляет счет

        amount int: сумма счета (автоматически станет в рублях)
        type str: тип инвойса, возможные варианты: purchase, topup
        lifetime int: время жизни инвойса в минутах, максимум - 4320
        amount_currency str: автоматически конвертируется в рубли, например: USD, BTC, ETH
        required_method str: заранее выбранный метод для оплаты, например: LZTMARKET, BITCOIN
        description str: описание в счете
        redirect_url str: ссылка для перенаправления после оплаты
        callback_url str: ссылка для HTTP Callback уведомления после успешной оплаты
        extra str: любые внутренние данные, например: ID платежа в вашей системе
        payer_details str: email плательщика
        
        Про типы инвойса: https://docs.crystalpay.io/api/oplata/vystavlenie-schyota и нажать на "Подробнее о type"
        """
        json_data = {"auth_login": self.__login, "auth_secret": self.__secret, "amount": amount, "type": type, \
                     "lifetime": lifetime, "amount_currency": amount_currency, "required_method": required_method, \
                     "description": description, "redirect_url": redirect_url, "callback_url": callback_url, \
                     "extra": extra, "payer_details": payer_details}
        return loads(await self.__make_request("https://api.crystalpay.io/v2/invoice/create/", json_data))
    
    async def invoice_info(self, invoice_id):
        json_data = {"auth_login": self.__login, "auth_secret": self.__secret, "id": invoice_id}
        return loads(await self.__make_request("https://api.crystalpay.io/v2/invoice/info/", json_data))
    