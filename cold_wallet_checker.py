"""
Cold Wallet Checker — утилита для обнаружения "спящих" или заброшенных Ethereum-кошельков.

Применение: поиск потенциальных cold wallets для исследований, исторического анализа или NFT-раскопок.
"""

import requests
import argparse
import datetime


ETHERSCAN_API = "https://api.etherscan.io/api"


def fetch_transactions(address, api_key):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": api_key
    }
    r = requests.get(ETHERSCAN_API, params=params)
    return r.json().get("result", [])


def analyze_activity(transactions, months_idle=12):
    if not transactions:
        return f"Кошелёк никогда не совершал транзакций — возможно, заброшен."

    last_tx = transactions[0]
    timestamp = int(last_tx["timeStamp"])
    last_active_date = datetime.datetime.utcfromtimestamp(timestamp)
    now = datetime.datetime.utcnow()
    delta = now - last_active_date

    if delta.days >= months_idle * 30:
        return f"🔒 Кошелёк не активен более {months_idle} мес. (последняя активность: {last_active_date.strftime('%Y-%m-%d')})"
    else:
        return f"✅ Кошелёк активен. Последняя активность: {last_active_date.strftime('%Y-%m-%d')} ({delta.days} дней назад)"


def main():
    parser = argparse.ArgumentParser(description="Анализ 'холодности' Ethereum-кошелька.")
    parser.add_argument("address", help="Ethereum-адрес")
    parser.add_argument("api_key", help="Etherscan API Key")
    parser.add_argument("--months", type=int, default=12, help="Сколько месяцев считать за 'холодный' (по умолчанию 12)")
    args = parser.parse_args()

    print("[•] Получаем историю транзакций...")
    txs = fetch_transactions(args.address, args.api_key)
    result = analyze_activity(txs, args.months)

    print("\nРезультат анализа:")
    print(result)


if __name__ == "__main__":
    main()
