from sdk.CrystalPay import CrystalPay
import asyncio
from time import sleep

async def main():
    cp = CrystalPay("секретны ключ", "логин с кассы")

    response = await cp.create_invoice(100, "purchase", 1000)
    print(response['url'])
    while True:
        result = await cp.invoice_info(response['id'])
        print(result['state'])
        if response['state'] == "payed":
            print("Счет успешно оплачен")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())