#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杖剑传说 - 智能游戏探索 Agent 启动脚本

使用方法:
    python run.py          # 启动主程序
    python run.py --hil    # 启动 HIL 服务器
"""

import sys
import os

# 设置编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    # 添加 src 目录到 Python 路径
    src_path = os.path.join(os.path.dirname(__file__), "src")
    sys.path.insert(0, src_path)
    
    if "--hil" in sys.argv:
        # 启动 HIL (Human-in-the-Loop) 服务器
        from mcp_server import app
        print("🚀 启动 HIL 服务器...")
        print("📍 服务地址: http://localhost:8001/hil")
        app.run(host="0.0.0.0", port=8001, debug=False, threaded=True)
    else:
        # 启动主程序
        from main import main as main_func
        auto_start = "--start" in sys.argv
        main_func(auto_start)

if __name__ == "__main__":
    main()
