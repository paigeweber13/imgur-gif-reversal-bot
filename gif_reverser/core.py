# -*- coding: utf-8 -*-

import cv2

class GifReverser:
    def __init__(self):
        pass

    def get_frames(self, gif_filename: str):
        vidcap = cv2.VideoCapture(gif_filename)
        framerate = vidcap.get(cv2.CAP_PROP_FPS)
        frames = []

        success,image = vidcap.read()
        while success:
            frames.append(image)
            success,image = vidcap.read()
        return (framerate, frames)

    # also works with mp4 files
    def reverse_gif(self, gif_filename: str, output_filename: str):
        framerate, frames = self.get_frames(gif_filename)
        height, width, layers = frames[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'),
                              framerate, size)

        for i in range(len(frames)-1, -1, -1):
            out.write(frames[i])
        out.release()
