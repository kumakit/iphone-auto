from vision import Vision
import time

def main():
    print("Starting iphone-auto test...")
    v = Vision()
    
    # テストキャプチャ
    img = v.capture_screen("initial_test.png")
    if img is not None:
        print("Initial screen capture successful.")
    else:
        print("Screen capture failed.")
        return

    # 10秒間、3秒おきにキャプチャする（動きを確認）
    for i in range(3):
        print(f"Loop {i+1}/3 - Capturing...")
        v.capture_screen(f"loop_{i+1}.png")
        time.sleep(3)

if __name__ == "__main__":
    main()
