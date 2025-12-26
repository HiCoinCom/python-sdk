#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证语法和导入
"""

import sys
import os

print("=" * 60)
print("ChainUp Custody Python SDK - 快速测试")
print("=" * 60)

# 检查 Python 版本
print(f"\n1. Python 版本: {sys.version}")
if sys.version_info < (3, 7):
    print("❌ 错误: 需要 Python 3.7 或更高版本")
    sys.exit(1)
else:
    print("✅ Python 版本符合要求")

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 测试语法
print("\n2. 测试示例文件语法...")
example_files = [
    "examples/waas_example.py",
    "examples/mpc_example.py",
    "examples/custom_crypto_example.py",
]

for file in example_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            compile(f.read(), file, 'exec')
        print(f"   ✅ {file}")
    except SyntaxError as e:
        print(f"   ❌ {file}: {e}")
        sys.exit(1)

# 测试依赖
print("\n3. 检查依赖...")
dependencies = {
    'requests': 'requests',
    'Crypto': 'pycryptodome',
}

missing = []
for module, package in dependencies.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} (未安装)")
        missing.append(package)

if missing:
    print(f"\n⚠️  请安装缺失的依赖:")
    print(f"   pip3 install {' '.join(missing)}")
else:
    # 测试导入 SDK
    print("\n4. 测试导入 SDK...")
    try:
        from chainup_custody_sdk import WaasClient, MpcClient, MpcSignUtil
        print("   ✅ WaasClient")
        print("   ✅ MpcClient")
        print("   ✅ MpcSignUtil")
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！SDK 已就绪。")
        print("=" * 60)
        print("\n运行示例:")
        print("  python3 examples/waas_example.py")
        print("  python3 examples/mpc_example.py")
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
