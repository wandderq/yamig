import logging as lg
import copy

class MlogGenerator:
    def __init__(self, max_script_length: int, display_name: str, target_resolution: tuple[int, int]):
        self.logger = lg.getLogger('amig.mlog-generator')
        self.max_script_length = max_script_length
        self.display_name = display_name
        self.target_resolution = target_resolution
    

    def generate_mlog(self, rects: list):
        rects = self.flip_coords(rects)
        color2rects = self.sort_rects_by_color(rects)
        big_script = self.generate_big_script(color2rects)
        scripts = self.split_big_script(big_script)

        return scripts
    

    def flip_coords(self, rects: list) -> list:
        flipped_rects = []

        for rect in rects:
            x, y, w, h, color = rect

            flipped_rect = [x, self.target_resolution[1]-y-h, w, h, color]
            flipped_rects.append(flipped_rect)

        return flipped_rects
    

    def sort_rects_by_color(self, rects: list) -> dict[tuple, list]:
        self.logger.debug('sorting rects by color')
        color2rects = {}

        for rect in rects:
            color = rect[4]

            if color not in color2rects:
                color2rects[color] = []
            
            color2rects[color].append(rect[:4])
        
        self.logger.debug(f'total rect colors: {len(color2rects)}')
        return color2rects
    

    def generate_big_script(self, color2rects: dict):
        self.logger.debug('generating big script')
        script = []

        for color, rects in color2rects.items():
            script.append(f'draw color {color[0]} {color[1]} {color[2]} 255')
            script.extend([
                f'draw rect {r[0]} {r[1]} {r[2]} {r[3]}'
                for r in rects
            ])
        
        self.logger.debug(f'big script length: {len(script)}')
        
        return script
    

    def split_big_script(self, big_script: str) -> list[str]:
        scripts = []
        script = []

        current_color = None

        for line_i, line in enumerate(big_script, start=1):
            if line.startswith('draw color'):
                self.logger.debug(f'current color={line}')
                current_color = line
                
                if line_i != 1:
                    script.append(f'drawflush {self.display_name}')
                script.append(line)
                continue

            if len(script) % (self.max_script_length-1) == 0:
                script.append(f'drawflush {self.display_name}')
                self.logger.debug(f'adding script part len={len(script)}')
                scripts.append(copy.deepcopy(script))
                script = [current_color]
                continue

            script.append(line)
        
        self.logger.debug(f'adding script part len={len(script)}')
        script.append(f'drawflush {self.display_name}')
        scripts.append(copy.deepcopy(script))

        return scripts
