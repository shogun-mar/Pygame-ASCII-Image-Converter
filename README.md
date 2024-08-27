# Pygame ASCII Pixel Image Converter
Application made with Pygame to convert images and videos into ASCII or pixel art depending on the file selected.

## Installation

```
pip install pygame opencv-python numba numpy tkinter
```

## Usage

In the folder named `images converters` you can find the files to convert images to:

* Colored ASCII art using `ascii color.py`
* Black and white ASCII art using `ascii greyscale.py`
* Colored pixel art using `pixel art color.py`
  
In all converters it's possible to select the input image and save the output image through file explorer (The supported file extensions are png, jpg and jpeg).

In the folder named `video converters` you can find the files to convert video to:

* Colored ASCII art using `ascii color.py`
* Black and white ASCII art using `ascii greyscale.py`
* Colored pixel art using `pixel art color.py`

In all converters it's possibile to select the input video and select the output path through file explorer.
The files `image_converter.py` and `video_converter.py` are made purely for organization reasons, they are not functional in any way.

`IMPORTANT`: When saving an entire video it's necessary to let the video play out until the end before trying to access the newly created file.

## Settings

By modifying the `font_size` value in the init method of ASCII converters you can increase or decrease the font size of the ouput.
By modifying the `pixel_size` value in the init method of pixel art converters you can increase or decrease the pixel size of the ouput.
By modifying the `color_lvl` value in the init method of color converter you can increase or decrease the numbers of colors in the palette (default value 8 will produce 512 colors &rarr; formula:  $x^3$ because of the three color channels).
 
## Controls 

While converting images:

* S &rarr; Save the converted image to the desired path.

While converting video:

* S &rarr; Save the current frame to the desired path.
* V &rarr; Save the video to desired path.
* R &rarr; Start recording, file explorer will open prompting you to choose a file path.
* ESCAPE &rarr; Stop recording and save video file to previously declared path.





