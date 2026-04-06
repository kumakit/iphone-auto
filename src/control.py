import pyautogui
import time
import os

class Control:
    def __init__(self, window_region=None):
        """
        window_region: (x, y, w, h) - iPhoneミラーリングのウィンドウ位置
        """
        self.window_region = window_region
        pyautogui.PAUSE = 1.0  # 各操作後の待機時間

    def set_window_region(self, region):
        self.window_region = region

    def _to_screen_coords(self, x, y):
        """ウィンドウ内相対座標をスクリーン絶対座標に変換"""
        if self.window_region:
            return (self.window_region[0] + x, self.window_region[1] + y)
        return (x, y)

    def tap(self, x, y):
        """指定した座標をタップ"""
        abs_x, abs_y = self._to_screen_coords(x, y)
        print(f"Tapping at ({abs_x}, {abs_y})")
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
