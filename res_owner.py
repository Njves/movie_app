import os
import uuid

from PIL import Image


class ResourceOwner:

    image_path = "image/image/"
    icon = "image/icon.png"

    def __generate_file_name(self):
        temp_uid = str(uuid.uuid1())
        split_uid = temp_uid.split("-")
        uid = split_uid[0] + split_uid[1]
        image_dir = self.image_path + uid + ".jpg"
        return image_dir

    def copy_image_to_dir(self, path) -> str:
        image_dir = self.__generate_file_name()
        with open(path, "rb") as read_file:
            file = read_file.read()
        with open(image_dir, "wb") as write_file:
            write_file.write(file)
        return image_dir

    def download_image(self, content):
        image_dir = self.__generate_file_name()
        with open(image_dir, "wb") as out:
            out.write(content)
        out.close()
        return image_dir

    def resizeImage(self):
        dirs = os.listdir(self.image_path)
        print(dirs)
        for i in dirs:
            orig = Image.open(self.image_path + i)
            resized = orig.resize((130, 300))
            resized.save(self.image_path + i.split(".")[0] + "_small.jpg")

    def get_images(self):
        dirs = os.listdir(self.image_path)
        small_images = []
        for i in dirs:
            if i.__contains__("_small"):
                small_images.append(i)
        return small_images