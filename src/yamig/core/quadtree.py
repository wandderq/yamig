import logging as lg
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
import numpy as np

class QuadtreeProcessor:
    def __init__(self,
        image: Image,
        min_region_size: int,
        dispersion_threshold: int,
        palette: np.array
    ):
        self.logger = lg.getLogger('amig.quadtree')
        self.image_array = np.array(image, dtype=np.float16)
        self.min_region_size = min_region_size
        self.dispersion_threshold = dispersion_threshold

        self.palette = palette
        self.color_tree = cKDTree(palette)


    def decompose(self, x: int, y: int, w: int, h: int) -> list:
        # self.logger.debug(f'processing region: ({x};{y}) {w}x{h}')

        region = self.image_array[y:y+h, x:x+w]
        region_mean_color = np.mean(region, axis=(0, 1))
        region_color_diff = region.astype(np.float16) - region_mean_color.astype(np.float16)
        region_dispersion = np.mean(np.sum(region_color_diff**2, axis=2))
        
        rects = []

        if (w <= self.min_region_size
            or h <= self.min_region_size
            or region_dispersion <= self.dispersion_threshold
        ):
            _, idx = self.color_tree.query(region_mean_color)
            rect_color = tuple(self.palette[idx])
            rects.append((x, y, w, h, rect_color))
        
        else:
            half_w = w // 2
            half_h = h // 2
            rects.extend(self.decompose(x, y, half_w, half_h))
            rects.extend(self.decompose(x + half_w, y, w - half_w, half_h))
            rects.extend(self.decompose(x, y + half_h, half_w, h - half_h))
            rects.extend(self.decompose(x + half_w, y + half_h, w - half_w, h - half_h))
        
        return rects
    
    
    def rects2int(self, rects: list) -> list:
        return [
            (r[0], r[1], r[2], r[3], tuple(int(c) for c in r[4]))
            for r in rects
        ]
    

    def recompose(self, target_resolution: tuple[int,int], rects: list) -> Image:
        self.logger.debug('recomposing image from rects')
        image = Image.new('RGB', target_resolution, (0, 0, 0))
        draw = ImageDraw.Draw(image)

        for rect in rects:
            x, y, w, h, color = rect
            
            x2 = x + w
            y2 = y + h
            
            draw.rectangle([x, y, x2, y2], fill=color)
        
        return image