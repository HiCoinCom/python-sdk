# 示例文件使用说明

## 安装依赖

在运行示例之前，请先安装必要的依赖：

```bash
# 安装依赖
pip3 install -r requirements.txt

# 或者以开发模式安装 SDK
pip3 install -e .
```

## 运行示例

### 方式 1: 直接运行（推荐）

```bash
# 运行 WaaS 示例
python3 examples/waas_example.py

# 运行 MPC 示例
python3 examples/mpc_example.py

# 运行自定义加密提供者示例
python3 examples/custom_crypto_example.py
```

### 方式 2: 添加执行权限后运行

```bash
# 添加执行权限
chmod +x examples/*.py

# 直接运行
./examples/waas_example.py
./examples/mpc_example.py
```

## 注意事项

1. **Python 版本**: 需要 Python 3.7 或更高版本

   ```bash
   # 检查 Python 版本
   python3 --version
   ```

2. **依赖安装**: 必须先安装 `pycryptodome` 和 `requests`

   ```bash
   pip3 install pycryptodome requests
   ```

3. **配置信息**: 示例文件中的配置信息需要替换为你的实际值：
   - `app_id`: 你的应用 ID
   - `rsa_private_key`: 你的 RSA 私钥
   - `waas_public_key`: WaaS 服务器公钥
   - `api_key`: API 密钥
   - `sign_private_key`: 交易签名私钥（可选）

## 常见问题

### 问题 1: `ModuleNotFoundError: No module named 'chainup_custody_sdk'`

**解决方法**:

```bash
# 以开发模式安装 SDK
pip3 install -e .
```

### 问题 2: `ModuleNotFoundError: No module named 'Crypto'`

**解决方法**:

```bash
# 安装 pycryptodome
pip3 install pycryptodome
```

### 问题 3: `SyntaxError: Non-ASCII character`

**解决方法**: 使用 Python 3 而不是 Python 2

```bash
# 使用 python3
python3 examples/waas_example.py

# 不要使用 python（可能是 Python 2）
# python examples/waas_example.py  # ❌
```

### 问题 4: `SyntaxError: invalid syntax` (f-string)

**原因**: Python 版本低于 3.6

**解决方法**: 升级到 Python 3.7+

```bash
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt install python3.9

# CentOS/RHEL
sudo yum install python39
```

## 示例说明

### waas_example.py

演示 WaaS (Wallet-as-a-Service) API 的使用，包括：

- 用户注册和管理
- 账户和地址查询
- 提现操作
- 充值记录查询
- 内部转账
- Webhook 通知处理

### mpc_example.py

演示 MPC (Multi-Party Computation) API 的使用，包括：

- 钱包创建和管理
- 地址生成
- 充值记录查询
- 提现操作（支持交易签名）
- Web3 交易
- 自动归集
- 工作区管理
- TRON 资源购买

### custom_crypto_example.py

演示如何实现自定义加密提供者，用于集成 HSM、KMS 等硬件安全模块。
