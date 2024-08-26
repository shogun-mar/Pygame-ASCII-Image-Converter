import pygame as pg
import pygame.gfxdraw
import numpy as np
import cv2
from numba import njit
from tkinter import filedialog

@njit
def accelerate_conversion(image, width, height, color_coeff, step):
    array_of_values = []
    for x in range(0, width, step):
        for y in range(0, height, step):
            color = image[x, y] // color_coeff
            if sum(color):
                array_of_values.append((color, (x, y)))
    return array_of_values

class Converter:
    def __init__(self, color_lvl = 8, pixel_size = 8):
        self.path = filedialog.askopenfilename()
        
        if not self.path or not self.path.endswith(('.mp4')):
            raise ValueError("Please select a valid file.")
        
        self.capture = cv2.VideoCapture(self.path)
        pg.init()
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.PIXEL_SIZE = pixel_size
        self.surface = pg.display.set_mode(self.RES)
        pg.display.set_caption(f"ASCII Color Converter - {self.path}")
        self.clock = pg.time.Clock()
        self.COLOR_LVL = color_lvl
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

        self.rec_fps = 25#self.capture.get(cv2.CAP_PROP_FPS)
        self.record = False
        self.recorder = cv2.VideoWriter("output/video/video.mp4", cv2.VideoWriter_fourcc("mp4v"), self.rec_fps, (self.WIDTH, self.HEIGHT))

    def draw_converted_image(self):
        self.image = self.get_image()
        array_of_values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.COLOR_COEFF, self.PIXEL_SIZE)
        for color_key, (x, y) in array_of_values:
            color = self.PALETTE[color_key]
            pg.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True) # Create a list with all the possible RGB values
        color_palette = np.array([[r, g, b] for r in colors for g in colors for b in colors]) # Create a 3D array with all the possible RGB values
        palette = {}
        color_coeff = int(color_coeff) # Get the color coefficient
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color

        return palette, color_coeff

    def get_image(self):
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_img = cv2.transpose(self.cv2_image)
        color_image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        return color_image
    
    def draw_cv2_image(self): # Resize the cv2 image so it fits the screen
        resized_cv2_image = cv2.resize(self.cv2_image, (480, 720), interpolation = cv2.INTER_AREA)
        cv2.imshow("img", resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_video(self):
        return # Disable saving for now
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        
        if not save_path:
            raise ValueError("No file selected for saving.")
        
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
        out = cv2.VideoWriter(save_path, fourcc, 20.0, (self.WIDTH, self.HEIGHT))

        # Capture frames and write to video file
        for _ in range(100):  # Capture 100 frames as an example
            self.draw()
            pg.display.flip()
            frame = pg.surfarray.array3d(self.surface)
            frame = cv2.transpose(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            self.clock.tick(20)  # 20 FPS

        # Release everything if job is finished
        out.release()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    self.save_video()
            
            self.draw()
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    Converter().run()