import pytesseract
from PIL import Image, ImageOps, ImageEnhance
from PIL import ImageFilter
import glob
import os
import argparse
import cv2
from easyocr import Reader


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    # (https://www.pyimagesearch.com/2020/09/14/getting-started-with-easyocr-for-optical-character-recognition/)
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


if __name__ == '__main__':
    path_to_imgs = "D:\\Bathymetric Mapping\\Images\\OCR_tests\\"
    path_to_formated_images = "D:\\Bathymetric Mapping\\Images\\OCR_tests\\processed_images\\"
    reader = Reader(["en"], gpu=False)

    # finding the files
    for filename in glob.glob(os.path.join(path_to_imgs, '*.jpg')):
        img = Image.open(filename)

        # processing the files
        # boosting contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(4)

        # make black and white
        img = img.convert('1')

        # define edges
        sharpen_rounds = 4
        for i in range(sharpen_rounds):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # convert to pure black or pure white
        pixels = img.load()
        for r in range(img.size[0]):  # for every pixel:
            for c in range(img.size[1]):
                if 0 < pixels[r, c] < 255:
                    print(pixels[r, c])

                if pixels[r, c] < 128:
                    pixels[r, c] = 0
                else:
                    pixels[r, c] = 255

        # saving the
        fp = filename.split("\\")[-1]
        img.save(path_to_formated_images+fp)

    for filename in glob.glob(os.path.join(path_to_imgs+"processed_images\\", '*.jpg')):
        number = float(filename.split("_")[-1].split(".")[0])

        easy_results = reader.readtext(filename)

        # getting the output from the top left box
        top_left_box_value = -1
        top_left_distance = (1920**2 + 1080**2) ** 0.5
        for result in easy_results:
            coordinates = result[0]
            x = coordinates[0][0]
            y = coordinates[0][1]
            dist = (x**2 + y**2) ** 0.5

            if dist < top_left_distance:
                try:
                    top_left_box_value = float(result[1])
                    top_left_distance = dist
                except ValueError:
                    try:
                        val = result[1].replace(" ", "")
                        val = val.replace("B", "3")
                        val = val.replace(":", "1")
                        top_left_box_value = float(val)
                        top_left_distance = dist
                    except ValueError:
                        pass

        # img = Image.open(filename)
        # tess_result = pytesseract.image_to_string(img, config='outputbase digits')
        print("number {}, file {}".format(number, filename))
        print("number {} read from easyocr at {:.2f} pixels from top left\n".format(top_left_box_value,
                                                                                     top_left_distance))
