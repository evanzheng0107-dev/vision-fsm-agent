import sys
import io
# 设置控制台编码为UTF-8，支持emoji和中文
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import cv2
import numpy as np
import pyautogui
import yaml
import win32gui
import win32con
import time
import os
from mss import mss
import random
from cloud_agent import CloudDecisionAgent
import keyboard
import requests
import json
import logging  # 新增：日志模块
from typing import Optional, Dict, Any  # 新增：类型提示

# 全局禁用pyautogui的鼠标移动失败保护（适配模拟器）
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# ===================== 优化后的HIL客户端类（核心修改） =====================
# 配置日志（方便排查HIL交互问题）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
hil_logger = logging.getLogger("HilClient")

class HilClient:
    def __init__(self, config: Dict[str, Any]):
        # 修复：使用传入的config参数，提升灵活性
        self.config = config or {}
        self.server_url = self.config.get(
            "hil_server_url",
            os.getenv("HIL_SERVER_URL", "http://localhost:8001/hil")
        )
        self.headers = {
            "Content-Type": "application/json",
            "HIL-Version": "1.0"  # 新增：HIL协议版本标识
        }
        self.script_id = self.config.get("script_id", "zhangsword_explore")  # 脚本唯一标识
        hil_logger.info(f"✅ HIL客户端初始化成功，服务地址：{self.server_url}")
    
    def get_manual_correction(self) -> Optional[Dict[str, Any]]:
        """
        获取用户的手动纠正指令（结构化格式，支持agent学习）
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
            response = requests.get(
                f"{self.server_url}/get_correction",
                headers=self.headers,
                timeout=2
            )
            if response.status_code == 200:
                correction = response.json()
                # 新增：校验纠正指令格式是否符合HIL协议
                if self._validate_correction(correction):
                    hil_logger.info(f"📥 获取到手动纠正指令：{correction}")
                    return correction
                else:
                    hil_logger.warning("❌ 手动纠正指令格式不符合HIL协议规范")
        except requests.exceptions.Timeout:
            hil_logger.warning("⚠️ 获取手动纠正指令超时（HIL服务可能未启动）")
        except Exception as e:
            hil_logger.error(f"❌ 获取手动纠正指令失败：{str(e)}")
        return None
    
    def send_status(self, status: Dict[str, Any]) -> bool:
        """
        发送结构化游戏状态到HIL服务（供agent分析场景）
        """
        try:
            # 新增：结构化payload，包含协议类型、脚本标识等
            payload = {
                "type": "game_status",
                "script_id": self.script_id,
                "status": status,
                "timestamp": time.time(),
                "window_title": self.config.get("window_title", "杖剑传说")
            }
            response = requests.post(
                f"{self.server_url}/send_status",
                headers=self.headers,
                json=payload,
                timeout=2
            )
            if response.status_code == 200:
                hil_logger.debug(f"📤 游戏状态上报成功：{status['current_state']}")
                return True
            else:
                hil_logger.warning(f"❌ 状态上报失败，状态码：{response.status_code}")
        except requests.exceptions.Timeout:
            hil_logger.warning("⚠️ 状态上报超时（HIL服务可能未启动）")
        except Exception as e:
            hil_logger.error(f"❌ 状态上报失败：{str(e)}")
        return False
    
    def send_correction_to_agent(self, correction: Dict[str, Any]) -> bool:
        """
        新增核心方法：将手动纠正指令发送给agent，供agent学习优化决策
        """
        if not correction:
            return False
        try:
            payload = {
                "type": "manual_correction",
                "script_id": self.script_id,
                "correction": correction,
                "timestamp": time.time()
            }
            response = requests.post(
                f"{self.server_url}/send_correction",
                headers=self.headers,
                json=payload,
                timeout=2
            )
            if response.status_code == 200:
                hil_logger.info("📤 手动纠正指令已发送给agent，等待学习优化...")
                return True
            else:
                hil_logger.warning(f"❌ 发送纠正指令给agent失败，状态码：{response.status_code}")
        except Exception as e:
            hil_logger.error(f"❌ 发送纠正指令失败：{str(e)}")
        return False
    
    def get_agent_decision(self, game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        新增核心方法：获取agent学习后的智能决策指令
        """
        try:
            payload = {
                "type": "request_decision",
                "script_id": self.script_id,
                "game_state": game_state,
                "timestamp": time.time()
            }
            response = requests.post(
                f"{self.server_url}/get_decision",
                headers=self.headers,
                json=payload,
                timeout=3  # 决策请求超时时间稍长
            )
            if response.status_code == 200:
                decision = response.json()
                hil_logger.info(f"🌐 获取到agent学习后的决策：{decision['action']}")
                return decision
            else:
                hil_logger.warning(f"❌ 获取agent决策失败，状态码：{response.status_code}")
        except Exception as e:
            hil_logger.error(f"❌ 获取agent决策失败：{str(e)}")
        return None
    
    def _validate_correction(self, correction: Dict[str, Any]) -> bool:
        """
        私有方法：校验手动纠正指令的格式是否合法
        """
        # 特殊处理无纠正指令的情况
        if correction.get("type") == "none":
            return True
            
        required_fields = ["type", "action", "correct_params"]
        for field in required_fields:
            if field not in correction:
                hil_logger.warning(f"❌ 纠正指令缺少必填字段：{field}")
                return False
        # 确保坐标参数存在
        if correction["action"] == "click" and ("x" not in correction["correct_params"] or "y" not in correction["correct_params"]):
            hil_logger.warning("❌ 点击类纠正指令缺少x/y坐标参数")
            return False
        return True

# ===================== 原有核心逻辑（无修改/仅适配HIL） =====================
# 加载配置文件
def load_config():
    # 可能的配置文件位置
    possible_paths = [
        os.path.join(os.getcwd(), "config.yaml"),
        os.path.join(os.getcwd(), "configs", "config.yaml"),
        os.path.join(os.path.dirname(__file__), "..", "configs", "config.yaml"),
        os.path.join(os.path.dirname(__file__), "..", "config.yaml"),
    ]
    
    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            break
    
    if config_path is None:
        print("❌ 未找到配置文件，请确保 config.yaml 在以下位置之一：")
        print("   - 项目根目录")
        print("   - configs/ 目录")
        print(f"当前工作目录：{os.getcwd()}")
        exit(1)
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print(f"✅ 配置文件加载成功：{config_path}")
        return config
    except Exception as e:
        print(f"❌ 配置加载失败：{e}")
        print(f"配置文件路径：{config_path}")
        exit(1)

# 定位模拟器窗口句柄
def get_window_handle(window_title):
    def callback(handle, extra):
        if window_title in win32gui.GetWindowText(handle):
            extra.append(handle)
        return True
    handles = []
    win32gui.EnumWindows(callback, handles)
    return handles[0] if handles else None

# 激活模拟器窗口（确保在前台）
def activate_window(handle):
    if handle:
        try:
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(handle)
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ 窗口激活失败：{e}，继续执行脚本")
            time.sleep(0.5)

# 高效截图（仅截取模拟器游戏区域）
def capture_screenshot(region):
    try:
        with mss() as sct:
            monitor = {
                "top": region[1],
                "left": region[0],
                "width": region[2],
                "height": region[3]
            }
            img = np.array(sct.grab(monitor))
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    except Exception as e:
        print(f"❌ 截图失败：{e}")
        return None

# 多尺度模板匹配（修复scale_start定义）
def multi_scale_match(template, screenshot, config):
    if template is None or screenshot is None:
        return 0, (0, 0)
    
    # 拆分缩放范围为起始/结束值
    scale_start, scale_end = config["scale_range"]
    scale_step = (scale_end - scale_start) / (config["scale_steps"] - 1)
    scales = [scale_start + i * scale_step for i in range(config["scale_steps"])]
    
    best_val = 0
    best_pos = (0, 0)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    for scale in scales:
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        # 跳过尺寸超过截图的模板
        if resized_template.shape[0] > gray_screenshot.shape[0] or resized_template.shape[1] > gray_screenshot.shape[1]:
            continue
        # 模板匹配
        result = cv2.matchTemplate(gray_screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > best_val:
            best_val = max_val
            best_pos = max_loc
    
    return best_val, best_pos

# 模拟人类点击（带随机偏移）
def human_click(x, y, config):
    # 添加随机偏移，避免固定点击位置
    offset_x = random.randint(-config["click_offset"], config["click_offset"])
    offset_y = random.randint(-config["click_offset"], config["click_offset"])
    click_x = x + offset_x
    click_y = y + offset_y
    # 随机点击延迟
    delay = random.uniform(*config["click_delay"])
    
    pyautogui.moveTo(click_x, click_y, duration=0.1)
    pyautogui.click(click_x, click_y, interval=delay)
    print(f"✅ 点击位置：({click_x}, {click_y})，延迟：{delay:.2f}秒")

# 盲走探索（无目标时随机移动）
def blind_explore(config):
    region = config["window_region"]
    # 在游戏区域内随机点击
    click_x = region[0] + random.randint(100, region[2]-100)
    click_y = region[1] + random.randint(200, region[3]-200)
    human_click(click_x, click_y, config)
    # 随机走路延迟
    walk_delay = random.uniform(*config["walk_delay"])
    print(f"🔍 无目标，盲走探索中，等待{walk_delay:.2f}秒...")
    time.sleep(walk_delay)

# 拖动地图
def drag_map(config, direction, distance=200):
    """
    拖动地图
    direction: 拖动方向，可选值：left, right, up, down
    distance: 拖动距离（像素）
    """
    region = config["window_region"]
    # 计算拖动起点（屏幕中心）
    start_x = region[0] + region[2] // 2
    start_y = region[1] + region[3] // 2
    
    # 计算拖动终点
    if direction == "left":
        end_x = start_x - distance
        end_y = start_y
    elif direction == "right":
        end_x = start_x + distance
        end_y = start_y
    elif direction == "up":
        end_x = start_x
        end_y = start_y - distance
    elif direction == "down":
        end_x = start_x
        end_y = start_y + distance
    else:
        return
    
    # 执行拖动操作
    pyautogui.moveTo(start_x, start_y, duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.5)
    pyautogui.mouseUp()
    
    print(f"🗺️ 拖动地图 {direction} 方向，距离 {distance} 像素")
    # 等待地图稳定
    time.sleep(1.0)

# 检查是否为个人信息页（特征：战力标题区域）
def is_personal_info_page(screenshot):
    # 个人信息页特征检测（战力标题区域）
    # 这里使用简单的颜色和纹理分析，实际应用中可使用更精确的模板匹配
    h, w = screenshot.shape[:2]
    # 检查左上角区域是否有特征颜色
    roi = screenshot[20:100, 20:200]
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # 战力标题区域通常有金色/黄色调
    lower = np.array([20, 100, 100])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    yellow_area = cv2.countNonZero(mask)
    # 提高阈值，减少误判
    is_personal = yellow_area > 1500
    if is_personal:
        print(f"🔍 个人信息页检测：黄色区域像素数 = {yellow_area}")
    return is_personal

# 检查是否为对话框（特征：对话文本框区域）
def is_dialog_page(screenshot, dialog_templates, config):
    # 对话框特征检测（对话文本框区域）
    h, w = screenshot.shape[:2]
    
    # 1. 首先检测是否为地图探索界面（特征：右下角有探索按钮）
    # 检查右下角区域是否有探索按钮特征
    explore_roi = screenshot[h-150:h, w-150:w]
    explore_gray = cv2.cvtColor(explore_roi, cv2.COLOR_BGR2GRAY)
    explore_edges = cv2.Canny(explore_gray, 50, 150)
    explore_edge_area = cv2.countNonZero(explore_edges)
    
    # 2. 检查是否为地图探索界面（特征：顶部有角色信息和地图）
    # 检查顶部区域是否有角色信息特征
    top_roi = screenshot[0:100, 0:w]
    top_gray = cv2.cvtColor(top_roi, cv2.COLOR_BGR2GRAY)
    top_edges = cv2.Canny(top_gray, 50, 150)
    top_edge_area = cv2.countNonZero(top_edges)
    
    # 3. 检查是否为地图探索界面（特征：中间有角色）
    # 检查中间区域是否有角色特征
    mid_roi = screenshot[h//2-100:h//2+100, w//2-100:w//2+100]
    mid_gray = cv2.cvtColor(mid_roi, cv2.COLOR_BGR2GRAY)
    mid_edges = cv2.Canny(mid_gray, 50, 150)
    mid_edge_area = cv2.countNonZero(mid_edges)
    
    # 如果检测到探索按钮、顶部角色信息或中间角色，说明是地图探索界面
    if explore_edge_area > 500 or top_edge_area > 1000 or mid_edge_area > 500:
        return False
    
    # 4. 使用对话框模板进行匹配
    if dialog_templates:
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        best_val = 0
        
        for template_name, dialog_template in dialog_templates:
            val, pos = multi_scale_match(dialog_template, screenshot, config)
            if val > best_val:
                best_val = val
        
        # 使用模板匹配阈值判断
        dialog_threshold = config.get("confidence_dialog", 0.6)
        is_dialog = best_val >= dialog_threshold
        
        if is_dialog:
            print(f"💬 对话框模板匹配：最佳匹配值 = {best_val:.2f}, 阈值 = {dialog_threshold}")
        
        return is_dialog
    else:
        # 如果没有对话框模板，使用边缘检测作为 fallback
        # 检测聊天对话框（两种形式）
        # 1. 完整聊天窗口（图1）：检查中间和顶部区域
        chat_roi1 = screenshot[50:h-100, 50:w-50]
        # 2. 底部聊天预览（图2）：检查底部区域
        chat_roi2 = screenshot[h-200:h, 50:w-50]
        
        # 转换为灰度
        gray1 = cv2.cvtColor(chat_roi1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(chat_roi2, cv2.COLOR_BGR2GRAY)
        
        # 检测边缘
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # 计算边缘区域
        edge_area1 = cv2.countNonZero(edges1)
        edge_area2 = cv2.countNonZero(edges2)
        
        # 聊天对话框特征：底部区域有大量文本和边缘
        is_dialog = edge_area2 > 3000 or edge_area1 > 4000
        
        if is_dialog:
            print(f"💬 聊天对话框检测：底部边缘区域 = {edge_area2}, 中间边缘区域 = {edge_area1}")
        
        return is_dialog

# 关闭弹窗/对话框
def close_popup(config, popup_type):
    region = config["window_region"]
    if popup_type == "personal_info":
        # 个人信息页：点击右上角关闭按钮区域（更精确的位置）
        click_x = region[0] + region[2] - 50
        click_y = region[1] + 50
    elif popup_type == "dialog":
        # 聊天对话框：点击左下角箭头关闭（根据图片位置）
        click_x = region[0] + 80  # 左下角箭头位置
        click_y = region[1] + region[3] - 50  # 底部位置
        print(f"🎯 聊天对话框关闭位置：({click_x}, {click_y})")
    else:
        return
    
    human_click(click_x, click_y, config)
    print(f"❌ 检测到{popup_type}页面，点击关闭区域")
    # 等待弹窗关闭
    time.sleep(1.0)

# 兼容原有CloudDecisionAgent（避免脚本报错）
class CloudDecisionAgent:
    def __init__(self):
        self.decision_count = 0
        print("✅ 云端决策代理初始化成功！")
    
    def get_decision(self, game_state):
        """基于游戏状态返回智能决策"""
        self.decision_count += 1
        
        # 分析游戏状态
        match_results = game_state.get("match_results", {})
        battle_found = match_results.get("battle", {}).get("found", False)
        pickup_found = match_results.get("pickup", {}).get("found", False)
        pathfind_found = match_results.get("pathfind", {}).get("found", False)
        
        # 决策逻辑
        if battle_found:
            return {
                "action": "battle",
                "reason": f"检测到战斗，执行战斗操作"
            }
        elif pickup_found:
            return {
                "action": "pickup",
                "reason": f"检测到拾取物品，执行拾取操作"
            }
        elif pathfind_found:
            return {
                "action": "pathfind",
                "reason": f"检测到定位器，执行移动操作"
            }
        else:
            # 无目标时的决策
            failed_attempts = game_state.get("failed_attempts", 0)
            if failed_attempts > 3:
                return {
                    "action": "wait",
                    "reason": f"连续失败{failed_attempts}次，等待场景加载"
                }
            else:
                return {
                    "action": "explore",
                    "reason": f"无目标，执行盲走探索（第{self.decision_count}次决策）"
                }

# ===================== 主循环逻辑（适配HIL优化） =====================
def main(auto_start=False):
    # 初始化配置
    config = load_config()
    # 定位模拟器窗口
    window_handle = get_window_handle(config["window_title"])
    if not window_handle:
        print(f"❌ 未找到窗口：{config['window_title']}")
        exit(1)
    print(f"✅ 找到模拟器窗口，句柄：{window_handle}")
    # 激活窗口
    activate_window(window_handle)
    
    # 加载模板图片
    battle_template = None
    pickup_templates = []
    locator_templates = []
    dialog_templates = []
    try:
        # 加载战斗按钮模板
        battle_path = os.path.join(os.getcwd(), config["battle_button_path"])
        battle_template = cv2.imread(battle_path, 0)
        if battle_template is None:
            print(f"⚠️ 未找到战斗按钮模板：{battle_path}，跳过战斗识别")
        else:
            print(f"✅ 战斗按钮模板加载成功：{battle_path}")
        
        # 加载拾取物品模板
        pickup_templates = []
        pickup_path = os.path.join(os.getcwd(), config["pickup_item_path"])
        pickup_template = cv2.imread(pickup_path, 0)
        if pickup_template is not None:
            pickup_templates.append(('default', pickup_template))
            print(f"✅ 拾取物品模板加载成功：{pickup_path}")
        
        # 加载额外的拾取物品模板
        template_dir = os.path.join(os.getcwd(), "assets", "templates")
        if os.path.exists(template_dir):
            for file_name in os.listdir(template_dir):
                if file_name.startswith("pickup_item_") and file_name.endswith(".png"):
                    pickup_path = os.path.join(template_dir, file_name)
                    pickup_template = cv2.imread(pickup_path, 0)
                    if pickup_template is not None:
                        pickup_templates.append((file_name, pickup_template))
                        print(f"✅ 拾取物品模板加载成功：{file_name}")
        
        if not pickup_templates:
            print(f"⚠️ 未找到拾取物品模板，跳过拾取识别")
        else:
            print(f"✅ 共加载 {len(pickup_templates)} 个拾取物品模板")
        
        # 加载定位器模板
        sample_dir = os.path.join(os.getcwd(), config["sample_dir"])
        if os.path.exists(sample_dir):
            for file_name in os.listdir(sample_dir):
                if (file_name.startswith("locator_") or file_name.startswith("target")) and file_name.endswith(".png"):
                    locator_path = os.path.join(sample_dir, file_name)
                    locator_template = cv2.imread(locator_path, 0)
                    if locator_template is not None:
                        locator_templates.append((file_name, locator_template))
                        print(f"✅ 定位器模板加载成功：{file_name}")
            if not locator_templates:
                print(f"⚠️ 未找到定位器模板，跳过定位器识别")
            else:
                print(f"✅ 共加载 {len(locator_templates)} 个定位器模板")
        else:
            print(f"⚠️ 样本目录不存在：{sample_dir}，跳过定位器识别")
        
        # 加载对话框模板
        sample_dir = os.path.join(os.getcwd(), config["sample_dir"])
        if os.path.exists(sample_dir):
            for file_name in os.listdir(sample_dir):
                if file_name.startswith("dailog_") or file_name.startswith("dialog_") and file_name.endswith(".png"):
                    dialog_path = os.path.join(sample_dir, file_name)
                    dialog_template = cv2.imread(dialog_path, 0)
                    if dialog_template is not None:
                        dialog_templates.append((file_name, dialog_template))
                        print(f"✅ 对话框模板加载成功：{file_name}")
            if not dialog_templates:
                print(f"⚠️ 未找到对话框模板，使用边缘检测方式")
            else:
                print(f"✅ 共加载 {len(dialog_templates)} 个对话框模板")
        else:
            print(f"⚠️ 样本目录不存在：{sample_dir}，使用边缘检测方式")
    except Exception as e:
        print(f"❌ 加载模板失败：{e}")
    
    # 初始化云端决策代理（兼容原有逻辑）
    cloud_agent = CloudDecisionAgent()
    print("✅ 云端决策代理初始化成功！")
    
    # 初始化优化后的HIL客户端
    hil_client = HilClient(config)  # 传入config参数，提升灵活性
    
    # 初始化失败次数
    failed_attempts = 0
    start_time = time.time()
    print("🚀 《杖剑传说》自动探索脚本已准备就绪！")
    print("💡 提示：输入 'start' 启动脚本，输入 'exit' 退出")
    print("💡 运行中按 ESC 键可终止脚本")
    
    # 等待启动指令
    if not auto_start:
        while True:
            # 检查ESC键是否被按下
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已退出！")
                exit(0)
            
            # 检查启动指令
            try:
                import sys
                if sys.stdin.isatty():
                    command = input("请输入指令 (start/exit): ").strip().lower()
                    if command == "start":
                        print("\n🚀 脚本开始运行...")
                        break
                    elif command == "exit":
                        print("\n🛑 脚本已退出！")
                        exit(0)
            except:
                # 如果不是交互式终端，等待HIL启动指令
                correction = hil_client.get_manual_correction()
                if correction and correction.get("action") == "start":
                    print("\n🚀 收到HIL启动指令，脚本开始运行...")
                    break
                time.sleep(0.5)
    else:
        print("\n🚀 自动启动脚本...")
    
    print("💡 提示：可以通过HIL服务发送手动纠正指令，格式：")
    print('{"type":"correct","action":"click","scene":"秘境入口","error_params":{"x":100,"y":200},"correct_params":{"x":150,"y":220},"reason":"坐标偏移导致点空"}')
    
    # 主循环
    loop_count = 0  # 新增：循环计数器，用于强制执行云端决策
    while True:
        try:
            loop_count += 1  # 新增：循环计数
            
            # 检查ESC键是否被按下（循环开始）
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            # ===================== HIL手动纠正核心逻辑（新增/修改） =====================
            # 检查HIL手动纠正指令前再次检查ESC键
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            correction = hil_client.get_manual_correction()
            if correction and correction.get("type") == "correct":
                print(f"🎮 收到HIL手动纠正指令：{correction}")
                action = correction.get("action")
                
                # 执行手动纠正操作
                if action == "click":
                    # 执行点击操作（使用结构化的correct_params）
                    correct_params = correction.get("correct_params", {})
                    click_x = correct_params.get("x")
                    click_y = correct_params.get("y")
                    if click_x is not None and click_y is not None:
                        # 检查坐标是否在窗口区域内
                        region = config["window_region"]
                        if region[0] <= click_x <= region[0] + region[2] and region[1] <= click_y <= region[1] + region[3]:
                            human_click(click_x, click_y, config)
                            print(f"✅ 执行手动纠正点击：({click_x}, {click_y})")
                        else:
                            print(f"❌ 手动点击坐标超出窗口区域：({click_x}, {click_y})")
                
                elif action == "stop":
                    # 停止脚本
                    print("🛑 收到停止指令，脚本已停止！")
                    exit(0)
                
                elif action == "reset":
                    # 重置状态
                    print("🔄 收到重置指令，重置状态！")
                    failed_attempts = 0
                
                # 核心新增：将手动纠正指令发送给agent，供agent学习
                hil_client.send_correction_to_agent(correction)
                
                # 等待一段时间，避免连续执行相同指令
                time.sleep(1.0)
                continue
            elif correction and correction.get("type") == "none":
                # 无纠正指令，不做处理，继续执行地图探索
                hil_logger.debug("ℹ️ 无HIL纠正指令，继续执行地图探索")
                pass
            
            # ===================== 原有截图和状态检测逻辑 =====================
            # 截图前再次检查ESC键
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            # 截图
            screenshot = capture_screenshot(config["window_region"])
            if screenshot is None:
                failed_attempts += 1
                if failed_attempts >= config["max_failed_attempts"]:
                    print("⚠️ 连续截图失败，重新激活窗口...")
                    activate_window(window_handle)
                    failed_attempts = 0
                time.sleep(random.uniform(*config["wait_delay"]))
                continue
            
            # 重置失败次数
            failed_attempts = 0
            
            # 画面反馈处理：检查并关闭弹窗/对话框
            if is_personal_info_page(screenshot):
                close_popup(config, "personal_info")
                continue
            
            if is_dialog_page(screenshot, dialog_templates, config):
                close_popup(config, "dialog")
                continue
            
            # 初始化匹配结果
            battle_found = False
            pickup_found = False
            locator_found = False
            best_battle_val = 0
            best_pickup_val = 0
            best_locator_val = 0
            best_locator_pos = (0, 0)
            best_pickup_pos = (0, 0)
            best_pickup_template = None
            
            # 匹配战斗按钮前再次检查ESC键
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            # 匹配战斗按钮
            if battle_template is not None:
                battle_val, battle_pos = multi_scale_match(battle_template, screenshot, config)
                best_battle_val = battle_val
                battle_found = battle_val >= config["confidence_battle"]
                if battle_found:
                    print(f"⚔️ 检测到战斗按钮，匹配值：{battle_val:.2f}")
                    # 计算点击坐标（窗口区域偏移）
                    click_x = config["window_region"][0] + battle_pos[0] + (battle_template.shape[1]//2)
                    click_y = config["window_region"][1] + battle_pos[1] + (battle_template.shape[0]//2)
                    human_click(click_x, click_y, config)
                    # 战斗延迟
                    battle_delay = random.uniform(*config["battle_delay"])
                    print(f"⚔️ 战斗中，等待{battle_delay:.2f}秒...")
                    time.sleep(battle_delay)
                    continue
            
            # 匹配拾取物品前再次检查ESC键
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            # 匹配拾取物品
            best_pickup_val = 0
            best_pickup_pos = (0, 0)
            best_pickup_template = None
            if pickup_templates:
                for template_name, pickup_template in pickup_templates:
                    pickup_val, pickup_pos = multi_scale_match(pickup_template, screenshot, config)
                    if pickup_val > best_pickup_val:
                        best_pickup_val = pickup_val
                        best_pickup_pos = pickup_pos
                        best_pickup_template = pickup_template
                
                pickup_found = best_pickup_val >= config["confidence_pickup"]
                if pickup_found and best_pickup_template is not None:
                    print(f"🎁 检测到拾取物品，匹配值：{best_pickup_val:.2f}")
                    # 计算点击坐标
                    click_x = config["window_region"][0] + best_pickup_pos[0] + (best_pickup_template.shape[1]//2)
                    click_y = config["window_region"][1] + best_pickup_pos[1] + (best_pickup_template.shape[0]//2)
                    human_click(click_x, click_y, config)
                    # 拾取延迟
                    time.sleep(random.uniform(*config["wait_delay"]))
                    continue
            
            # 匹配定位器前再次检查ESC键
            if keyboard.is_pressed('esc'):
                print("\n🛑 检测到ESC键按下，脚本已停止！")
                exit(0)
            
            # 匹配定位器
            best_locator_template = None
            if locator_templates:
                for locator_name, locator_template in locator_templates:
                    locator_val, locator_pos = multi_scale_match(locator_template, screenshot, config)
                    if locator_val > best_locator_val:
                        best_locator_val = locator_val
                        best_locator_pos = locator_pos
                        best_locator_template = locator_template
                
                locator_found = best_locator_val >= config["confidence_map"]
                if locator_found and best_locator_template is not None:
                    # 新增：每10次循环强制使用云端决策，跳过定位器点击
                    if loop_count % 10 == 0:
                        print(f"[强制云端决策] 第{loop_count}次循环，跳过定位器点击，使用云端决策...")
                    else:
                        print(f"📍 检测到定位器，匹配值：{best_locator_val:.2f}")
                        
                        # 计算定位器在屏幕中的相对位置
                        screen_width = config["window_region"][2]
                        screen_height = config["window_region"][3]
                        locator_x = best_locator_pos[0] + (best_locator_template.shape[1]//2)
                        locator_y = best_locator_pos[1] + (best_locator_template.shape[0]//2)
                        
                        # 检查定位器是否在屏幕边缘
                        edge_threshold = 150  # 边缘阈值（像素）
                        need_drag = False
                        drag_direction = ""
                        
                        if locator_x < edge_threshold:
                            # 定位器在左侧边缘，向右拖动地图
                            need_drag = True
                            drag_direction = "right"
                            print(f"📍 定位器在左侧边缘（x={locator_x}），需要向右拖动地图")
                        elif locator_x > screen_width - edge_threshold:
                            # 定位器在右侧边缘，向左拖动地图
                            need_drag = True
                            drag_direction = "left"
                            print(f"📍 定位器在右侧边缘（x={locator_x}），需要向左拖动地图")
                        elif locator_y < edge_threshold:
                            # 定位器在上侧边缘，向下拖动地图
                            need_drag = True
                            drag_direction = "down"
                            print(f"📍 定位器在上侧边缘（y={locator_y}），需要向下拖动地图")
                        elif locator_y > screen_height - edge_threshold:
                            # 定位器在下侧边缘，向上拖动地图
                            need_drag = True
                            drag_direction = "up"
                            print(f"📍 定位器在下侧边缘（y={locator_y}），需要向上拖动地图")
                        
                        if need_drag:
                            # 拖动地图
                            drag_map(config, drag_direction, distance=250)
                            # 等待地图稳定后再次检测
                            continue
                        else:
                            # 计算点击坐标（窗口区域偏移）
                            click_x = config["window_region"][0] + best_locator_pos[0] + (best_locator_template.shape[1]//2)
                            click_y = config["window_region"][1] + best_locator_pos[1] + (best_locator_template.shape[0]//2) + config["pathfind_offset"]
                            human_click(click_x, click_y, config)
                            # 走路延迟
                            walk_delay = random.uniform(*config["walk_delay"])
                            print(f"🚶 移动中，等待{walk_delay:.2f}秒...")
                            time.sleep(walk_delay)
                            continue
            
            # 构建结构化游戏状态（适配HIL协议）
            game_state = {
                "current_state": "idle",
                "match_results": {
                    "battle": {"found": battle_found, "confidence": best_battle_val},
                    "pickup": {"found": pickup_found, "confidence": best_pickup_val},
                    "pathfind": {"found": locator_found, "confidence": best_locator_val}
                },
                "failed_attempts": failed_attempts,
                "time_elapsed": time.time() - start_time,
                "templates_loaded": {
                    "battle": battle_template is not None,
                    "pickup": len(pickup_templates) > 0,
                    "pathfind": len(locator_templates) > 0
                },
                "window_region": config["window_region"]  # 新增：窗口区域信息，供agent参考
            }
            
            # 发送结构化状态到HIL服务
            hil_client.send_status(game_state)
            
            # ===================== 获取agent学习后的决策（新增） =====================
            # 新增：每10次循环强制使用一次云端决策，确保云端决策功能能够被触发
            force_cloud_decision = (loop_count % 10 == 0)
            
            if force_cloud_decision:
                print(f"🔄 第{loop_count}次循环，强制使用云端决策...")
            
            # 优先从HIL获取agent学习后的决策，无则使用原有云端决策
            agent_decision = hil_client.get_agent_decision(game_state) or cloud_agent.get_decision(game_state)
            print(f"🌐 最终决策：{agent_decision['action']} - {agent_decision['reason']}")
            
            # 根据决策执行动作
            if agent_decision['action'] == 'explore':
                # 执行盲走探索
                blind_explore(config)
            elif agent_decision['action'] == 'wait':
                # 执行等待
                wait_delay = random.uniform(*config["wait_delay"])
                print(f"⏳ 等待中，等待{wait_delay:.2f}秒...")
                time.sleep(wait_delay)
            else:
                # 无目标或其他决策，执行盲走探索
                blind_explore(config)
            
            # 循环延迟
            loop_delay = random.uniform(*config["loop_delay"])
            time.sleep(loop_delay)
        
        except KeyboardInterrupt:
            print("\n🛑 脚本已手动停止！")
            exit(0)
        except Exception as e:
            print(f"❌ 主循环异常：{e}")
            failed_attempts += 1
            time.sleep(random.uniform(*config["wait_delay"]))
            if failed_attempts >= config["max_failed_attempts"]:
                print("⚠️ 连续异常，重新激活窗口...")
                activate_window(window_handle)
                failed_attempts = 0

import sys

if __name__ == "__main__":
    # 检查命令行参数
    auto_start = False
    if len(sys.argv) > 1 and sys.argv[1] == "--start":
        # 通过命令行参数启动
        print("🚀 通过命令行参数启动脚本...")
        auto_start = True
    main(auto_start)