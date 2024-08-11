import customtkinter as ctk
import tkinter
from tkinter import filedialog
import openai
from PIL import Image, ImageTk
import requests
import io

def generate():
    openai.api_key = '' #Insert your API key Here
    user_prompt = prompt_entry.get("0.0", tkinter.END)
    user_prompt += "in style: " + style_dropdown.get()

    response = openai.Image.create(
        prompt=user_prompt,
        n=int(number_slider.get()),
        size="512x512"
    )

    global image_urls
    image_urls = []
    for i in range(len(response['data'])):
        image_urls.append(response['data'][i]['url'])

    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)

    def update_image(index=0):
        canvas.image = images[index]
        canvas.create_image(0, 0, anchor="nw", image=images[index])
        index = (index + 1) % len(images)
        canvas.after(3000, update_image, index)

    update_image()

def save_image():
    if hasattr(canvas, "image") and image_urls:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                        ("JPEG files", "*.jpg;*.jpeg"),
                                                                                        ("All files", "*.*")])
        if file_path:
            file_format = file_path.split('.')[-1].upper()
            response = requests.get(image_urls[0])
            img = Image.open(io.BytesIO(response.content))
            img.save(file_path, format=file_format)
root = ctk.CTk()
root.title("LuminusCraft")
ctk.set_appearance_mode("dark")
input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(input_frame, text=" Enter Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(input_frame, text="Images")
number_label.grid(row=2, column=0)
number_slider = ctk.CTkSlider(input_frame, from_=1, to=10, number_of_steps=9, button_color='#7f5a9f')
number_slider.grid(row=2, column=1)

generate_button = ctk.CTkButton(input_frame, text="Generate Image", command=generate, hover_color='#6a4b84', fg_color='#49335b')
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

save_button = ctk.CTkButton(input_frame, text="Save Image", command=save_image, hover_color='#6a4b84', fg_color='#49335b')
save_button.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)

progressbar = ctk.CTkProgressBar(input_frame, orientation="horizontal")

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="right")

root.mainloop()
