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
            r, g, b = image[x, y] // color_coeff
            if r + g + b:
                array_of_values.append(((r, g, b), (x, y)))

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

        self.previous_frames = [] 
        self.record = False
        self.recorder = None #Will be initialized when the user presses 'r'

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.transpose(frame)

    def record_frame(self):
        if self.record:
            
            if not self.recorder: 
                path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
                self.recorder = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), self.capture.get(cv2.CAP_PROP_FPS), (self.WIDTH, self.HEIGHT))
                                                # path, codec, fps, resolution

            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow("Recording", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record = False
                self.recorder = None
                cv2.destroyAllWindows()

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
        resized_cv2_image = self.cv2_image
        #resized_cv2_image = cv2.resize(self.cv2_image, (480, 720), interpolation = cv2.INTER_AREA)
        cv2.imshow("Original selected video", resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_frame(self):
        # Save the Pygame surface directly to an image file
        pg.image.save(self.surface, filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]))

    def pygame_surface_to_cv2_image(self, surface):
        # Convert the pygame surface to a NumPy array
        frame = pg.surfarray.array3d(surface)
        
        # Transpose the array to match OpenCV's format
        frame = np.transpose(frame, (1, 0, 2))
        
        # Convert the color format from RGB to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
        return frame

    def save_video(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        
        if not save_path:
            raise ValueError("No file selected for saving.")
        
        # Define the codec and create VideoWriter object
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), self.capture.get(cv2.CAP_PROP_FPS), (self.WIDTH, self.HEIGHT))
        # path, codec, fps, resolution

        for frame in self.previous_frames:
            frame = self.pygame_surface_to_cv2_image(frame)
            out.write(frame)

        num_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        remaining_frames = num_frames - len(self.previous_frames)

        for _ in range(remaining_frames):
            self.draw()
            pg.display.flip()
            frame = self.pygame_surface_to_cv2_image(self.surface)
            out.write(frame)
            self.clock.tick(20)  # 20 FPS

        # Release everything if job is finished
        out.release()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    self.capture.release()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.save_frame()
                    elif event.key == pg.K_v:
                        self.save_video()
                    elif event.key == pg.K_r:
                        self.record = not self.record
            
            self.record_frame()
            self.draw()
            self.previous_frames.append(self.surface.copy())
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    Converter().run()