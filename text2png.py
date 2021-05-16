from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def text2png(text,
             image_save_path,
             font_color="#000",
             background_color="#FFF",
             fontfullpath="MYRIADPRO-BOLD.OTF",
             fontsize=50,
             padding=20):
    font = ImageFont.truetype(fontfullpath, fontsize)

    lines = text.split("\n")

    line_height = int(font.getsize(lines[0])[1] * 1.6)
    img_height = int(line_height * len(lines) * 1.1)

    longest_line = ""

    for line in lines:
        if len(line) > len(longest_line):
            longest_line = line

    img_width = int(font.getsize(longest_line)[0] * 1.1)

    img = Image.new("RGBA", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        line_width = int(font.getsize(line)[0])

        draw.text((img_width / 2 - line_width / 2, y), line, font_color, font=font)
        y += line_height

    img.save(image_save_path)
