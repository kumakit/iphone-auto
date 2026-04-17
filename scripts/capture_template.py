import sys
import os
import time
import cv2
import pyautogui

# 親ディレクトリをパスに追加してsrcをインポート可能にする
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from window_helper import get_iphone_mirroring_window_region
from vision import Vision

def main():
    print("=== iPhone Template Capture Tool ===")
    
    # 1. ウィンドウの検出
    region = get_iphone_mirroring_window_region()
    if not region:
        print("Error: iPhone Mirroring window not found.")
        return

    print(f"Window found at: {region}")
    v = Vision(workspace_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # 2. アプリ名と保存名の取得
    app_name = input("Enter app name (e.g., pully, torima): ").strip()
    if not app_name:
        app_name = "pully"
    v.set_app(app_name)

    filename = input("Enter template filename (e.g., ad_close.png): ").strip()
    if not filename.endswith('.png'):
        filename += '.png'
    
    save_path = os.path.join(v.template_dir, filename)
    
    print("\nHow to use:")
    print("1. Move mouse to the TOP-LEFT corner of the target button.")
    print("2. Wait 3 seconds...")
    time.sleep(3)
    p1 = pyautogui.position()
    print(f"Point 1 captured: {p1}")
    
    print("\n3. Move mouse to the BOTTOM-RIGHT corner of the target button.")
    print("4. Wait 3 seconds...")
    time.sleep(3)
    p2 = pyautogui.position()
    print(f"Point 2 captured: {p2}")
    
    # 3. キャプチャとクロップ
    # 全画面をキャプチャしてから、ウィンドウ相対座標を計算
    full_img = v.capture_screen("temp_capture.png")
    if full_img is None:
        print("Error: Failed to capture screen.")
        return
    
    # スクリーン絶対座標からウィンドウ相対座標、そして画像上のピクセル座標へ
    # vision.py の capture_screen(region=region) は、screencapture -x で撮った後のクロップ
    # screencapture は Retina ディスプレイだとピクセル数が2倍になることがある
    
    # とりあえず、pyautogui の座標系でクロップ範囲を決定
    x1, y1 = min(p1.x, p2.x), min(p1.y, p2.y)
    x2, y2 = max(p1.x, p2.x), max(p1.y, p2.y)
    w, h = x2 - x1, y2 - y1
    
    if w <= 0 or h <= 0:
        print("Error: Invalid region selected.")
        return

    # スクリーンショット全体のサイズ
    screen_h, screen_w = full_img.shape[:2]
    # pyautogui の座標系（ポイント）と OpenCV の座標系（ピクセル）の比率を考慮
    # Mac の Retina 等ではピクセル比が異なる場合がある
    # ここではシンプルにフルスクリーンキャプチャから抽出する
    
    # vision.py の capture_screen は screencapture を使っている。
    # screencapture で保存した画像(full_img)から、絶対座標(x1, y1, w, h)でクロップを試みる
    # Retinaの場合、full_img の解像度は倍になっている可能性があるため調整が必要
    
    # 画面解像度とピクセル解像度の比率を取得
    screen_w_pts, screen_h_pts = pyautogui.size()
    screen_h_pix, screen_w_pix = full_img.shape[:2]
    
    ratio_w = screen_w_pix / screen_w_pts
    ratio_h = screen_h_pix / screen_h_pts
    
    ix1, iy1, iw, ih = int(x1 * ratio_w), int(y1 * ratio_h), int(w * ratio_w), int(h * ratio_h)
    
    cropped = full_img[iy1:iy1+ih, ix1:ix1+iw]
    
    if cropped.size == 0:
        print("Error: Cropped image is empty. Check coordinates.")
        return
        
    cv2.imwrite(save_path, cropped)
    print(f"\nSuccess! Template saved to: {save_path}")
    print(f"Selection size: {w}x{h} points ({iw}x{ih} pixels)")

if __name__ == "__main__":
    main()
