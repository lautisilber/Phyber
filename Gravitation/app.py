from PIL import Image
import numpy as np

size = (1000, 800)
frameBuffer = np.zeros((size[1], size[0], 3), dtype=np.uint8)

def draw(x, y, col):
    assert len(col) == 3
    if x >= 0 and y >= 0 and x < size[0] and y < size[1]:
        frameBuffer[y][x] = col

def draw_buffered(x, y, buffer):
    if x >= 0 and y >= 0 and x < size[0] and y < size[1]:
        buffer[y][x] = True

def draw_line(pos1, pos2, col):
    # borrowed from javidx's olcConsoleGameEngine
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    dx = x2 - x1
    dy = y2 - y1
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
            draw(x, y, col)

def draw_line_buffered(pos1, pos2, buffer):
    # borrowed from javidx's olcConsoleGameEngine
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    dx = x2 - x1
    dy = y2 - y1
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

        draw_buffered(x, y, buffer)

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
            draw_buffered(x, y, buffer)

    else:
        if dy >= 0:
            x = x1
            y = y1
            ye = y2
        else:
            x = x2
            y = y2
            ye = y1

        draw_buffered(x, y, buffer)

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
            draw_buffered(x, y, buffer)

def draw_triangle(verts, col):
    assert len(verts) == 3
    draw_line(verts[0], verts[1], col)
    draw_line(verts[1], verts[2], col)
    draw_line(verts[2], verts[0], col)

def draw_triangle_buffered(verts, buffer):
    assert len(verts) == 3
    draw_line_buffered(verts[0], verts[1], buffer)
    draw_line_buffered(verts[1], verts[2], buffer)
    draw_line_buffered(verts[2], verts[0], buffer)

def fill_triangle(verts, col):
    tempBuffer = np.zeros((size[0], size[1]), dtype=np.bool)
    draw_triangle_buffered(verts, tempBuffer)

    for r in range(size[1]):
        raster = False
        left = -1
        right = -1
        for i in range(len(tempBuffer[r])):
            if tempBuffer[r][i] == True:
                left = i
                break
        for i in range(len(tempBuffer[r]) - 1, -1, -1):
            if tempBuffer[r][i] == True:
                right = i
                break
        if left == -1:
            pass
        else:
            if right == -1:
                frameBuffer[r][left] = col
            else:
                for i in range(left, right + 1):
                    frameBuffer[r][i] = col
        

def save_image():
    vert1 = [500, 200]
    vert2 = [300, 400]
    vert3 = [700, 400]
    verts = [vert1, vert2, vert3]
    #draw_triangle(verts, [255, 255, 255])
    fill_triangle(verts, [255, 255, 255])
    img = Image.fromarray(frameBuffer, 'RGB')
    img.save('test_pil.png')


save_image()