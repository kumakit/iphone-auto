import os
import subprocess
import cv2
import numpy as np
from datetime import datetime

class Vision:
    def __init__(self, workspace_dir="~/dev/iphone-auto"):
        self.workspace_dir = os.path.expanduser(workspace_dir)
        self.log_dir = os.path.join(self.workspace_dir, "logs")
        self.base_template_dir = os.path.join(self.workspace_dir, "images")
        self.template_dir = self.base_template_dir
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if not os.path.exists(self.base_template_dir):
            os.makedirs(self.base_template_dir)

    def set_app(self, app_name):
        """検索対象のアプリサブディレクトリを設定"""
        self.template_dir = os.path.join(self.base_template_dir, app_name)
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        print(f"Vision template directory set to: {self.template_dir}")

    def capture_screen(self, filename=None, region=None):
        """
        スクリーンショットを取得して OpenCV 形式で返す
        region: (x, y, w, h) が指定されている場合はその範囲でクロップする
        """
        if filename is None:
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        path = os.path.join(self.log_dir, filename)
        
        try:
            subprocess.run(["screencapture", "-x", path], check=True)
            img = cv2.imread(path)
            if img is not None:
                if region:
                    import pyautogui
                    # 座標（ポイント）とピクセル解像度の比率を計算
                    screen_w_pts, screen_h_pts = pyautogui.size()
                    screen_h_pix, screen_w_pix = img.shape[:2]
                    self.ratio_w = screen_w_pix / screen_w_pts
                    self.ratio_h = screen_h_pix / screen_h_pts

                    x, y, w, h = region
                    ix, iy, iw, ih = int(x * self.ratio_w), int(y * self.ratio_h), int(w * self.ratio_w), int(h * self.ratio_h)
                    
                    # 範囲が画像内に収まっているか確認
                    iy2, ix2 = min(iy+ih, screen_h_pix), min(ix+iw, screen_w_pix)
                    img = img[iy:iy2, ix:ix2]
                    
                    # クロップ後の画像も保存（デバッグ用）
                    crop_path = os.path.join(self.log_dir, "last_crop.png")
                    cv2.imwrite(crop_path, img)
                
                return img
        except Exception as e:
            print(f"Capture failed: {e}")
            
        return None

    def find_template(self, screen_img, template_name, threshold=0.8):
        """テンプレート画像がスクリーン内に存在するか検索する"""
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.exists(template_path):
            print(f"Template not found: {template_path}")
            return None
            
        template = cv2.imread(template_path)
        if template is None:
            return None
            
        # 安全チェック: テンプレートが画面より大きい場合は失敗させる
        h, w = template.shape[:2]
        sh, sw = screen_img.shape[:2]
        if h > sh or w > sw:
            print(f"Warning: Template {template_name} results in ({w}x{h}) which is larger than screen ({sw}x{sh})")
            return None

        res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return {"center": center, "confidence": max_val, "rect": (max_loc[0], max_loc[1], w, h)}
            
        return None

    def find_any_template(self, screen_img, template_names, threshold=0.8):
        """複数のテンプレートのうち、いずれかが存在するか検索する"""
        for name in template_names:
            res = self.find_template(screen_img, name, threshold)
            if res:
                res["template_name"] = name
                return res
        return None

    def list_templates(self, prefix=""):
        """登録されているテンプレート画像の一覧を取得"""
        if not os.path.exists(self.template_dir):
            return []
        
        files = os.listdir(self.template_dir)
        return [f for f in files if f.startswith(prefix) and f.endswith(('.png', '.jpg', '.jpeg'))]

    def save_visual_debug(self, screen_img, res, filename="last_match.png"):
        """マッチング箇所を可視化して保存"""
        debug_img = screen_img.copy()
        x, y, w, h = res["rect"]
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        # 信頼度も描画
        cv2.putText(debug_img, f"{res['confidence']:.2f}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        path = os.path.join(self.log_dir, filename)
        cv2.imwrite(path, debug_img)
        return path

if __name__ == "__main__":
    v = Vision()
    img = v.capture_screen("test_capture.png")
    if img is not None:
        print("Vision test successful.")
