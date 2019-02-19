from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_filename

from .context import Context

IMPACT_FONT = ImageFont.truetype(resource_filename(__name__, 'impact.ttf'), 32)
RESIZE_WIDTH = 1080

def caption(context: Context, image_path: str, text: str):
    img = Image.open(image_path)
    context.logger.debug("Loaded image, resizing")
    img = resize_proportional(img, RESIZE_WIDTH)
    context.logger.debug("Resized image: " + str((img.width, img.height)))
    draw = ImageDraw.Draw(img)

    context.logger.info("Image canvas ready")
    drawText(img, draw, text, "bottom")
    context.logger.info("Captioned image")
    img.save(image_path)

def resize_proportional(img: Image, to_width: int):
    to_height = int(img.height * (to_width / img.width))
    return img.resize((to_width, to_height), Image.BILINEAR)


# Below mostly a ripoff of https://github.com/lipsumar/meme-caption

def drawTextWithOutline(img, draw, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=IMPACT_FONT)
    draw.text((x+2, y-2), text,(0,0,0),font=IMPACT_FONT)
    draw.text((x+2, y+2), text,(0,0,0),font=IMPACT_FONT)
    draw.text((x-2, y+2), text,(0,0,0),font=IMPACT_FONT)
    draw.text((x, y), text, (255,255,255), font=IMPACT_FONT)
    return

def drawText(img, draw, text, pos):
    text = text.upper()
    w, h = draw.textsize(text, IMPACT_FONT) # measure the size the text will take

    lineCount = 1
    if w > img.width:
        lineCount = int(round((w / img.width) + 1))

    # print("lineCount: {}".format(lineCount))

    lines = []
    if lineCount > 1:

        lastCut = 0
        isLast = False
        for i in range(0,lineCount):
            if lastCut == 0:
                cut = (len(text) // lineCount) * i
            else:
                cut = lastCut

            if i < lineCount-1:
                nextCut = (len(text) // lineCount) * (i+1)
            else:
                nextCut = len(text)
                isLast = True

            # print("cut: {} -> {}".format(cut, nextCut))

            # make sure we don't cut words in half
            if nextCut == len(text) or text[nextCut] == " ":
                # print("may cut")
                pass
            else:
                # print("may not cut")
                while text[nextCut] != " ":
                    nextCut += 1
                # print("new cut: {}".format(nextCut))

            line = text[cut:nextCut].strip()

            # is line still fitting ?
            w, h = draw.textsize(line, IMPACT_FONT)
            if not isLast and w > img.width:
                # print("overshot")
                nextCut -= 1
                while text[nextCut] != " ":
                    nextCut -= 1
                # print("new cut: {}".format(nextCut))

            lastCut = nextCut
            lines.append(text[cut:nextCut].strip())

    else:
        lines.append(text)

    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 10

    for i in range(0, lineCount):
        w, h = draw.textsize(lines[i], IMPACT_FONT)
        x = img.width//2 - w//2
        y = lastY + h
        drawTextWithOutline(img, draw, lines[i], x, y)
        lastY = y