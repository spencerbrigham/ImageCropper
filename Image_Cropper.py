import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import sys

def process_image(image_path, output_dir):
    try:
        # Open the image
        image = Image.open(image_path)
        width, height = image.size

        # Calculate the 16:9 aspect ratio size
        aspect_ratio = 16 / 9

        # Determine the maximum possible dimensions for the 16:9 ratio
        max_height = height
        max_width = max_height * aspect_ratio

        if max_width > width:
            max_width = width
            max_height = max_width / aspect_ratio

        # Crop from top-left corner
        left_box = (0, 0, int(max_width), int(max_height))
        left_crop = image.crop(left_box)

        # Crop from top-right corner
        right_box = (width - int(max_width), 0, width, int(max_height))
        right_crop = image.crop(right_box)

        # Resize images so that the long edge is 2560 pixels
        def resize_image(img):
            w, h = img.size
            if w >= h:
                new_w = 2560
                new_h = int(h * (2560 / w))
            else:
                new_h = 2560
                new_w = int(w * (2560 / h))
            return img.resize((int(new_w), int(new_h)), resample=Image.LANCZOS)

        left_resized = resize_image(left_crop)
        right_resized = resize_image(right_crop)

        # Save images as PNG for lossless quality
        left_output_path = os.path.join(output_dir, 'output_left.png')
        right_output_path = os.path.join(output_dir, 'output_right.png')

        left_resized.save(left_output_path, 'PNG')
        right_resized.save(right_output_path, 'PNG')

    except Exception as e:
        raise e

def main():
    root = tk.Tk()
    root.title('Image Cropper')

    def select_file():
        file_path = filedialog.askopenfilename(
            title='Select an Image File',
            filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp')]
        )
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

    def process():
        image_path = entry.get()
        if not image_path or not os.path.isfile(image_path):
            messagebox.showerror('Error', 'Please select a valid image file.')
            return
        try:
            # Set output_dir to the same directory as the input image
            output_dir = os.path.dirname(os.path.abspath(image_path))
            process_image(image_path, output_dir)
            messagebox.showinfo('Success', f'Images have been saved as "output_left.png" and "output_right.png" in {output_dir}.')
            entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

    # GUI Layout
    tk.Label(root, text='Select an Image File').pack(pady=5)
    frame = tk.Frame(root)
    frame.pack(pady=5)
    entry = tk.Entry(frame, width=60)
    entry.pack(side=tk.LEFT)
    tk.Button(frame, text='Browse', command=select_file).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text='Process', command=process).pack(pady=5)
    tk.Button(root, text='Exit', command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
