# Add custom watermarks / logos to images.

[Note from NW: This was written by the client.]

I am adding 10 images, 2 logos and 5 possible lines of text that I would like you to use as an example to demonstrate the scripts works.
Share the generated images.

#### function 1
```
def add_watermark(img, txt_prob = 0.2, txt, logo_folder):

if np.random.rand() < text:
   # randomly choose from possible text (txt)
   # randomly set location and size of text in image
   # randomly set opacity (has to be watermark!)
   # randomly set colour (80% probability grey, 5% red, 5% blue, 5% green, 5% yellow)
   # add to image
else:
   # randomly choose from possible images in folder (logo_folder)
   # randomly set location and size of watermark in image
   # randomly set colour (50% probability grey, 50% probability is orginical colour)
   # randomly set opacity (has to be watermark!). If colour is not grey, make more transparant
   # add to image

return img, xmin, xmax, ymin, ymax #coordinates of the corners of the text/watermark
```

#### function 2
```
def add_logo(img, logo_folder):

   # randomly choose from possible images in folder (logo_folder)
   # randomly set location and size of logo in image
   # set opacity to be non-transparant, not a watermark!
   # add to image
return img xmin, xmax, ymin, ymax #coordinates of the corners of the text/watermark
```

# folder structure
```
base_images = 'C:/folder_base'
watermark_images = 'C:/output_watermark'
logo_images =  'C:/output_logo'  # this folder just contains many .png files
logos = 'C:/input_logo'
watermark_coordinates = 'C:/coordinates_water.csv'
logo_coordinates = 'C:/coordinates_logo.csv'
txt = 'C:/possible_texts.txt'
```

# loop over all files in base_images:
```
   image = im.open()
   watermark, xmin_water, xmax_water, ymin_water, ymax_water = add_watermark(img, watermark, txt_prob, txt, logo_folder)
   logo, xmin_logo, xmax_logo, ymin_logo, ymax_logo = add_logo(img, logo_folder)

   im.save(watermark, watermark_images) # use nameof the original image+ '_watermark'
   im.savelogo, logo_images) # use nameof the original image+ '_logo'

   # write the coordinates to file for watermark. 5 columns: image_name, xmin, xmax, ymin, ymax
   # write the coordinates to file for logo. 5 columns: image_name, xmin, xmax, ymin, ymax

   print x% completed
```