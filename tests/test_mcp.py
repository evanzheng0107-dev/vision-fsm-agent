#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 HIL (Human-in-the-Loop) 服务器是否正常运行
"""

import sys
import io
# 设置控制台编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import time

def test_hil_status():
    """测试 HIL 服务状态"""
    url = "http://localhost:8001/hil/status"
    print(f"测试 HIL 服务状态: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ HIL 服务正常运行！")
            print(f"   状态: {status.get('status')}")
            print(f"   时间戳: {time.ctime(status.get('timestamp', time.time()))}")
            print(f"   纠正指令数: {status.get('correction_count', 0)}")
            print(f"   学习数据数: {status.get('learning_count', 0)}")
            return True
        else:
            print(f"❌ HIL 服务返回错误状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 HIL 服务，请检查服务是否启动")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def test_get_correction():
    """测试获取纠正指令"""
    url = "http://localhost:8001/hil/get_correction"
    print(f"\n测试获取纠正指令: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            correction = response.json()
            print("✅ 获取纠正指令成功！")
            print(f"   响应: {correction}")
            return True
        else:
            print(f"❌ 获取纠正指令失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def test_set_correction():
    """测试设置纠正指令"""
    url = "http://localhost:8001/hil/set_correction"
    print(f"\n测试设置纠正指令: {url}")
    
    try:
        data = {
            "type": "correct",
            "action": "click",
            "scene": "测试场景",
            "correct_params": {"x": 400, "y": 500},
            "reason": "测试手动纠正"
        }
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ 设置纠正指令成功！")
            print(f"   响应: {result}")
            return True
        else:
            print(f"❌ 设置纠正指令失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== HIL 服务测试 ===")
    
    # 测试服务状态
    status_ok = test_hil_status()
    
    # 如果服务正常，测试其他功能
    if status_ok:
        test_get_correction()
        test_set_correction()
    
    print("\n=== 测试完成 ===")
