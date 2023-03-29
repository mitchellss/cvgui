import multiprocessing as mp
import sys
from typing import Literal
import pygame
import cv2
import mediapipe
import numpy as np

'''
THIS EXAMPLE:

Image capture running in the background.

Image display running in the main process.

Image data sent over queue
'''


'''
DESIRED:
    Main:
        UI
    Background:
        Capture
        Display?
        Processing

Skeleton data sent over queue
'''

'''
CURRENT:
    Main:
        Capture
        Display
        Processing
    Background:
        UI

Data transferred using global variable
'''

def capture_and_show(q):
    cap = cv2.VideoCapture(0)
    while True:
        suc, img = cap.read()
        if suc:
            q.put(img)
            cv2.imshow("Test", img)
            wait_key = cv2.waitKey(1)
            if wait_key == 27:
                pass

def process_image(image_queue, skeleton_queue):
    model = mediapipe.solutions.pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0)
    pose_array = np.zeros((33,4))
    while True:
        if image_queue.empty():
            continue
        frame = image_queue.get()
        skeleton_points = model.process(frame).pose_world_landmarks.landmark

        for landmark, _ in enumerate(skeleton_points):
            pose_array[landmark][0] = skeleton_points[landmark].x
            pose_array[landmark][1] = skeleton_points[landmark].y
            pose_array[landmark][2] = skeleton_points[landmark].z
            pose_array[landmark][3] = skeleton_points[landmark].visibility

        skeleton_queue.put(pose_array)
        

def main(skeleton_queue):
    CONNECTIONS: np.ndarray = np.array([
        [16, 14], [16, 18], [16, 20], [16, 22],
        [18, 20], [14, 12], [12, 11], [12, 24],
        [11, 23], [11, 13], [15, 13], [15, 17],
        [15, 19], [15, 21], [17, 19], [24, 23],
        [26, 24], [26, 28], [25, 23], [25, 27],
        [10, 9], [8, 6], [5, 6], [5, 4], [0, 4],
        [0, 1], [2, 1], [2, 3], [3, 7], [28, 32],
        [28, 30], [27, 29], [27, 31], [32, 30],
        [29, 31]
    ])
    LIMB_COLOR: tuple[Literal[255], Literal[255],
                      Literal[255]] = (255, 255, 255)
    LIMB_WIDTH: Literal[2] = 2

    LANDMARK_COLOR: tuple[Literal[0], Literal[255], Literal[0]] = (0, 255, 0)
    LANDMARK_RADIUS: Literal[5] = 5
    LANDMARK_OUTLINE_WIDTH: Literal[0] = 0

    NUM_LANDMARKS: Literal[33] = 33
    POINTS_PER_LANDMARK: Literal[4] = 4  # x, y, z, depth?

    X = 0
    Y = 1

    pygame.init()
    pygame.font.init()

    # Game Setup
    fps_clock = pygame.time.Clock()

    window: pygame.surface.Surface = pygame.display.set_mode(
        (1920//2, 1080//2))
    pygame.display.set_caption("cvgui")
    while True:
        window.fill((0,0,0))
        if skeleton_queue.empty():
            continue
        skeleton_points = skeleton_queue.get()
        skeleton_points[:, X] = skeleton_points[:, X] * \
            450 + 800 
        skeleton_points[:, Y] = skeleton_points[:, Y] * \
            450 + 600 
        # print(skeleton_points)
        for landmark_pair in CONNECTIONS:
            start_landmark: int = landmark_pair[X]
            end_landmark: int = landmark_pair[Y]
            line_start_x: float = skeleton_points[start_landmark][X]
            line_start_y: float = skeleton_points[start_landmark][Y]
            line_end_x: float = skeleton_points[end_landmark][X]
            line_end_y: float = skeleton_points[end_landmark][Y]
            pygame.draw.line(window, LIMB_COLOR,
                             [float(line_start_x), float(line_start_y)],
                             [float(line_end_x), float(line_end_y)],
                             LIMB_WIDTH)

        for _, landmark in enumerate(skeleton_points):
            point_x: float = landmark[X]
            point_y: float = landmark[Y]
            pygame.draw.circle(window, LANDMARK_COLOR,
                               [point_x, point_y],
                               LANDMARK_RADIUS,
                               LANDMARK_OUTLINE_WIDTH)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps_clock.tick(60)

if __name__ == '__main__':
    mp.set_start_method('spawn')
    image_queue = mp.Queue()
    skeleton_queue = mp.Queue()

    cap = mp.Process(target=capture_and_show, args=(image_queue,))
    proc = mp.Process(target=process_image, args=(image_queue,skeleton_queue))

    cap.start()
    proc.start()
    try:
        main(skeleton_queue)
    except KeyboardInterrupt:
        cap.kill()
        proc.kill()

    cap.join()