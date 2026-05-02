import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agent import iPhoneAgent

def main():
    app_name = "pully"
    if len(sys.argv) > 1:
        app_name = sys.argv[1]
    
    print(f"--- Starting iphone-auto with app: {app_name} ---")
    print("Press Ctrl+C to stop.")
    
    agent = iPhoneAgent(app_name=app_name)
    agent.run()

if __name__ == "__main__":
    main()
