import os
import subprocess
import cv2
import numpy as np
from datetime import datetime

class Vision:
    def __init__(self, workspace_dir="~/dev/iphone-auto"):
        self.workspace_dir = os.path.expanduser(workspace_dir)
        self.log_dir = os.path.join(self.workspace_dir, "logs")
        self.template_dir = os.path.join(self.workspace_dir, "images")
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def capture_screen(self, filename=None):
        """スクリーンショットを取得して OpenCV 形式で返す"""
        if filename is None:
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        path = os.path.join(self.log_dir, filename)
        
        # macOS native screencapture command (more reliable than pyautogui in some cases)
        try:
            subprocess.run(["screencapture", "-x", path], check=True)
            img = cv2.imread(path)
            if img is not None:
                print(f"Captured screen to {path}")
                return img
        except Exception as e:
            print(f"screencapture failed: {e}")
            
        return None

    def find_template(self, screen_img, template_name, threshold=0.8):
        """テンプレート画像がスクリーン内に存在するか検索する"""
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.exists(template_path):
            print(f"Template not found: {template_path}")
            return None
            
        template = cv2.imread(template_path)
        res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return {"center": center, "confidence": max_val, "rect": (max_loc[0], max_loc[1], w, h)}
            
        return None

if __name__ == "__main__":
    v = Vision()
    img = v.capture_screen("test_capture.png")
    if img is not None:
        print("Vision test successful.")
