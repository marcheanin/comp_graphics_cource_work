import math

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

import points_dealing

corr = -0.7

field_width = 1.5
field_height = 1.5
size = 0

MAX_CORR = 75  # max size of field

locators = [['A0', 40, 20, 2500],
            ['A1', 20, 40, 5000],
            ['A2', 60, 40, 2500]]

emitter_trace = [(5000, 20, 1, 30, 2),
                 (5000, 40, 1, 50, 2),
                 (5000, 70, 10, 60, 2),
                 (5000, 30, 1, 50, 2)]

emitters = {}

data = [(5000, 10, 10, 10),
        (5000, math.sqrt(600), math.sqrt(300), math.sqrt(500)),
        #(2500, 30, 70, 50),
        (5000, math.sqrt(1000), math.sqrt(400), math.sqrt(700))]
        #(2500, 30, 30, 30)]


def emulate_moving():
    pass


def draw_locators(data: dict):
    pass


def draw_field():
    glBegin(GL_LINES)

    zero_cords = (corr, corr)
    y_cords = (corr, field_width + corr)
    x_cords = (field_width + corr, corr)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0 + corr, 0 + corr)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0 + corr, field_width + corr)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0 + corr, 0 + corr)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(field_height + corr, 0 + corr)

    glEnd()

    i = zero_cords[0]
    cord = 0
    cord_step = MAX_CORR / 10
    fin = x_cords[0]
    step = abs(zero_cords[0] - x_cords[0]) / 10

    while i < fin + 0.1:
        text = str(int(cord))
        glRasterPos2d(i, corr - 0.02)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(char))

        i += step
        cord += cord_step

    i = zero_cords[0]
    cord = 0
    cord_step = MAX_CORR / 10
    fin = x_cords[0]
    step = abs(zero_cords[0] - x_cords[0]) / 10

    i += step
    cord += cord_step

    while i < fin + 0.1:
        text = str(int(cord))
        glRasterPos2d(corr - 0.07, i)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(char))

        i += step
        cord += cord_step


def draw_circle(radius, center):
    glBegin(GL_LINE_LOOP)

    line_amount = 50
    twice_pi = 2.0 * 3.1415

    for i in range(line_amount):
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex2f(
            center[0] + (radius * math.cos(i * twice_pi / line_amount)),
            center[1] + (radius * math.sin(i * twice_pi / line_amount))
        )

    glEnd()


def draw_emitter(data: list):
    print(data)
    glLineWidth(2.0)

    glBegin(GL_LINE_STRIP)

    last_pos_x, last_pos_y, last_freq = 0, 0, 0

    for i in range(0, len(data)):
        glColor3f(1.0, 1.0, 0.0)
        glVertex2f(data[i][1] / MAX_CORR * 1.5 + corr, data[i][2] / MAX_CORR * 1.5 + corr)

        last_pos_x = data[i][1]
        last_pos_y = data[i][2]
        last_freq = data[i][0]

    glEnd()

    for i in range(len(data)):
        draw_circle(data[i][3] / MAX_CORR * 1.5,
                    (data[i][1] / MAX_CORR * 1.5 + corr, data[i][2] / MAX_CORR * 1.5 + corr))

    glColor3f(1.0, 1.0, 0.0)
    text = "(" + str(last_freq) + ")" + " x: " + str(last_pos_x) + " y: " + str(last_pos_y)
    glRasterPos2d((last_pos_x - 9) / MAX_CORR * 1.5 + corr, (last_pos_y + 3) / MAX_CORR * 1.5 + corr)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(char))


def draw_line(x1, y1, x2, y2, max_corr):
    glBegin(GL_LINES)

    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x1 / max_corr * 1.5 + corr, y1 / max_corr * 1.5 + corr)

    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x2 / max_corr * 1.5 + corr, y2 / max_corr * 1.5 + corr)

    glEnd()


def draw_receiver(name: str, x: int, y: int, max_corr, freq):
    glColor3f(0, 1.0, 0.0)
    text = "(" + name + ")" + " x: " + str(x) + " y: " + str(y) + " freq: " + str(freq)
    glRasterPos2d((x - 9) / max_corr * 1.5 + corr, (y + 3) / max_corr * 1.5 + corr)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(char))

    glPointSize(10)
    glBegin(GL_POINTS)

    glVertex3f(x / max_corr * 1.5 + corr, y / max_corr * 1.5 + corr, 0)

    glEnd()


def update_data():
    stop_data = []
    for elem in data:
        key = elem[0]
        val = tuple(elem[1:])
        if key not in emitters:
            emitters[key] = list()
            emitters[key].append(val)
        elif val not in emitters[key]:
            emitters[key].append(val)


def display(window):
    global field_height
    global field_width

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glutInit()

    glPushMatrix()
    draw_field()
    # draw_line(10, 10, 70, 70, 100)
    for elem in locators:
        # draw_receiver(70, 70, 100, 5000)
        draw_receiver(elem[0], elem[1], elem[2], MAX_CORR, elem[3])
    update_data()
    data_for_draw = []
    for key, val in emitters.items():
        for elem in val:
            cords = points_dealing.count_point_from_3_dists(locators[0][1], locators[0][2], elem[0],
                                                            locators[1][1], locators[1][2], elem[1],
                                                            locators[2][1], locators[2][2], elem[2])
            data_for_draw.append([key] + list(cords))
        draw_emitter(data_for_draw)
    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "visualizer", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    # glfw.set_key_callback(window, key_callback)
    # glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main()
