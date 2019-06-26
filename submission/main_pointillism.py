import cv2
import argparse
import math
import progressbar
from pointillism import *

def pointillism(img_path, colors):
    img = cv2.imread(img_path)
    print("image path", img_path)
    
    stroke_scale = int(math.ceil(max(img.shape) / 1000))
    print("Automatically chosen stroke scale: %d" % stroke_scale)


    gradient_smoothing_radius = int(round(max(img.shape) / 50))
    print("Automatically chosen gradient smoothing radius: %d" % gradient_smoothing_radius)


    # convert the image to grayscale to compute the gradient
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    palette_size = 20
    print("Computing color palette...")
    palette = ColorPalette(colors)

    print("Extending color palette...")
#     palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])

    # display the color palette
    # cv2.imshow("palette", palette.to_image())
    # cv2.waitKey(200)

    print("Computing gradient...")
    gradient = VectorField.from_gradient(gray)

    print("Smoothing gradient...")
    gradient.smooth(gradient_smoothing_radius)

    print("Drawing image...")
    # create a "cartonized" version of the image to use as a base for the painting
    res = cv2.medianBlur(img, 11)
    # define a randomized grid of locations for the brush strokes
    grid = randomized_grid(img.shape[0], img.shape[1], scale=3)
    batch_size = 10000

    bar = progressbar.ProgressBar()
    for h in bar(range(0, len(grid), batch_size)):
        # get the pixel colors at each point of the grid
        pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
        # precompute the probabilities for each color in the palette
        # lower values of k means more randomnes
        color_probabilities = compute_color_probabilities(pixels, palette, k=9)

        for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
            color = color_select(color_probabilities[i], palette)
            angle = math.degrees(gradient.direction(y, x)) + 90
            length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))

            # draw the brush stroke
            cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)


    # cv2.imshow("res", limit_size(res, 1080))
    cv2.imwrite(img_path, res)
