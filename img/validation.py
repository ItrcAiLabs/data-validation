import json
from ImageFormatValidator.ImageFormatValidator import ImageFormatValidator
from configs.configFormatValidator import configFormatValidator
from utils import list_all_files


class validation:
    def __init__(self,) -> None:
        pass

    def level0(self) -> None:
        self.path_logger = configFormatValidator.get("path_logger")
        self.path_image_folder = configFormatValidator.get("path_image_folder")
        self.path_image_list = configFormatValidator.get("path_image_list")
        self.max_size_mb = configFormatValidator.get("max_size_mb")
        self.allowed_formats = configFormatValidator.get("allowed_formats")
        self.min_size_mb = configFormatValidator.get("min_size_mb")
        self.expected_dimensions_list = configFormatValidator.get("expected_dimensions_list")
        self.expected_mode = configFormatValidator.get("expected_mode")
        self.pixel_range = configFormatValidator.get("pixel_range")


        self.list_path_images = list_all_files(self.path_image_folder)

        with open(self.path_image_list, "r") as file:
            self.image_list = json.load(file)
        # for level_0
        ImageFormatValidator(self.path_logger, 
                self.list_path_images , 
                self.image_list, 
                self.max_size_mb, 
                self.allowed_formats,
                self.min_size_mb, 
                self.expected_dimensions_list,
                self.expected_mode,
                self.pixel_range)
        


model = validation()
model.level0()