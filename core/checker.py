import asyncio

import aiohttp
from eth_account import Account
from loguru import logger
from tenacity import retry
from web3.auto import w3

from utils import append_file
from utils import get_proxy
from utils import loader

Account.enable_unaudited_hdwallet_features()


def log_retry_error(retry_state):
    logger.error(retry_state.outcome.exception())


class Checker:
    def __init__(self,
                 client: aiohttp.ClientSession,
                 account_address: str,
                 account_data: str):
        self.client: aiohttp.ClientSession = client
        self.account_address: str = account_address
        self.account_data: str = account_data

    @retry(after=log_retry_error)
    async def _get_eoa_address(self) -> str:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await self.client.post(
                url=f'https://rpc.particle.network/evm-chain',
                proxy=get_proxy(),
                params={
                    'chainId': '204',
                    'projectUuid': '64c673d8-30bd-4e02-8be4-f9c5531a79a5',
                    'projectKey': 'cwTncilkSkASDvXWHC6LAfj3UnJOSb0vWmdXmS9C',
                    'method': 'particle_aa_getSmartAccount'
                },
                json={
                    'chainId': 204,
                    'id': 1733940579286795,
                    'jsonrpc': '2.0',
                    'method': 'particle_aa_getSmartAccount',
                    'params': [
                        {
                            'name': 'BICONOMY',
                            'version': '2.0.0',
                            'ownerAddress': self.account_address.lower()
                        }
                    ]
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return response_json['result'][0]['smartAccountAddress']

        except Exception as error:
            raise Exception(
                f'{self.account_address} | Unexpected Error When Getting EOA address: {error}'
                + (f', response: {response_text}' if response_text else '')
            ) from error

    @retry(after=log_retry_error)
    async def _get_balance(self) -> float:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await self.client.get(
                url=f'https://app.usual.money/api/points/{self.account_address}'
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            if response_json.get('statusCode', 0) == 500:
                return 0

            return int(response_json['amount']) / 10 ** 18

        except Exception as error:
            raise Exception(
                f'{self.account_address} | Unexpected Error When Checking Eligible: {error}'
                + (f', response: {response_text}' if response_text else '')
            ) from error

    async def balance_checker(self) -> None:
        account_balance: float = await self._get_balance()

        if account_balance <= 0:
            logger.error(f'{self.account_address} | Not Eligible')
            return

        logger.success(f'{self.account_address} | {self.account_data} | {account_balance:.10f} $USUAL')

        async with asyncio.Lock():
            await append_file(
                file_path='result/with_balances.txt',
                file_content=f'{self.account_address} | {self.account_data} | {account_balance:.10f} $USUAL\n'
            )


async def check_account(
        client: aiohttp.ClientSession,
        account_data: str
) -> None:
    async with loader.semaphore:
        account_address: None = None

        try:
            account_address: str = Account.from_key(private_key=account_data).address

        except Exception:
            pass

        if not account_address:
            try:
                account_address: str = Account.from_mnemonic(mnemonic=account_data).address

            except Exception:
                pass

        if not account_address:
            try:
                account_address: str = w3.to_checksum_address(value=account_data)

            except Exception:
                pass

        if not account_address:
            logger.error(f'{account_data} | Not Mnemonic and not PKey')
            return

        checker: Checker = Checker(
            client=client,
            account_address=account_address,
            account_data=account_data
        )

        return await checker.balance_checker()
