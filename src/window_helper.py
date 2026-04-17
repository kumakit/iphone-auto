import subprocess
import os

def get_iphone_mirroring_window_region():
    """
    AppleScriptを使用して 'iPhone Mirroring' ウィンドウの (x, y, w, h) を取得する
    """
    script = '''
    tell application "System Events"
        set procNames to {"iPhone Mirroring", "iPhoneミラーリング"}
        repeat with procName in procNames
            try
                set p to first process whose name is procName
                set win to first window of p
                set pos to position of win
                set siz to size of win
                return (item 1 of pos as string) & "," & (item 2 of pos as string) & "," & (item 1 of siz as string) & "," & (item 2 of siz as string)
            end try
        end repeat
        return "not found"
    end tell
    '''
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        output = result.stdout.strip()
        if output == "not found" or not output:
            return None
        
        parts = [int(p) for p in output.split(',')]
        if len(parts) == 4:
            return tuple(parts)
            
    except Exception as e:
        print(f"Error getting window region: {e}")
        
    return None

if __name__ == "__main__":
    region = get_iphone_mirroring_window_region()
    if region:
        print(f"iPhone Mirroring found at: {region}")
    else:
        print("iPhone Mirroring not found. Please make sure it is running.")
