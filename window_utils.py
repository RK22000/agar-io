import pywinctl

AGARIO_TITLE_SUBSTRING = "Agar.io"


def find_agario():
    a = pywinctl.getWindowsWithTitle(AGARIO_TITLE_SUBSTRING, condition=pywinctl.Re.CONTAINS)[0]
    res = {
        "x": a.left,
        "y": a.top,
        "width": a.width,
        "height": a.height,
    }
    return res


if __name__ == '__main__':
    # Example
    info = find_agario()
    if info:
        print(f"Position: ({info['x']}, {info['y']})")
        print(f"Size: ({info['width']} x {info['height']})")
