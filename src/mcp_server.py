#!/usr/bin/env python3
"""
HIL (Human-in-the-Loop) 手动纠正服务器

提供手动纠正指令的 API 接口，支持：
- GET /hil/get_correction - 获取用户的手动纠正指令
- POST /hil/send_correction - 发送纠正指令给 agent 学习

运行方式：
python hil_server.py

服务将在 http://localhost:8001/hil 启动
"""

from flask import Flask, request, jsonify
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - HIL Server - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 存储手动纠正指令
correction_store = {
    "last_correction": None,
    "correction_history": []
}

# 存储 agent 学习数据
agent_learning_store = {
    "learning_history": []
}

@app.route('/hil/get_correction', methods=['GET'])
def get_correction():
    """
    获取用户的手动纠正指令
    
    返回示例：
    {
        "type": "correct",
        "action": "click",
        "scene": "秘境入口",
        "error_params": {"x": 100, "y": 200},
        "correct_params": {"x": 150, "y": 220},
        "reason": "坐标偏移导致点空"
    }
    """
    try:
        correction = correction_store.get("last_correction")
        if correction:
            logger.info(f"返回手动纠正指令：{correction}")
            # 清空上次纠正，避免重复处理
            correction_store["last_correction"] = None
            return jsonify(correction), 200
        else:
            return jsonify({"type": "none", "message": "无纠正指令"}), 200
    except Exception as e:
        logger.error(f"获取纠正指令失败：{str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/hil/send_correction', methods=['POST'])
def send_correction():
    """
    发送纠正指令给 agent 学习
    
    请求示例：
    {
        "type": "manual_correction",
        "script_id": "zhangsword_explore",
        "correction": {
            "type": "correct",
            "action": "click",
            "scene": "秘境入口",
            "error_params": {"x": 100, "y": 200},
            "correct_params": {"x": 150, "y": 220},
            "reason": "坐标偏移导致点空"
        },
        "timestamp": 1620000000.0
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "缺少请求数据"}), 400
        
        # 记录学习数据
        learning_data = {
            "data": data,
            "received_at": time.time()
        }
        agent_learning_store["learning_history"].append(learning_data)
        
        # 限制历史记录长度
        if len(agent_learning_store["learning_history"]) > 100:
            agent_learning_store["learning_history"] = agent_learning_store["learning_history"][-50:]
        
        logger.info(f"收到 agent 学习数据：{data}")
        return jsonify({"status": "success", "message": "学习数据已记录"}), 200
    except Exception as e:
        logger.error(f"发送纠正指令失败：{str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/hil/set_correction', methods=['POST'])
def set_correction():
    """
    设置手动纠正指令（测试用）
    
    请求示例：
    {
        "type": "correct",
        "action": "click",
        "scene": "秘境入口",
        "error_params": {"x": 100, "y": 200},
        "correct_params": {"x": 150, "y": 220},
        "reason": "坐标偏移导致点空"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "缺少请求数据"}), 400
        
        # 验证必填字段
        required_fields = ["type", "action", "correct_params"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"缺少必填字段：{field}"}), 400
        
        # 存储纠正指令
        correction_store["last_correction"] = data
        correction_store["correction_history"].append({
            "correction": data,
            "timestamp": time.time()
        })
        
        # 限制历史记录长度
        if len(correction_store["correction_history"]) > 50:
            correction_store["correction_history"] = correction_store["correction_history"][-25:]
        
        logger.info(f"设置手动纠正指令：{data}")
        return jsonify({"status": "success", "message": "纠正指令已设置"}), 200
    except Exception as e:
        logger.error(f"设置纠正指令失败：{str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/hil/status', methods=['GET'])
def get_status():
    """
    获取 HIL 服务器状态
    """
    try:
        status = {
            "status": "running",
            "timestamp": time.time(),
            "correction_count": len(correction_store["correction_history"]),
            "learning_count": len(agent_learning_store["learning_history"]),
            "has_pending_correction": correction_store["last_correction"] is not None
        }
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"获取状态失败：{str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("HIL 服务器启动中...")
    logger.info("服务将在 http://localhost:8001/hil 可用")
    logger.info("API 接口：")
    logger.info("- GET  /hil/get_correction    - 获取纠正指令")
    logger.info("- POST /hil/send_correction   - 发送纠正指令给 agent")
    logger.info("- POST /hil/set_correction    - 设置纠正指令（测试）")
    logger.info("- GET  /hil/status           - 获取服务状态")
    
    # 启动服务器
    app.run(
        host='0.0.0.0',
        port=8001,
        debug=False,
        threaded=True
    )
