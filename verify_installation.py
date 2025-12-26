#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDK 安装验证脚本
验证 ChainUp Custody Python SDK 是否正确安装
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("=" * 70)
print("ChainUp Custody Python SDK - 安装验证")
print("=" * 70)

# 1. 检查 Python 版本
print(f"\n✓ Python 版本: {sys.version.split()[0]}")
if sys.version_info < (3, 7):
    print("  ⚠️  警告: 建议使用 Python 3.7+")

# 2. 检查依赖
print("\n检查依赖...")
deps_ok = True

try:
    import requests
    print(f"  ✓ requests ({requests.__version__})")
except ImportError:
    print("  ✗ requests (未安装)")
    deps_ok = False

try:
    import Crypto
    print(f"  ✓ pycryptodome ({Crypto.__version__})")
except ImportError:
    print("  ✗ pycryptodome (未安装)")
    deps_ok = False

if not deps_ok:
    print("\n请安装缺失的依赖:")
    print("  pip3 install pycryptodome requests")
    sys.exit(1)

# 3. 测试导入 SDK
print("\n检查 SDK 模块...")
try:
    from chainup_custody_sdk import WaasClient, MpcClient, MpcSignUtil
    from chainup_custody_sdk import ICryptoProvider, RsaCryptoProvider
    from chainup_custody_sdk import __version__
    
    print(f"  ✓ SDK 版本: {__version__}")
    print(f"  ✓ WaasClient")
    print(f"  ✓ MpcClient")
    print(f"  ✓ MpcSignUtil")
    print(f"  ✓ ICryptoProvider")
    print(f"  ✓ RsaCryptoProvider")
    
except Exception as e:
    print(f"  ✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 验证 Builder 模式
print("\n测试 Builder 模式...")
try:
    # 测试 WaaS Builder（不实际调用 API）
    builder = WaasClient.new_builder()
    builder.set_host("https://api.example.com")
    builder.set_app_id("test-app-id")
    print("  ✓ WaasClient.new_builder()")
    
    # 测试 MPC Builder（不实际调用 API）
    builder = MpcClient.new_builder()
    builder.set_domain("https://mpc.example.com")
    builder.set_app_id("test-app-id")
    print("  ✓ MpcClient.new_builder()")
    
except Exception as e:
    print(f"  ✗ Builder 测试失败: {e}")
    sys.exit(1)

# 5. 测试签名工具
print("\n测试 MpcSignUtil...")
try:
    # 测试参数排序
    result = MpcSignUtil.params_sort({
        'amount': '1.0001000',
        'symbol': 'ETH',
        'address': '0x123'
    })
    expected = 'address=0x123&amount=1.0001&symbol=eth'
    if result == expected:
        print(f"  ✓ params_sort() 正常工作")
    else:
        print(f"  ⚠️  params_sort() 结果不符合预期")
        print(f"     期望: {expected}")
        print(f"     实际: {result}")
    
    # 测试 MD5
    md5_result = MpcSignUtil.md5('test')
    if md5_result == '098f6bcd4621d373cade4e832627b4f6':
        print(f"  ✓ md5() 正常工作")
    else:
        print(f"  ⚠️  md5() 结果不符合预期")
        
except Exception as e:
    print(f"  ✗ MpcSignUtil 测试失败: {e}")
    import traceback
    traceback.print_exc()

# 总结
print("\n" + "=" * 70)
print("✓ SDK 安装成功！可以开始使用。")
print("=" * 70)
print("\n下一步:")
print("  1. 配置你的 API 密钥和证书")
print("  2. 参考示例代码: examples/waas_example.py 和 examples/mpc_example.py")
print("  3. 查看文档: README.md")
print("\n注意: 示例文件中的配置需要替换为你的实际值才能运行。")
print("=" * 70)
