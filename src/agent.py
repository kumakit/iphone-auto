import sys
import time
import os
from enum import Enum, auto
from vision import Vision
from control import Control
from window_helper import get_iphone_mirroring_window_region

class State(Enum):
    IDLE = auto()
    POINT_READY = auto()   # 「ポイントゲット」ボタン待機
    AD_PLAYING = auto()    # 広告再生中（「×」印待機）
    POINT_RESULT = auto()  # 「獲得」ボタン待機
    UNKNOWN = auto()

class iPhoneAgent:
    def __init__(self, app_name="pully"):
        self.vision = Vision()
        self.vision.set_app(app_name)
        self.control = Control()
        self.state = State.IDLE
        self.is_running = False
        self.window_region = None
        self.app_name = app_name

    def update_window(self):
        """ウィンドウ位置を更新"""
        region = get_iphone_mirroring_window_region()
        if region:
            self.window_region = region
            self.control.set_window_region(region)
            return True
        return False

    def run(self):
        print(f"Starting Automation Agent for: {self.app_name}...")
        self.is_running = True
        
        try:
            while self.is_running:
                if not self.update_window():
                    print("Waiting for iPhone Mirroring window...")
                    time.sleep(5)
                    continue

                # 1. 画面キャプチャ
                img = self.vision.capture_screen("current_screen.png", region=self.window_region)
                if img is None:
                    time.sleep(2)
                    continue

                # 画面の状態が変わっている可能性があるので、最新のウィンドウ位置を取得
                self.update_window()

                # 2. 状態判定とアクション
                if hasattr(self.vision, 'ratio_w'):
                    self.control.set_ratio(self.vision.ratio_w, self.vision.ratio_h)
                
                self.process_cycle(img)

                time.sleep(1)
        except KeyboardInterrupt:
            print(f"Agent for {self.app_name} stopped by user.")
        finally:
            self.is_running = False

    def process_cycle(self, img):
        """現在の画面から状態を判定し、アクションを実行する"""
        
        # 判定用テンプレートのプレフィックス
        temp_ready_list = self.vision.list_templates(prefix="point_ready")
        temp_get_list = self.vision.list_templates(prefix="point_get")
        temp_ad_close_list = self.vision.list_templates(prefix="ad_close")

        # 1. ポイント獲得ボタンのチェック
        res_get = self.vision.find_any_template(img, temp_get_list)
        if res_get:
            template_name = res_get['template_name']
            print(f"\n>>> [HIT] {template_name} (信頼度: {res_get['confidence']:.2f}) -> ポイント獲得ボタンをタップ")
            # ファイル名に使用できない文字を置換
            safe_name = template_name.replace(".", "_")
            self.vision.save_visual_debug(img, res_get, f"match_get_{safe_name}.png")
            x, y = res_get["center"]
            self.control.tap(x, y)
            return

        # 2. ポイントゲット開始ボタンのチェック
        res_ready = self.vision.find_any_template(img, temp_ready_list)
        if res_ready:
            template_name = res_ready['template_name']
            print(f"\n>>> [HIT] {template_name} (信頼度: {res_ready['confidence']:.2f}) -> 開始ボタンをタップ")
            safe_name = template_name.replace(".", "_")
            self.vision.save_visual_debug(img, res_ready, f"match_ready_{safe_name}.png")
            x, y = res_ready["center"]
            self.control.tap(x, y)
            return

        # 3. 広告の×印のチェック
        res_ad = self.vision.find_any_template(img, temp_ad_close_list)
        if res_ad:
            template_name = res_ad['template_name']
            print(f"\n>>> [HIT] {template_name} (信頼度: {res_ad['confidence']:.2f}) -> 広告を閉じます")
            safe_name = template_name.replace(".", "_")
            self.vision.save_visual_debug(img, res_ad, f"match_ad_close_{safe_name}.png")
            x, y = res_ad["center"]
            self.control.tap(x, y)
            return


        print(".", end="", flush=True)  # スキャン中であることを示すドットを表示


if __name__ == "__main__":
    app_name = "pully"
    if len(sys.argv) > 1:
        app_name = sys.argv[1]
    
    agent = iPhoneAgent(app_name=app_name)
    agent.run()
