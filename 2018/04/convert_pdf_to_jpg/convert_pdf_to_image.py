from PIL import Image
from pdf2image import convert_from_path
import os
import wand

path_to_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.pdf')
pages = convert_from_path('test.pdf', 500)
# for page in pages:
#     page.save('out.jpg', 'JPEG')
