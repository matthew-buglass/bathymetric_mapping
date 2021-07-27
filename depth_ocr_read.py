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
        img.show()

        # processing the files
        # img = ImageOps.grayscale(img)
        # img.show()
        # x = input("continue?")

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        
        img = img.convert('1')

        sharpen_rounds = 4
        for i in range(sharpen_rounds):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # saving the
        fp = filename.split("\\")[-1]
        img.save(path_to_formated_images+fp)

    for filename in glob.glob(os.path.join(path_to_imgs+"processed_images\\", '*.jpg')):
        number = float(filename.split("_")[-1].split(".")[0])
        print("file {}, number {}".format(filename, number))

        easy_results = reader.readtext(filename)

        # img = Image.open(filename)
        # tess_result = pytesseract.image_to_string(img, config='outputbase digits')
        print("Number read from easyocr: {}\n".format(easy_results))
