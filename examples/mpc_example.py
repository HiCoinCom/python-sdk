#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MPC API 使用示例
"""
import sys
import os

# 添加项目根目录到 Python 路径（允许在不安装的情况下运行）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 检查依赖
try:
    from chainup_custody_sdk import MpcClient, ApiError
except ImportError as e:
    print("=" * 60)
    print("❌ 缺少必要的依赖")
    print("=" * 60)
    print(f"\n错误: {e}\n")
    print("请先安装依赖:")
    print("  pip3 install pycryptodome requests")
    print("\n或者:")
    print("  pip3 install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)


def main():
    # 创建 MPC 客户端
    mpc_client = (
        MpcClient.new_builder()
        .set_app_id("")
        .set_rsa_private_key("")
        .set_sign_private_key("")
        .set_waas_public_key("") 
        .set_debug(False)  # 关闭调试模式
        .build()
    )

    # ============== 钱包管理 ==============
    wallet_api = mpc_client.get_wallet_api()

    # 创建钱包（使用随机名称避免重复）
    import random
    import time
    sub_wallet_id = 1000537
    wallet_name = "TestWallet"
    """ 
    try:
        wallet = wallet_api.create_wallet(
            {"sub_wallet_name": wallet_name, "app_show_status": 1}
        )
        print(f"Created wallet: {wallet}")
        # validate_response 现在直接返回 data 部分
        sub_wallet_id = wallet.get("sub_wallet_id")
        if not sub_wallet_id:
            print("创建成功，但未返回 sub_wallet_id")
            return
    except ApiError as e:
        print(f"创建钱包失败: {e}")
        return
 """
    # 创建钱包地址
    try:
        address = wallet_api.create_wallet_address(
            {"sub_wallet_id": sub_wallet_id, "symbol": "ETH"}
        )
        print(f"Created address: {address}")
    except ApiError as e:
        print(f"创建地址失败: {e}")

    # 查询钱包地址
    try:
        addresses = wallet_api.query_wallet_address(
            {"sub_wallet_id": sub_wallet_id, "symbol": "ETH", "max_id": 0}
        )
        print(f"Wallet addresses: {len(addresses) if isinstance(addresses, list) else 'N/A'}")
    except ApiError as e:
        print(f"查询地址失败: {e}")

    # 获取钱包资产
    try:
        assets = wallet_api.get_wallet_assets(
            {"sub_wallet_id": sub_wallet_id, "symbol": "ETH"}
        )
        print(f"Wallet assets: {assets}")
    except ApiError as e:
        print(f"查询资产失败: {e}")

    # ============== 充值管理 ==============
    deposit_api = mpc_client.get_deposit_api()

    # 同步充值记录
    try:
        deposits = deposit_api.sync_deposit_records(0)
        print(f"Deposits count: {len(deposits) if isinstance(deposits, list) else 'N/A'}")
        
        # 获取特定充值记录（deposits 现在直接是列表）
        if deposits and isinstance(deposits, list) and len(deposits) > 0:
            deposit_ids = [d["id"] for d in deposits[:3]]  # 取前3条
            deposit_records = deposit_api.get_deposit_records({"ids": deposit_ids})
            print(f"Deposit records count: {len(deposit_records) if isinstance(deposit_records, list) else 'N/A'}")
    except ApiError as e:
        print(f"查询充值记录失败: {e}")

    # ============== 提现管理 ==============
    withdraw_api = mpc_client.get_withdraw_api()

    # 发起提现（注意：需要先关注币种才能提现）
    try:
        withdraw_result = withdraw_api.withdraw(
            {
                "request_id": "1234567803",
                "sub_wallet_id": 1000537,
                "symbol": "Sepolia",
                "amount": "0.001",
                "address_to": "0xdcb0D867403adE76e75a4A6bBcE9D53C9d05B981",
                "remark": "Test withdrawal",
                "need_transaction_sign" : True,
            }
        )
        print(f"Withdraw result: {withdraw_result}")
    except ApiError as e:
        print(f"提现失败: {e}")

    # 查询提现记录
    try:
        withdraw_records = withdraw_api.get_withdraw_records(["12345678"])
        print(f"Withdraw records: {withdraw_records}")
    except ApiError as e:
        print(f"查询提现记录失败: {e}")

    # 同步提现记录
    try:
        withdrawals = withdraw_api.sync_withdraw_records(0)
        print(f"Withdrawals count: {len(withdrawals) if isinstance(withdrawals, list) else 'N/A'}")
    except ApiError as e:
        print(f"同步提现记录失败: {e}")

    # ============== Web3 交易 ==============
    web3_api = mpc_client.get_web3_api()

    # 创建 Web3 交易
    try:
        web3_result = web3_api.create_web3_trans(
            {
                "request_id": "12345678",
                "sub_wallet_id": sub_wallet_id,
                "main_chain_symbol": "ETH",
                "interactive_contract": "0x1234567890abcdef1234567890abcdef12345678",
                "amount": "0",
                "gas_price": "20",
                "gas_limit": "21000",
                "input_data": "0x",
                "trans_type": "1",
                "need_transaction_sign": False,
            }
        )
        print(f"Web3 transaction result: {web3_result}")
    except ApiError as e:
        print(f"创建 Web3 交易失败: {e}")

    # 查询 Web3 交易记录
    try:
        web3_records = web3_api.get_web3_trans_records(["12345678"])
        print(f"Web3 records: {len(web3_records) if isinstance(web3_records, list) else 'N/A'}")
    except ApiError as e:
        print(f"查询 Web3 交易记录失败: {e}")
        
         # 同步 Web3 交易记录
    try:
        sync_web3_records = web3_api.sync_web3_trans_records(1)
        print(f"Web3 records: {len(sync_web3_records) if isinstance(sync_web3_records, list) else 'N/A' }")
    except ApiError as e:
        print(f"同步 Web3 交易记录失败: {e}")

    # ============== 自动归集 ==============
    auto_sweep_api = mpc_client.get_auto_sweep_api()

    # 查询自动归集钱包
    try:
        sweep_wallets = auto_sweep_api.auto_collect_sub_wallets({"symbol": "USDTERC20"})
        print(f"Auto sweep wallets: {sweep_wallets}")
    except ApiError as e:
        print(f"查询自动归集钱包失败: {e}")

    # 设置自动归集配置
    try:
        sweep_config = auto_sweep_api.set_auto_collect_symbol(
            {"symbol": "USDTERC20", "collect_min": "100", "fueling_limit": "0.01"}
        )
        print(f"Auto sweep config: {sweep_config}")
    except ApiError as e:
        print(f"设置自动归集配置失败: {e}")

    # 同步自动归集记录
    try:
        sweep_records = auto_sweep_api.sync_auto_collect_records(0)
        print(f"Auto sweep records count: {len(sweep_records) if isinstance(sweep_records, list) else 'N/A'}")
    except ApiError as e:
        print(f"同步自动归集记录失败: {e}")

    # ============== 工作区管理 ==============
    workspace_api = mpc_client.get_workspace_api()

    # 获取支持的主链
    try:
        chains = workspace_api.get_support_main_chain()
        # chains 返回 {'open_main_chain': [...], 'support_main_chain': [...]}
        if isinstance(chains, dict):
            open_chains = chains.get("open_main_chain", [])
            support_chains = chains.get("support_main_chain", [])
            print(f"Open chains: {len(open_chains)}, Support chains: {len(support_chains)}")
        else:
            print(f"Chains: {chains}")
    except ApiError as e:
        print(f"获取支持主链失败: {e}")

    # 获取币种详情
    try:
        coins = workspace_api.get_coin_details(
            {"base_symbol": "ETH", "open_chain": True, "limit": 10}
        )
        print(f"Coin details count: {len(coins) if isinstance(coins, list) else 'N/A'}")
    except ApiError as e:
        print(f"获取币种详情失败: {e}")

    # 获取最新区块高度
    try:
        block_height = workspace_api.get_last_block_height({"base_symbol": "ETH"})
        print(f"Block height: {block_height}")
    except ApiError as e:
        print(f"获取区块高度失败: {e}")

    # ============== TRON 资源管理 ==============
    tron_api = mpc_client.get_tron_resource_api()

    # 购买 TRON 资源（通常需要有效的 TRON 地址）
    try:
        tron_result = tron_api.create_tron_delegate(
            {
                'request_id': '12345678908',
                'resource_type': 1,
                'buy_type': 0,
                'energy_num': 32000,
                'address_from': 'TPjJg9FnzQuYBd6bshgaq7rkH4s36zju5S',
                'address_to': 'TGmBzYfBBtMfFF8v9PweTaPwn3WoB7aGPd',
                'contract_address': 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
                'service_charge_type': '10010'
            }
        )
        print(f"TRON delegation result: {tron_result}")
    except ApiError as e:
        print(f"购买 TRON 资源失败: {e}")

    # 查询资源购买记录
    try:
        tron_records = tron_api.get_buy_resource_records(["12345678908"])
        print(f"TRON records: {len(tron_records) if isinstance(tron_records, list) else 'N/A'}")
    except ApiError as e:
        print(f"查询 TRON 资源记录失败: {e}")
        
        
    # 查询资源购买记录
    try:
        tron_records = tron_api.sync_buy_resource_records(10)
        print(f"TRON records: {len(tron_records) if isinstance(tron_records, list) else 'N/A'}")
    except ApiError as e:
        print(f"同步 TRON 资源记录失败: {e}")

    # ============== 通知处理 ==============
    notify_api = mpc_client.get_notify_api()

    # 解密通知数据（在 webhook 回调中使用）
    encrypted_data = "Af-uUJj8a2-Og7E5CwzANv4vo8NMf-z-DijwrIuK74Or8eRveM7G_-f0ErtX4WurcVrjdWC-tqU0BDhBwiDijbdyCFBvYB5UmLnHL_Rg13amhQTM-kaHoh-U9WPhYB3vGRwWkTwJ_aETERVVciAvoTf5CalqydMSe8G3KNz-ymrSVUe92DfW5ZdDKJm1hNYYteGJvg0hk--GRiPybPv2W78NlTLyWmXq094megsVzZv-KlsEGPUvPoBnEJ0Xu__AO-l-GfCG4rVO4rb8J01Nq_0Q9eRKcKWq0ci7MfnPPLMhtAWwRvSd3U8PUNHOLqGaJzOLraFnuFUHn90h7T23_DeAduA2W6dto99qb8YQ_iVnMnOKfE0Ls7Vv5S2qhgQJ0nl-BA3PPPOwW37cMb-wTbi3ZezU_S1NQEbrruEChkPhTaK0AqsM6mESV8wGflcWx3N9XPv6QatJ9zedBnkfJ4bJ4Vy2rUEtQF8eVc6zXhV8PuDRiSMf0V0yxzMjE6o9z0s087KSAqFphitlHvQMPJ29FUnyvCe_Czr5WPuhl89GOZjERE2uoNTfHqAlZVzMamoPv4y0qyIjJTufAQm-WwrQK9kGesky7eCiOXVdtR9UhEYpzEJSgXxENjUrHMx6D2AlEzlr17a2DgI-WrWB7oUnyiNnf__ElmLPPkJBdFUfzJByQkLxkUB0FLvTWdVbiIRPmPpdgb7jkhJsHUSOH0NmULqu8bYiEQtGfqRJh8I98qDzHWwfE_VAbqwATj2oD959Fm1eInBqh7eXGoy2WR3o00VpPrNvoE4eJNmw3WpVzlRF7ZVwOpcWRT-dHTShz9mB2Etk9P8D4rGmMZyXHkt4aGUJkE1b3cOEjzkOEFX8CaNe-VHiBYhIyFzMetn7mfIFB0hl565FGEumbhDKNNz_m9T2qPM5k4BQ9fLWUt_WJAVdC81_piIlBOQfYPDbdYoc_9ser1p-Jy5cgTyOMdWuSWC3jMsT09xr8dMcLkKmd39khGidAvGqOOPL1ST0"
    notify_data = notify_api.notify_request(encrypted_data)
    if notify_data:
        print(f"Notify type: {notify_data['side']}")  # 'deposit' or 'withdraw'
        print(f"Sub wallet ID: {notify_data['sub_wallet_id']}")
        print(f"Symbol: {notify_data['symbol']}")
        print(f"Amount: {notify_data['amount']}")


if __name__ == "__main__":
    main()
