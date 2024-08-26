import pygame as pg
import pygame.gfxdraw
import numpy as np
import cv2
from numba import njit
from tkinter import filedialog


class VideoConverter:
    def __init__(self) -> None:
        self.path = filedialog.askopenfilename()
        
        if not self.path or not self.path.endswith(('.mp4')):
            raise ValueError("Please select a valid file.")
        
        self.capture = cv2.VideoCapture(self.path)
        pg.init()
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.previous_frames = [] 
        self.record = False
        self.recorder = None #Will be initialized when the user presses 'r'

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

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

    def save_frame(self):
        # Save the Pygame surface directly to an image file
        pg.image.save(self.surface, filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]))

    def save_video(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        
        if not save_path:
            raise ValueError("No file selected for saving.")
        
        # Define the codec and create VideoWriter object
        capture_fps = self.capture.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), capture_fps, (self.WIDTH, self.HEIGHT))
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
            self.clock.tick(capture_fps)

        # Release everything if job is finished
        out.release()

    def pygame_surface_to_cv2_image(self, surface):
        # Convert the pygame surface to a NumPy array
        frame = pg.surfarray.array3d(surface)
        
        # Transpose the array to match OpenCV's format
        frame = np.transpose(frame, (1, 0, 2))
        
        # Convert the color format from RGB to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
        return frame
    
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
            self.clock.tick(60)