from PIL import Image, ImageOps, ImageChops
import numpy

first_img_path = "samples/320_etalon.png"
second_img_path = "samples/320_.png"

with Image.open(first_img_path).convert('LA') as first:
    with Image.open(second_img_path).convert('LA') as second:
        if first.size[1] > second.size[1]:
            second = second.resize(first.size)
        else:
            first = first.resize(second.size)
        
        first = first.convert('RGBA')
        # NOTE: inverted image over initial should give monochromic color
        second = ImageOps.invert(second.convert('RGB')).convert('RGBA')
        
        first.putalpha(128)
        second.putalpha(128)
        first.paste(second, None, second)
        first = first.convert('RGB')
        first.save("overlay.png")
        
        np_im = numpy.array(first)
        width, height, colors_count = np_im.shape
        difference = 0
        
        for x in range(width):
            for y in range(height):
                if not numpy.array_equal([127, 127, 127], np_im[x][y]):
                    diffed_pixel = np_im[x][y]
                    difference += 1
                    diff_color = 255 - 2 * abs(127 - diffed_pixel[0])
                    np_im[x][y] = [255, diff_color, diff_color]
                else:
                    np_im[x][y] = [255, 255, 255]
        
        print("{:.2%}".format(difference / (width * height)))
        new_im = Image.fromarray(np_im)
        new_im.save("result.png")
        
