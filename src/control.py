import pyautogui
import time

class Control:
    def __init__(self, window_region=None):
        """
        window_region: (x, y, w, h) - iPhoneミラーリングのウィンドウ位置
        """
        self.window_region = window_region
        self.ratio_w = 1.0  # ピクセルからポイントへの変換倍率
        self.ratio_h = 1.0
        pyautogui.PAUSE = 1.0  # 各操作後の待機時間

    def set_window_region(self, region):
        self.window_region = region

    def set_ratio(self, ratio_w, ratio_h):
        self.ratio_w = ratio_w
        self.ratio_h = ratio_h

    def _to_screen_coords(self, x, y):
        """ウィンドウ内相対座標(pixel)をスクリーン絶対座標(point)に変換"""
        # 1. ピクセル座標をポイント座標に変換
        pt_x, pt_y = x / self.ratio_w, y / self.ratio_h
        
        # 2. ウィンドウのオフセットを加算
        if self.window_region:
            return (self.window_region[0] + pt_x, self.window_region[1] + pt_y)
        return (pt_x, pt_y)

    def tap(self, x, y):
        """指定した座標をタップ"""
        abs_x, abs_y = self._to_screen_coords(x, y)
        print(f"Tapping at ({abs_x}, {abs_y})")
        pyautogui.moveTo(abs_x, abs_y)
        time.sleep(0.2)
        pyautogui.click(abs_x, abs_y)

    def swipe(self, x1, y1, x2, y2, duration=0.5):
        """スワイプ操作"""
        abs_x1, abs_y1 = self._to_screen_coords(x1, y1)
        abs_x2, abs_y2 = self._to_screen_coords(x2, y2)
        print(f"Swiping from ({abs_x1}, {abs_y1}) to ({abs_x2}, {abs_y2})")
        pyautogui.moveTo(abs_x1, abs_y1)
        pyautogui.dragTo(abs_x2, abs_y2, duration=duration, button='left')

    def wait(self, seconds):
        """待機"""
        time.sleep(seconds)

if __name__ == "__main__":
    # テスト用
    ctrl = Control()
    print("Control test initialized.")
