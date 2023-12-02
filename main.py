import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
from OpenGL.GLU import *
import math

corr = -0.7

field_width = 1.5
field_height = 1.5
size = 0

MAX_CORR = 100  # max size of field

locators = [('A0', 10, 10, 2500),
            ('A1', 10, 40, 5000),
            ('A2', 80, 40, 2500),
            ('A3', 70, 80, 5000)]

emitters = [(5000, 20, 1, 30, 2),
            (5000, 40, 1, 50, 2),
            (5000, 70, 10, 60, 2),
            (5000, 30, 1, 50, 2)]


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
    glLineWidth(2.0)

    glBegin(GL_LINE_STRIP)

    last_pos_x, last_pos_y, last_freq = 0, 0, 0

    for i in range(0, len(data)):
        glColor3f(1.0, 1.0, 0.0)
        glVertex2f(data[i][1] / MAX_CORR * 1.5 + corr, data[i][3] / MAX_CORR * 1.5 + corr)

        last_pos_x = data[i][1]
        last_pos_y = data[i][3]
        last_freq = data[i][0]

    glEnd()

    for i in range(len(data)):
        draw_circle(((data[i][2] + data[i][4]) / 2) / MAX_CORR * 1.5,
                    (data[i][1] / MAX_CORR * 1.5 + corr, data[i][3] / MAX_CORR * 1.5 + corr))

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
    draw_emitter(emitters)
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
