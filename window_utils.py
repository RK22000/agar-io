import subprocess
import sys

AGARIO_TITLE_SUBSTRING = "Agar.io"


def find_agario_x11():
    output = subprocess.check_output(['wmctrl', '-l', '-G']).decode('utf-8')
    lines = output.splitlines()
    for line in lines:
        if AGARIO_TITLE_SUBSTRING in line:
            parts = line.split()
            return {
                "window_id": parts[0],
                "desktop_id": parts[1],
                "x": int(parts[2]),
                "y": int(parts[3]),
                "width": int(parts[4]),
                "height": int(parts[5]),
                "window_title": ' '.join(parts[7:])
            }
    return None


def find_agario():
    if sys.platform == 'linux':
        return find_agario_x11()
    else:
        import pygetwindow
        return pygetwindow.getWindowsWithTitle(AGARIO_TITLE_SUBSTRING)[0]


if __name__ == '__main__':
    # Example
    info = find_agario()
    if info:
        print(f"Title: {info['window_title']}")
        print(f"Position: ({info['x']}, {info['y']})")
        print(f"Size: ({info['width']} x {info['height']})")
