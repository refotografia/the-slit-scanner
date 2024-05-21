import imageio.v3 as iio
import numpy as np


def slitscan(
        video,
        width,
        height,
        x,
        y,
        velocity_x,
        velocity_y,
        out_width,
        out_height,
        out_x,
        out_y,
        out_velocity_x,
        out_velocity_y):

    reader = iio.imread(video, plugin="FFMPEG")

    # six args can contain % at the end, we check them here
    # and convert if necessary
    if type(height) == str:
        if height[-1] == '%':
            height = int(reader[1].shape[0] * float(height[:-1]) * 0.01)
        else:
            height = int(height)

    if type(width) == str:
        if width[-1] == '%':
            width = int(reader[1].shape[1] * float(width[:-1]) * 0.01)
        else:
            width = int(width)

    if type(x) == str:
        if x[-1] == '%':
            x = int(reader[1].shape[1] * float(x[:-1]) * 0.01)
        else:
            x = int(x)

    if type(y) == str:
        if y[-1] == '%':
            y = int(reader[1].shape[0] * float(y[:-1]) * 0.01)
        else:
            y = int(y)

    if type(out_width) == str:
        if out_width[-1] == '%':
            out_width = int(reader[1].shape[1] * float(out_width[:-1]) * 0.01)
        else:
            out_width = int(out_width)

    if type(out_height) == str:
        if out_height[-1] == '%':
            out_height = int(reader[1].shape[0] * float(out_height[:-1]) * 0.01)
        else:
            out_height = int(out_height)

    out = np.zeros(reader[1].shape, dtype=np.float32)
    # based on the second frame of the video, we are getting width and height
    # in pixels and the number of channels

    for f in range(0, len(reader)):
        img = reader[f]

        overlap = 1
        if out_velocity_x > 0 and out_velocity_y == 0:
            overlap = float(out_velocity_x) / out_width
        elif out_velocity_x == 0 and out_velocity_y > 0:
            overlap = float(out_velocity_y) / out_height
        elif out_velocity_x > 0 and out_velocity_y > 0:
            overlap = (float(out_velocity_x) / out_width) * (float(out_velocity_y) / out_height)
        if overlap > 1:
            overlap = 1

        out[out_y: out_y + out_height, out_x: out_x + out_width] += img[y: y + height, x: x + width] * overlap

        x += velocity_x
        y += velocity_y

        out_x += out_velocity_x
        out_y += out_velocity_y

    out = np.around(out).astype(np.uint8)
    return out
