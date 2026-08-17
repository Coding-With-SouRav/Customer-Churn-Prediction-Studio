import math
from PIL import Image, ImageTk, ImageDraw

def draw_icon(app):
    size = 128
    icon_img = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )
    gradient = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )
    top_color = (0, 198, 174)
    bottom_color = (17, 24, 96)
    gradient_draw = ImageDraw.Draw(gradient)
    for y in range(size):
        ratio = y / (size - 1)
        r = int(
            top_color[0]
            + (bottom_color[0] - top_color[0]) * ratio
        )
        g = int(
            top_color[1]
            + (bottom_color[1] - top_color[1]) * ratio
        )
        b = int(
            top_color[2]
            + (bottom_color[2] - top_color[2]) * ratio
        )
        gradient_draw.line(
            [(0, y), (size, y)],
            fill=(r, g, b, 255)
        )
    mask = Image.new(
        "L",
        (size, size),
        0
    )
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        (0, 0, size, size),
        radius=26,
        fill=255
    )
    icon_img.paste(
        gradient,
        (0, 0),
        mask
    )
    draw = ImageDraw.Draw(icon_img)
    bar_color = (255, 255, 255, 200)
    bars = [
        (30, 90, 46, 100),
        (54, 75, 70, 100),
        (78, 55, 94, 100)
    ]
    for x0, y0, x1, y1 in bars:
        draw.rounded_rectangle(
            (x0, y0, x1, y1),
            radius=3,
            fill=bar_color
        )
    line_color = (255, 215, 0, 255)
    points = [
        (28, 95),
        (52, 65),
        (76, 45),
        (100, 25)
    ]
    draw.line(
        points,
        fill=line_color,
        width=5,
        joint="curve"
    )
    end_x, end_y = points[-1]
    prev_x, prev_y = points[-2]
    angle = math.atan2(
        end_y - prev_y,
        end_x - prev_x
    )
    arrow_len = 12
    arrow_angle = math.radians(28)
    x1 = (
        end_x
        - arrow_len * math.cos(angle - arrow_angle)
    )
    y1 = (
        end_y
        - arrow_len * math.sin(angle - arrow_angle)
    )
    x2 = (
        end_x
        - arrow_len * math.cos(angle + arrow_angle)
    )
    y2 = (
        end_y
        - arrow_len * math.sin(angle + arrow_angle)
    )
    draw.polygon(
        [
            (end_x, end_y),
            (x1, y1),
            (x2, y2)
        ],
        fill=line_color
    )
    icon_photo = ImageTk.PhotoImage(icon_img)
    app._icon_ref = icon_photo
    app.iconphoto(
        True,
        icon_photo
    )
