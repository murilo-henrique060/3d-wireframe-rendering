import pygame
import numpy as np

def point(x, y, z):
    return np.array([x, y, z])

def pointList(*args):
    return [point(*arg) for arg in args]

def rotateX(point, angle):
    cos = np.cos(angle)
    sin = np.sin(angle)

    rotationMatrix = np.array([
        [1, 0, 0],
        [0, cos, -sin],
        [0, sin, cos]
    ])

    return point @ rotationMatrix

def rotateY(point, angle):
    cos = np.cos(angle)
    sin = np.sin(angle)

    rotationMatrix = np.array([
        [cos, 0, sin],
        [0, 1, 0],
        [-sin, 0, cos]
    ])

    return point @ rotationMatrix

def rotateZ(point, angle):
    cos = np.cos(angle)
    sin = np.sin(angle)

    rotationMatrix = np.array([
        [cos, -sin, 0],
        [sin, cos, 0],
        [0, 0, 1]
    ])

    return point @ rotationMatrix

def project(point):
    x, y, z = point * 100

    D_y = y - camera[1]
    D_x = x - camera[0]

    d_y = window[1] - camera[1]
    d_x = d_y * D_x / D_y

    D_z = z - camera[2]
    d_z = d_y * D_z / D_y

    x_ = d_x + camera[0] + O[0]
    y_ = d_z + camera[2] + O[1]

    return (x_, y_)

# Constants

WINDOW_TITLE = "Pygame 3D"
WINDOW_SIZE = (800, 600)
O = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2) # Origin

window = point(-400, 100, -300)
camera = point(0, 400, 0)

class Object:
    def __init__(self, points, lines):
        self.points = pointList(*points)
        self.lines = lines

    def project(self):
        projectedPoints = []

        for p in self.points:
            projectedPoints.append(project(p))

        return projectedPoints

    def draw(self, screen):
        projectedPoints = self.project()

        for p in projectedPoints:
            pygame.draw.circle(screen, (255, 255, 255), p, 3)

        for l in self.lines:
            pygame.draw.line(screen, (255, 255, 255), projectedPoints[l[0]], projectedPoints[l[1]])

    def rotateX(self, angle):
        for i, p in enumerate(self.points):
            self.points[i] = rotateX(p, angle)

    def rotateY(self, angle):
        for i, p in enumerate(self.points):
            self.points[i] = rotateY(p, angle)

    def rotateZ(self, angle):
        for i, p in enumerate(self.points):
            self.points[i] = rotateZ(p, angle)

    def rotate(self, angleX=0, angleY=0, angleZ=0):
        self.rotateX(angleX)
        self.rotateY(angleY)
        self.rotateZ(angleZ)

class Cube(Object):
    def __init__(self, size=1, position=(0, 0, 0)):
        position = point(*position)

        super().__init__(
            points = [
                position + point(1, 1, 1) * size,
                position + point(1, 1, -1) * size,
                position + point(1, -1, -1) * size,
                position + point(1, -1, 1) * size,
                position + point(-1, 1, 1) * size,
                position + point(-1, 1, -1) * size,
                position + point(-1, -1, -1) * size,
                position + point(-1, -1, 1) * size
            ],
            lines = [
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0),
                (4, 5),
                (5, 6),
                (6, 7),
                (7, 4),
                (0, 4),
                (1, 5),
                (2, 6),
                (3, 7)
            ]
        )

cube = Cube(1)

pygame.init()

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

# Main loop

clock = pygame.time.Clock()

running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Draw
    screen.fill((0, 0, 0))

    cube.draw(screen)
    cube.rotate(0.01, 0, 0.01)

    clock.tick(120)

    # Flip the display
    pygame.display.flip()