#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入脚本
"""
import sys
sys.path.insert(0, '.')

try:
    from chainup_custody_sdk import WaasClient, MpcClient, MpcSignUtil
    print("✅ 导入成功!")
    print(f"WaasClient: {WaasClient}")
    print(f"MpcClient: {MpcClient}")
    print(f"MpcSignUtil: {MpcSignUtil}")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
