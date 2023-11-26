from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Render your scatter plot here using GLScatterPlotItem

    # Save the model-view matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Set the projection matrix to an orthographic view
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Set the position for the text
    glWindowPos2d(10, 10)  # Adjust the coordinates as per your requirement
    text = "Your Text Here"

    # Render the text using OpenGL's built-in bitmap font
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glutSwapBuffers()

# Initialize OpenGL and create a window
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Scatter Plot with Text")

glutDisplayFunc(render)
glutMainLoop()