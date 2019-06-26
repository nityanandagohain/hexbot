import cv2
import numpy as np
import math
from sklearn.cluster import KMeans
from .utils import limit_size, regulate


class ColorPalette:
    def __init__(self, colors):
        self.colors = colors
        self.base_len = len(colors)

    def to_image(self):
        cols = self.base_len
        rows = int(math.ceil(len(self.colors) / cols))

        res = np.zeros((rows * 80, cols * 80, 3), dtype=np.uint8)
        for y in range(rows):
            for x in range(cols):
                if y * cols + x < len(self.colors):
                    color = [int(c) for c in self.colors[y * cols + x]]
                    cv2.rectangle(res, (x * 80, y * 80), (x * 80 + 80, y * 80 + 80), color, -1)

        return res

    def __len__(self):
        return len(self.colors)

    def __getitem__(self, item):
        return self.colors[item]
