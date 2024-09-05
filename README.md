# Pygame ASCII Pixel Image Converter
Application made with Pygame to convert images and videos into ASCII or pixel art depending on the file selected.

## Installation

Run this command:
```
pip install -r requirements.txt
```
while in the directory folder.

NOTE: Python 3+ required.

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

## Example images

ASCII Greyscale:  
![ascii greyscale example image](https://github.com/user-attachments/assets/90d58d77-bf6d-4de4-8bd5-6006b0d32f06)  

ASCII Color:  
![ascii color example image](https://github.com/user-attachments/assets/97b05314-61d1-4605-ab89-591fc949efa0)

Pixel art wih color:  
![pixel art color example image](https://github.com/user-attachments/assets/5d121849-d867-45c6-b3ac-76a9df34d674)

Video ASCII Color:  
![video](https://github.com/user-attachments/assets/da5d1e4d-e35c-439b-9365-7efdecd8dc29) 
