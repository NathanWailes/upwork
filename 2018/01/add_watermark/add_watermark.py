import csv
import os
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    exit("This script requires the PIL module.\nInstall with pip install Pillow")
import random
import ntpath


def add_watermarks_and_logos(path_to_folder_of_images_to_be_watermarked, path_to_folder_to_output_marked_images_to, path_to_folder_to_output_logoed_images_to):
    # randomly choose from possible images in folder (logo_folder)
    filenames_of_images_to_add_watermarks_and_logos_to = os.listdir(path_to_folder_of_images_to_be_watermarked)

    for filename in filenames_of_images_to_add_watermarks_and_logos_to:
        path_to_original_image = path_to_folder_of_images_to_be_watermarked + '/' + filename

        watermark, xmin_water, xmax_water, ymin_water, ymax_water = add_watermark(path_to_original_image,
                      path_to_file_containing_text_to_use_as_watermarks,
                      path_to_folder_of_images_to_use_as_watermarks, probability_of_text_watermark=0.2)
        output_image(watermark, path_to_original_image, path_to_folder_to_output_marked_images_to, "_watermark")

        # write the coordinates to file for watermark. 5 columns: image_name, xmin, xmax, ymin, ymax
        log_output_path = 'output_with_watermarks.csv'
        output_to_log(log_output_path, filename, xmin_water, xmax_water, ymin_water, ymax_water)

        image_with_logo, xmin_water, xmax_water, ymin_water, ymax_water = add_logo(path_to_original_image,
                                                                                   path_to_folder_of_images_to_use_as_watermarks)
        output_image(image_with_logo, path_to_original_image, path_to_folder_to_output_logoed_images_to, "_logo")

        # write the coordinates to file for logo. 5 columns: image_name, xmin, xmax, ymin, ymax
        log_output_path = 'output_with_logos.csv'
        output_to_log(log_output_path, filename, xmin_water, xmax_water, ymin_water, ymax_water)

    print("Done")


def add_watermark(path_to_image_file, path_to_file_containing_text_to_use_as_watermarks,
                  path_to_folder_of_images_to_use_as_watermarks, probability_of_text_watermark=0.2):
    image = Image.open(path_to_image_file).convert('RGBA')
    base_image_width, base_image_height = image.size

    if random.random() <= probability_of_text_watermark:
        # randomly choose from possible text (txt)
        with open(path_to_file_containing_text_to_use_as_watermarks) as file:
            text_options = [line.strip() for line in file.readlines()]
        text_to_use = random.choice(text_options)

        # randomly set size of text in image
        font_size = int(random.uniform(base_image_height/20, base_image_height/5))  # TODO: Make this random.
        font = ImageFont.truetype('arial.ttf', font_size)

        image_watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image_watermark)

        margin = 10

        # randomly set location of text in image
        watermark_width, watermark_height = draw.textsize(text_to_use, font)
        top_left_corner_x = random.uniform(margin, base_image_width - watermark_width - margin)
        top_left_corner_y = random.uniform(margin, base_image_height - watermark_height - margin)

        # randomly set colour (80% probability grey, 5% red, 5% green, 5% blue, 5% yellow)
        if random.random() <= 0.8:
            color = (0, 0, 0, 255)  # grey
        elif random.random() <= 0.25:
            color = (255, 0, 0, 255)  # red
        elif random.random() <= 0.33:
            color = (0, 255, 0, 255)  # green
        elif random.random() <= 0.5:
            color = (0, 0, 255, 255)  # blue
        else:
            color = (255, 255, 0, 255)  # yellow

        draw.text((top_left_corner_x, top_left_corner_y), text_to_use, color, font)

        # randomly set opacity (has to be watermark!)
        opacity = random.uniform(0.1, 0.3)
        image_watermark = reduce_opacity_to_x(image_watermark, opacity)

        # add to image
        image = Image.alpha_composite(image, image_watermark)

    else:
        # randomly choose from possible images in folder (logo_folder)
        filenames_of_possible_watermark_images = os.listdir(path_to_folder_of_images_to_use_as_watermarks)
        while True:
            filename_of_image_to_use_as_a_watermark = random.choice(filenames_of_possible_watermark_images)

            # This is just the logo, smaller than the base image
            try:
                image_watermark_without_container = Image.open(path_to_folder_of_images_to_use_as_watermarks + '/' +
                                                               filename_of_image_to_use_as_a_watermark).convert('RGBA')
                break
            except:
                continue

        # This is a transparent layer the same size as the base image.  We're going to use this to have the logo show
        # up in a random location.
        watermark_container = Image.new('RGBA', image.size, (0, 0, 0, 0))

        # randomly set size of watermark in image
        max_width = random.randrange(base_image_width / 20, base_image_width / 4)
        image_watermark_without_container.thumbnail((max_width, max_width))

        margin = 10

        # randomly set location of watermark in image
        watermark_width, watermark_height = image_watermark_without_container.size
        top_left_corner_x = int(random.uniform(margin, base_image_width - watermark_width - margin))
        top_left_corner_y = int(random.uniform(margin, base_image_height - watermark_height - margin))

        # Here we create the layer that is both 1) the same size as the base image, and 2) has the watermark.
        watermark_container.paste(image_watermark_without_container, box=(top_left_corner_x, top_left_corner_y), mask=None)

        # randomly set colour (50% probability grey, 50% probability is original colour)
        is_grey = False
        if random.random() <= 0.5:
            is_grey = True
            converter = ImageEnhance.Color(watermark_container)
            watermark_container = converter.enhance(0)

        # randomly set opacity (has to be watermark!). If colour is not grey, make more transparent
        if is_grey:
            opacity = random.uniform(0.1, 0.3)
        else:
            opacity = random.uniform(0.1, 0.15)
        watermark_container = reduce_opacity_to_x(watermark_container, opacity)

        # add to image
        image = Image.alpha_composite(image, watermark_container)

    # return image and coordinates of the corners of the text/watermark
    return image, top_left_corner_x, top_left_corner_x + watermark_width, base_image_height - top_left_corner_y - watermark_height, base_image_height - top_left_corner_y


def add_logo(path_to_image_file, path_to_folder_of_images_to_use_as_watermarks):
    image = Image.open(path_to_image_file).convert('RGBA')
    base_image_width, base_image_height = image.size

    # randomly choose from possible images in folder (logo_folder)
    filenames_of_possible_watermark_images = os.listdir(path_to_folder_of_images_to_use_as_watermarks)

    while True:
        filename_of_image_to_use_as_a_watermark = random.choice(filenames_of_possible_watermark_images)

        try:
            # This is just the logo, smaller than the base image
            image_watermark_without_container = Image.open(path_to_folder_of_images_to_use_as_watermarks + '/' +
                                                           filename_of_image_to_use_as_a_watermark).convert('RGBA')
            break
        except:
            continue

    # This is a transparent layer the same size as the base image.  We're going to use this to have the logo show
    # up in a random location.
    watermark_container = Image.new('RGBA', image.size, (0, 0, 0, 0))

    # randomly set size of watermark in image
    max_width = random.randrange(base_image_width / 20, base_image_width / 4)
    image_watermark_without_container.thumbnail((max_width, max_width))

    margin = 10

    # randomly set location of watermark in image
    watermark_width, watermark_height = image_watermark_without_container.size
    top_left_corner_x = int(random.uniform(margin, base_image_width - watermark_width - margin))
    top_left_corner_y = int(random.uniform(margin, base_image_height - watermark_height - margin))

    # Here we create the layer that is both 1) the same size as the base image, and 2) has the watermark.
    watermark_container.paste(image_watermark_without_container, box=(top_left_corner_x, top_left_corner_y), mask=None)

    # set opacity to be non-transparent, not a watermark!
    if False:  # <-- The code in this block will never execute.
        opacity = random.uniform(0.1, 0.2)
        watermark_container = reduce_opacity_to_x(watermark_container, opacity)

    # add to image
    image = Image.alpha_composite(image, watermark_container)

    # return image and coordinates of the corners of the text/watermark
    return image, top_left_corner_x, top_left_corner_x + watermark_width, base_image_height - top_left_corner_y - watermark_height, base_image_height - top_left_corner_y


def reduce_opacity_to_x(image, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    else:
        image = image.copy()
    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    image.putalpha(alpha)
    return image


def output_image(image, path_to_image_file, path_to_folder_to_output_marked_images_to, filename_suffix):
    """

    :param image:
    :param path_to_image_file:
    :param path_to_folder_to_output_marked_images_to:
    :param filename_suffix: For example, "_watermark" or "_logo"
    :return:
    """
    original_filename = ntpath.basename(path_to_image_file)
    if not os.path.exists(path_to_folder_to_output_marked_images_to):
        os.makedirs(path_to_folder_to_output_marked_images_to)

    filename_without_extension = os.path.splitext(original_filename)[0]
    extension = os.path.splitext(original_filename)[1]

    filename_with_suffix_and_extension = filename_without_extension + filename_suffix + extension

    image.convert('RGB').save(path_to_folder_to_output_marked_images_to + "/" + filename_with_suffix_and_extension)


def output_to_log(output_path, marked_image_name, xmin_water, xmax_water, ymin_water, ymax_water):
    if not os.path.exists(output_path):
        need_to_write_headers = True
    else:
        need_to_write_headers = False

    with open(output_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if need_to_write_headers:
            fieldnames = ['image_name', 'xmin', 'xmax', 'ymin', 'ymax']
            writer.writerow(fieldnames)

        writer.writerow([marked_image_name, int(xmin_water), int(xmax_water), int(ymin_water), int(ymax_water)])


if __name__ == '__main__':
    """
    base_images = 'C:/folder_base'
    watermark_images = 'C:/output_watermark'
    logo_images =  'C:/output_logo'  # this folder just contains many .png files
    logos = 'C:/input_logo'
    watermark_coordinates = 'C:/coordinates_water.csv'
    logo_coordinates = 'C:/coordinates_logo.csv'
    txt = 'C:/possible_texts.txt'
    """
    path_to_folder_of_images_to_be_watermarked = './base_images/'
    path_to_folder_of_images_to_use_as_watermarks = './logo/'
    path_to_file_containing_text_to_use_as_watermarks = './possible_text.txt'
    path_to_folder_to_output_marked_images_to = './output_watermark'
    path_to_folder_to_output_logoed_images_to = './output_logo'

    add_watermarks_and_logos(path_to_folder_of_images_to_be_watermarked, path_to_folder_to_output_marked_images_to, path_to_folder_to_output_logoed_images_to)