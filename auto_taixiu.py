import json
import os
from datetime import datetime
import requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    config["system_status"]["last_updated"] = datetime.now().isoformat()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def fetch_game_data():
    """
    TODO: Thay bằng API/scrape thực tế từ https://play-sunwin.agency
    Hiện tại trả về dữ liệu mẫu để test.
    """
    # Ví dụ:
    # url = "https://play-sunwin.agency/api/taixiu/history"
    # resp = requests.get(url, timeout=10)
    # data = resp.json()
    # return data["dice"], data["session"]
    return [3, 4, 6], "3260785"

def analyze_trend(dice_history, window=10):
    if not dice_history:
        return "Tài"
    recent = dice_history[:window]
    tai = sum(1 for d in recent if sum(d) > 10)
    xiu = len(recent) - tai
    if tai >= 6:
        return "Xỉu"
    elif xiu >= 6:
        return "Tài"
    else:
        last_total = sum(recent[0])
        return "Tài" if last_total > 10 else "Xỉu"

def main():
    print(f"[{datetime.now()}] Bắt đầu phân tích...")
    config = load_config()

    try:
        new_dice, session = fetch_game_data()
        print(f"Phiên {session}: {new_dice} -> Tổng {sum(new_dice)}")
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        return

    history = config["game_info"].get("dice_history", [])
    if new_dice not in history:
        history.insert(0, new_dice)
    config["game_info"]["dice_history"] = history[:10]
    config["game_info"]["current_session"] = session
    config["game_info"]["last_result"] = "Tài" if sum(new_dice) > 10 else "Xỉu"

    prediction = analyze_trend(config["game_info"]["dice_history"])
    print(f"Dự đoán phiên tới: {prediction}")
    config["system_status"]["last_prediction"] = prediction

    save_config(config)
    print("Đã lưu config.json")

if __name__ == "__main__":
    main()
