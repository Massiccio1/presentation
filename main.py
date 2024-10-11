import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import itertools
import random

class ImageCarouselApp:
    def __init__(self, master,controller, col=4, row=2):
        self.master = master
        self.controller = controller
        self.image_folder = self.choose_folder()
        self.image_files = self.get_image_files()
        # print(self.image_files)
        random.shuffle(self.image_files)
        self.current_images = itertools.cycle(self.image_files)
        
        self.minspeed_val=3000
        self.rangespeed_val=4000
        
        self.view_count=0
        
        self.row=row
        self.col=col
        self.zoom_val=1
        
        self.img_size=int(200*self.zoom_val)

        self.start()
        
    def start(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.image_widgets = []
        self.create_widgets()
        self.update_images()
        self.create_controller()

    def get_image_files(self):
        return self.rec_find_images(self.image_folder, [])

    def rec_find_images(self, image_folder, masterlist):
        # masterlist = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(".png") or file.endswith(".jpg")]
        files = os.listdir(image_folder)
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".PNG") or file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".gif"):
                masterlist.append(os.path.join(image_folder, file))
            elif os.path.isdir(os.path.join(image_folder, file)):
                self.rec_find_images(os.path.join(image_folder, file), masterlist)
        return masterlist

    def print_values(self):
        try:
            self.row=int(self.row_scale.get())
            self.col=int(self.col_scale.get())
            self.zoom_val=self.zoom.get()
            self.img_size=int(200*self.zoom_val)
            self.minspeed_val = int(self.minspeed.get())
            self.rangespeed_val = int(self.rangespeed.get())
            print("minspeed:", self.minspeed_val)
            print("speedrange:", self.rangespeed_val)
            self.start()
        except:
            pass
        
    def get_random_timeout(self):
        return int(random.randrange(self.minspeed_val, (self.minspeed_val+self.rangespeed_val), 1))
    
    def create_widgets(self):
        
       
        count = 0
        for i in range(self.col* self.row):
            image_widget = tk.Label(self.master, borderwidth=2, relief="groove")
            image_widget.grid(row=i // self.col, column=i % self.col, padx=5, pady=5)
            self.image_widgets.append(image_widget)
            count +=1
        
    def create_controller(self):
                    
        count = 0
        self.minspeed = tk.Scale(self.controller, from_=1, to=10000, orient=tk.HORIZONTAL,label = "min speed")
        self.minspeed.set(self.minspeed_val)
        self.minspeed.grid(row=count, column=0, padx=5, pady=5)

        self.rangespeed = tk.Scale(self.controller, label = "range", from_=1, to=10000, orient=tk.HORIZONTAL)
        self.rangespeed.set(self.rangespeed_val)
        self.rangespeed.grid(row=count+1, column=0)
        

        self.zoom = tk.Scale(self.controller, label = "zoom", from_=0.1, to=4.0, resolution = 0.01 , digits = 3,orient=tk.HORIZONTAL)
        self.zoom.set(self.zoom_val)
        self.zoom.grid(row=count, column=1)
        
        self.row_scale = tk.Scale(self.controller, label = "rows", from_=1, to=10,orient=tk.HORIZONTAL)
        self.row_scale.set(self.row)
        self.row_scale.grid(row=count, column=2)
        
        self.col_scale = tk.Scale(self.controller, label = "cols", from_=1, to=10,orient=tk.HORIZONTAL)
        self.col_scale.set(self.col)
        self.col_scale.grid(row=count+1, column=2)

        self.print_values_button = tk.Button(self.controller, text="Confirm", command=self.print_values)
        self.print_values_button.grid(row=count+1, column=3, columnspan=2, padx=5, pady=5)    

    
    def choose_folder(self):
        return filedialog.askdirectory()

    def update_single_image(self, idx, viewcount=0):
        # print("updating ", idx)
        if viewcount!=self.view_count:
            return
        image_path = next(self.current_images)
        image = Image.open(image_path)
        image = image.resize((self.img_size, self.img_size))
        photo = ImageTk.PhotoImage(image)
        self.image_widgets[idx].configure(image=photo)
        self.image_widgets[idx].image = photo
        self.master.after(self.get_random_timeout(), lambda idx=idx, vc=self.view_count: self.update_single_image(idx, vc))
    
    def update_images(self):
        self.view_count+=1
        for i, wiget in enumerate(self.image_widgets):
            image_path = next(self.current_images)
            image = Image.open(image_path)
            image = image.resize((self.img_size, self.img_size))
            photo = ImageTk.PhotoImage(image)
            self.image_widgets[i].configure(image=photo)
            self.image_widgets[i].image = photo

            # Schedule the next update for this image
            self.master.after(self.get_random_timeout(), lambda idx=i, vc=self.view_count: self.update_single_image(idx, vc))
        


def main():
    root = tk.Tk()
    root.title("Image Carousel")
    controller = tk.Tk()
    controller.title("Carousel controller")

    app = ImageCarouselApp(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
