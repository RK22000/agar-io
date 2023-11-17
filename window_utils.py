import pywinctl

AGARIO_TITLE_SUBSTRING = "Agar.io"

correction_biases = {
    'left':   20,
    'top':    109,
    'width': -40,
    'height':-160,
}
def find_agario():
    a = pywinctl.getWindowsWithTitle(AGARIO_TITLE_SUBSTRING, condition=pywinctl.Re.CONTAINS)[0]
    res = {
        "left":     a.left  + correction_biases['left'],
        "top":      a.top   + correction_biases['top'],
        "width":    a.width + correction_biases['width'],
        "height":   a.height+ correction_biases['height'],
    }
    return res


if __name__ == '__main__':
    # Example
    info = find_agario()
    if info:
        print(f"Position: ({info['x']}, {info['y']})")
        print(f"Size: ({info['width']} x {info['height']})")
