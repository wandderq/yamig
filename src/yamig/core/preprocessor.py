from PIL import Image
from pathlib import Path

import logging as lg
import numpy as np


class PreprocessorError(Exception):
    pass


class Preprocessor:
    def __init__(self, 
        input_path: Path,
        target_resolution: tuple[int,int],
        max_colors: int
    ):
        self.logger = lg.getLogger('amig')

        self.input_path = input_path
        self.target_resolution = target_resolution
        self.max_colors = max_colors


    def run(self) -> tuple[Image, np.array]:
        self.logger.info(f'loading image: {self.input_path}')
        img = Image.open(self.input_path).convert('RGB')
        
        self.logger.debug(f'original image resolution: {img.size}')
        
        self.logger.info(f'quanting palette to {self.max_colors} colors')
        img = img.quantize(
            colors=self.max_colors,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE
        ).convert('RGB')

        img_array = np.array(img, dtype=np.float16)
        palette = np.unique(img_array.reshape(-1, 3), axis=0)

        self.logger.debug(f'unique colors: {len(palette)}')

        self.logger.info(f'resizing image to the target resolution: {self.target_resolution}')
        img = img.resize(self.target_resolution, Image.Resampling.LANCZOS)

        return img, palette