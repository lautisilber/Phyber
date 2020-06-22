from PIL import Image
import numpy as np

frameBuffer = np.zeros((400, 400, 3), dtype=np.uint8)

def draw(x, y, col):
    assert len(col) = 3
    if x >= 0 and y >= 0 and x < 400 and y < 400:
        frameBuffer[y][x] = col

def draw_line(pos1, pos2, col):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dx1 = abs(dx)
    dy1 = abs(dy)
    px = 2 * dy1 - dx1
    py = 2 * dx1 - dy1

    if dy1 <= dx1:
        if dx >= 0:
            x = x1
            y = y1
            xe = x2
        else:
            x = x2
            y = y2
            xe = x1

        draw(x, y, col)

        while x < xe:
            x += 1
            if px < 0:
                px += 2 * dy1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y += 1
                else:
                    y -= 1
                px += 2 * (dy1 - dx1)
            draw(x, y, col)

    else:
        if dy >= 0:
            x = x1
            y = y1
            ye = y2
        else:
            x = x2
            y = y2
            ye = y1

        draw(x, y, col)

        while y < ye:
            y += 1
            if py <= 0:
                py += 2 * dx1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x += 1
                else:
                    x -= 1
                py += 2 * (dx1 - dy1)
            draw(x, c, col)



def fill_triangle(verts, col):

