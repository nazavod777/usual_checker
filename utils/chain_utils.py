from copy import deepcopy

import aiohttp
from eth_abi import encode
from loguru import logger
from web3.auto import w3

from data import config


async def get_gwei(provider_client: aiohttp.ClientSession) -> tuple[int, int, int]:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                params={
                    'chainId': '204',
                    'projectUuid': '64c673d8-30bd-4e02-8be4-f9c5531a79a5',
                    'projectKey': 'cwTncilkSkASDvXWHC6LAfj3UnJOSb0vWmdXmS9C',
                    'method': 'particle_getTokensAndNFTs'
                },
                json={
                    'jsonrpc': '2.0',
                    'id': 'f1804dae-2c52-4773-b624-8901eddca19b',
                    'method': 'particle_suggestedGasFees',
                    'params': []
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return (
                int(float(response_json['result']['baseFee']) * 10 ** 9),
                int(float(response_json['result']['high']['maxPriorityFeePerGas']) * 10 ** 9),
                int(float(response_json['result']['high']['maxFeePerGas']) * 10 ** 9)
            )

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting GWEI: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting GWEI: {error}')


async def get_chain_id(provider_client: aiohttp.ClientSession) -> int:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_chainId',
                    'params': [],
                    'id': 1
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(str(response_json['result']), 0)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting Chain ID: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting Chain ID: {error}')


async def get_nonce(provider_client: aiohttp.ClientSession,
                    address: str) -> int:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                params={
                    'chainId': '204',
                    'projectUuid': '64c673d8-30bd-4e02-8be4-f9c5531a79a5',
                    'projectKey': 'cwTncilkSkASDvXWHC6LAfj3UnJOSb0vWmdXmS9C',
                    'method': 'particle_getTokensAndNFTs'
                },
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_getTransactionCount',
                    'params': [
                        w3.to_checksum_address(value=address),
                        'pending'
                    ],
                    'id': 1
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(str(response_json['result']), 0)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting Nonce: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting Nonce: {error}')


async def get_last_block(provider_client: aiohttp.ClientSession) -> int:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_blockNumber',
                    'params': [],
                    'id': 1
                }
            )
            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(str(response_json['result']), 0)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting Last Block: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting Last Block: {error}')


async def get_nonces(provider_client: aiohttp.ClientSession,
                     owner_address: str) -> int:
    while True:
        response_text: None = None

        try:
            tx_data: str = '0x7ecebe00' + encode(
                types=['address'],
                args=[w3.to_checksum_address(value=owner_address)]
            ).hex()

            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                json={
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'eth_call',
                    'params': [
                        {
                            'to': config.TOKEN_CONTRACT_ADDRESS,
                            'data': tx_data
                        },
                        'latest'
                    ]
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(response_json['result'], 16)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting Nonces: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting Nonces: {error}')


async def get_balance(provider_client: aiohttp.ClientSession,
                      address: str) -> int:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                params={
                    'chainId': '204',
                    'projectUuid': '64c673d8-30bd-4e02-8be4-f9c5531a79a5',
                    'projectKey': 'cwTncilkSkASDvXWHC6LAfj3UnJOSb0vWmdXmS9C',
                    'method': 'particle_getTokensAndNFTs'
                },
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_getBalance',
                    'params': [
                        w3.to_checksum_address(value=address),
                        'latest'
                    ],
                    'id': 1
                }
            )
            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(str(response_json['result']), 0)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Getting Account Balance: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Getting Account Balance: {error}')


async def estimate_gas_price(provider_client: aiohttp.ClientSession,
                             transaction_data: dict) -> int | None:
    while True:
        response_text: None = None

        try:
            formatted_transaction_data: dict = deepcopy(transaction_data)

            formatted_transaction_data['maxFeePerGas']: str = w3.to_hex(
                primitive=transaction_data['maxFeePerGas']
            )
            formatted_transaction_data['maxPriorityFeePerGas']: str = w3.to_hex(
                primitive=transaction_data['maxPriorityFeePerGas']
            )
            formatted_transaction_data['nonce']: str = w3.to_hex(
                primitive=transaction_data['nonce']
            )
            del formatted_transaction_data['chainId']

            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                json={
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'eth_estimateGas',
                    'params': [
                        formatted_transaction_data,
                        'latest'
                    ]
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return int(response_json['result'], 16)

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Estimating Gas Price: {error}, response: {response_text}')

            else:
                logger.error(f'Unexpected Error When Estimating Gas Price: {error}')


async def send_transaction(provider_client: aiohttp.ClientSession,
                           transaction_data: bytes) -> str:
    while True:
        response_text: None = None

        try:
            r: aiohttp.ClientResponse = await provider_client.post(
                url=config.RPC_URL,
                params={
                    'chainId': '204',
                    'projectUuid': '64c673d8-30bd-4e02-8be4-f9c5531a79a5',
                    'projectKey': 'cwTncilkSkASDvXWHC6LAfj3UnJOSb0vWmdXmS9C',
                    'method': 'particle_getTokensAndNFTs'
                },
                json={
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'eth_sendRawTransaction',
                    'params': [
                        transaction_data.hex()
                    ]
                }
            )

            response_text: str = await r.text()
            response_json: dict = await r.json(content_type=None)

            return response_json['result']

        except Exception as error:
            if response_text:
                logger.error(f'Unexpected Error When Sending Transaction: {error}, response: {response_text}')


            else:
                logger.error(f'Unexpected Error When Sending Transaction: {error}')
