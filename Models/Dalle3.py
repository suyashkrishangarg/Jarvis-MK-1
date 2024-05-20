#pip install --upgrade BingImageCreator
from os import system, listdir
import matplotlib.pyplot as plt
import PIL
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import Bing_key


C = Bing_key
output_path = r'Downloads\images'

def Dalle3(prompt: str):
    output_dir = "Downloads\\images"
    system(f'python -m BingImageCreator --prompt "{prompt}" -U "{C}" --output-dir "{output_dir}"')
    return listdir(output_path)[-4:]

class Show_Image:
    def __init__(self, li: list) -> None:
        self.listd = li
        self.current_index = 0

    def open(self):
        try:
            img_path = f"{output_path}\\{self.listd[self.current_index]}"
            img = plt.imread(img_path)
            plt.imshow(img)
            plt.show(block=False)
        except IndexError:
            print("No more images to show.")
        except PIL.UnidentifiedImageError:
            print(f"Corrupted image: {img_path}. Skipping...")
            self.show_next()

    def close(self):
        plt.close()

    def show_next(self):
        try:
            self.close()
            self.current_index += 1
            if self.current_index < len(self.listd):
                self.open()
            else:
                print("No more images to show.")
        except IndexError:
            print("No more images to show.")


print(f"==> Dalle3 Loaded!")

if __name__ == "__main__":
    prompt = "youtube play button"  # Modify the prompt as needed
    images_list = Dalle3(prompt)
    show_image_instance = Show_Image(images_list)

    while True:
        # user_input = speechrecognition()
        user_input = input("suuu: ")

        if user_input == 'show':
            show_image_instance.open()
            plt.pause(0.01)  # Add a small pause to handle input events
        elif user_input == 'next':
            show_image_instance.show_next()
            plt.pause(0.01)  # Add a small pause to handle input events
        elif user_input == 'exit':
            break
        else:
            print("Invalid input. Please enter 'show', 'next', or 'exit'.")
    sys.exit()