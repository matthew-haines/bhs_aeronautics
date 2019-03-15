#include <GLFW/glfw3.h>
#include <glm/glm.hpp> 
#include <stdlib.h>
#include <cmath>
#include <stdio.h>

static void error_callback(int error, const char* description) {
    fputs(description, stderr);
}

static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GL_TRUE);
}

static void renderGrid(int rows, int columns) {
    glBegin(GL_LINES);
    for (int i = 0; i <= rows; i++) {
        glVertex2f(0, i);
        glVertex2f(columns, i);
    }
    for (int i = 0; i < columns; i++) {
        glVertex2f(i, 0);
        glVertex2f(i, rows);
    }
    glEnd();
}

int main(void) {
    GLFWwindow* window;
    glfwSetErrorCallback(error_callback);
    if (!glfwInit())
        exit(EXIT_FAILURE);
    window = glfwCreateWindow(640, 480, "Simple example", NULL, NULL);
    if (!window) {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }
    glfwMakeContextCurrent(window);
    glfwSetKeyCallback(window, key_callback);

    const double maxFPS = 60;
    const double timings = 1.0 / maxFPS;
    double lastframeTime = glfwGetTime();

    int frameCount = 0;
    double previousTime = glfwGetTime();

    while (!glfwWindowShouldClose(window)) {
        if (glfwGetTime() - lastframeTime >= timings) {
            float ratio;
            int width, height;
            glfwGetFramebufferSize(window, &width, &height);
            ratio = width / (float) height;
            glViewport(0, 0, width, height);

            double currentTime = glfwGetTime();
            frameCount++;

            if (currentTime - previousTime >= 1.0) {
                printf("Framerate: %d\n", frameCount);
                frameCount = 0;
                previousTime = currentTime;
            }

            glClear(GL_COLOR_BUFFER_BIT);
            glMatrixMode(GL_PROJECTION);

            glLoadIdentity();
            glOrtho(-ratio, ratio, -1.f, 1.f, 1.f, -1.f);
            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();
            glRotatef(glfwGetTime() * 5.f, 0.f, 0.f, 1.f);

            glBegin(GL_TRIANGLES);
            glColor3f(1.f, 0.f, 0.f);
            glVertex3f(-0.5f, -0.43f, 0.f);
            glColor3f(0.f, 1.f, 0.f);
            glVertex3f(0.5f, -0.43f, 0.f);
            glColor3f(0.f, 0.f, 1.f);
            glVertex3f(0.f, 0.43f, 0.f);
            glEnd();
            
            glPopMatrix();

            renderGrid(5, 5);

            glfwSwapBuffers(window);
            glfwPollEvents();

            lastframeTime = glfwGetTime();
        }
    }
    glfwDestroyWindow(window);
    glfwTerminate();
    exit(EXIT_SUCCESS);
}
