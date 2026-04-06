import subprocess
import json

def get_window_list():
    # AppleScript to get window names and their bounds
    applescript = '''
    tell application "System Events"
        set windowList to {}
        set processList to every process whose background only is false
        repeat with proc in processList
            set procName to name of proc
            set winList to every window of proc
            repeat with win in winList
                set winName to name of win
                set winPos to position of win
                set winSize to size of win
                set end of windowList to {process:procName, name:winName, position:winPos, size:winSize}
            end repeat
        end repeat
        return windowList
    end tell
    '''
    try:
        result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
        # Note: osascript output formatting needs parsing, but let's just print it for now
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_window_list()
