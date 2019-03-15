#include <GLUT/glut.h>
#include <fstream>
#include <cmath>
GLUquadricObj *quadObj;
float theta = 0.0;
int increment = 40;
int size;
bool MojaveWorkAround = true;
void display(void)
{
    if(MojaveWorkAround)
    {
        glutReshapeWindow(2 * size,2 * size);//Necessary for Mojave. Has to be different dimensions than in glutInitWindowSize();
        MojaveWorkAround = false;
    }
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    theta += 0.001;
    glBegin(GL_POINTS);
    for(int radius = 0;radius <= size; radius += increment)
        glVertex2f((float)radius * cos(theta),(float)radius * sin(theta));
    glEnd();
    glutSwapBuffers();
    glutPostRedisplay();//Necessary for Mojave.
}
static void Key(unsigned char key, int x, int y)
{
    switch (key)
    {
        case 'q':gluDeleteQuadric(quadObj);exit(0);
        case '\033':gluDeleteQuadric(quadObj);exit(0);
    }
}
int main(int argc, char **argv)
{
    size = 10 * increment;
    glutInit(&argc, argv);
    glutInitWindowSize(size,size);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutCreateWindow("My OpenGL Window");
    glutDisplayFunc(display);
    glClear(GL_COLOR_BUFFER_BIT);
    glutKeyboardFunc(Key);
    glClearColor(1.0,1.0,1.0,1.0);
    gluOrtho2D(- size,size,- size,size);
    glEnable(GL_POINT_SMOOTH);
    glPointSize(20.0);
    glColor4f(1.0,0.0,0.0,1.0);
    glutMainLoop();
    return 0;
}
