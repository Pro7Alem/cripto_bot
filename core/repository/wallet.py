from core.repository.db import exec_command, exec_query


def get_local_wallet():
    # LOAD LOCAL WALLET FROM DATABASE
    result = exec_query("SELECT btc, usdt FROM wallet LIMIT 1")
    return result[0]


def update_local_wallet(btc, usdt, updated_at):
    # UPDATE LOCAL WALLET STATE
    exec_command(
        "UPDATE wallet SET btc = ?, usdt = ?, updated_at = ?", (btc, usdt, updated_at)
    )
