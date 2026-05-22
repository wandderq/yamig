from argparse import ArgumentParser
from pathlib import Path
from colorlog import ColoredFormatter

from yamig.core.mlog import MlogGenerator
from yamig.core.preprocessor import Preprocessor
from yamig.core.quadtree import QuadtreeProcessor
from yamig.core.schema import SchemaGenerator

import logging as lg
import json
import sys
import os


class yamigcli:
    def __init__(self):
        self.argparser = self._init_argparser()
    

    def _init_argparser(self) -> ArgumentParser:
        argparser = ArgumentParser(
            description='yet another mindustry image generator'
        )

        argparser.add_argument(
            'input_path',
            type=Path,
            help='input image filepath'
        )

        argparser.add_argument(
            '-o', '--output-path',
            type=Path,
            default=None,
            help='output directory (default: derived from input_path)'
        )

        argparser.add_argument(
            '-r', '--target-resolution',
            default='320x192',
            type=str,
            help='target resolution (default: 320x192)'
        )

        argparser.add_argument(
            '-c', '--max-colors',
            default=64,
            type=int,
            help='max colors in the target image (default: 64) (may be inaccurate, +-15%% after quadtree)'
        )

        argparser.add_argument(
            '-R', '--min-region-size',
            default=8,
            type=int,
            help='minimal quadtree region size (px) (default: 8)'
        )

        argparser.add_argument(
            '-t', '--dispersion-threshold',
            type=int,
            default=600,
            help='quadtree color dispersion threshold (default: 600)'
        )

        argparser.add_argument(
            '-l', '--max-script-length',
            default=1000,
            type=int,
            help='max lines of script in each processor (default: 1000)'
        )

        argparser.add_argument(
            '-d', '--display-name',
            type=str,
            default='display1',
            help='display to draw to (default: display1)'
        )

        argparser.add_argument(
            '-N', '--schema-name',
            type=str,
            default=None,
            help='output schematic name (default: derived from other args)'
        )

        argparser.add_argument(
            '-D', '--schema-description',
            type=str,
            default=None,
            help='output schematic description (default: None)'
        )

        argparser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='debug logs'
        )

        return argparser
    

    def _setup_logger(self, verbose: bool, log_file_path: Path) -> lg.Logger:
        stream_handler = lg.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(
            ColoredFormatter(
                fmt="{log_color}{levelname}{reset}:{name} {message}",
                style='{',
                log_colors={
                    'DEBUG': 'blue',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red'
                }
            )
        )
        stream_handler.setLevel(lg.DEBUG if verbose else lg.INFO)

        file_handler = lg.FileHandler(
            filename=log_file_path,
            mode='w',
            encoding='utf-8'
        )
        file_handler.setFormatter(
            lg.Formatter(
                fmt="{asctime} {name} {levelname}: {message}",
                style='{',
                datefmt="%Y.%m.%d-%H:%M:%S"
            )
        )
        file_handler.setLevel(lg.DEBUG)

        root_logger = lg.getLogger()
        root_logger.setLevel(lg.DEBUG)
        
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)
        
        return lg.getLogger('amig.cli')
    

    def _parse_output_path(self, input_path: Path, output_path: Path | None) -> Path:
        if output_path is None:
            output_name = f'{input_path.stem}_output'
            output_path = Path(output_name).absolute()
        
        else:
            output_path = output_path.absolute()
        
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path
    

    def _parse_input_path(self, input_path: Path) -> Path:
        if not input_path.exists() or not input_path.is_file():
            raise FileNotFoundError(f'Input file \'{str(input_path)}\' not found!')
        
        return input_path.absolute()
    

    def _parse_target_resolution(self, target_resolution: str) -> tuple[int,int]:
        target_resolution_parts = target_resolution.strip().lower().split('x')
        if len(target_resolution_parts) != 2 or not all(part.isdigit() for part in target_resolution_parts):
            raise ValueError(f'Invalid resolution format: {target_resolution}')
        
        orig_width = int(target_resolution_parts[0])
        orig_height = int(target_resolution_parts[1])
        
        width = (orig_width + 16) // 32 * 32
        height = (orig_height + 16) // 32 * 32

        if orig_width != width or orig_height != height:
            self.logger.warning(f'target resolution was rounded to the nearest dividable by 32 value: {width}x{height}')
        
        return (width, height)
    
    
    def _parse_max_colors(self, max_colors: int) -> int:
        if max_colors < 2:
            raise ValueError(
                'Number of max colors must be at least 2, '
                f'got {max_colors}'
            )
        
        if max_colors > 256:
            raise ValueError(
                'Number of max colors can\'t be higher than 256, '
                f'got {max_colors}'
            )
        
        return max_colors


    def _parse_min_region_size(self, min_region_size: int) -> int:
        if min_region_size < 1:
            raise ValueError(
                'Minimal region size value must be at least 1, '
                f'got {min_region_size}'
            )
        
        return min_region_size
    

    def _parse_dispersion_threshold(self, dispersion_threshold: int) -> int:
        if dispersion_threshold < 1:
            raise ValueError(
                'Quadtree color dispersion threshold value must be at least 1, '
                f'got {dispersion_threshold}'
            )
        
        return dispersion_threshold
    

    def _parse_max_script_length(self, max_script_length: int) -> int:
        if max_script_length < 1:
            raise ValueError(
                'Max script length value must be at least 1, '
                f'got {max_script_length}'
            )
        
        if max_script_length > 1000:
            raise ValueError(
                'Max script length value can\'t be higher than 1000, '
                f'got {max_script_length}'
            )
        
        return max_script_length


    def _parse_schema_name(self, input_path: Path, schema_name: str | None, target_resolution: str) -> str:
        if schema_name is None:
            schema_name = f'{input_path.stem} picture {target_resolution}'
        
        return schema_name
        


    def run_cli(self) -> None:
        args = self.argparser.parse_args()

        # parsing args
        args.input_path = self._parse_input_path(args.input_path)
        args.output_path = self._parse_output_path(args.input_path, args.output_path)

        # setting up logger
        self.logger = self._setup_logger(
            args.verbose,
            args.output_path / 'amig.log'
        )

        # keep going but with logger
        args.target_resolution = self._parse_target_resolution(args.target_resolution)
        args.max_colors = self._parse_max_colors(args.max_colors)
        args.min_region_size = self._parse_min_region_size(args.min_region_size)
        args.dispersion_threshold = self._parse_dispersion_threshold(args.dispersion_threshold)
        args.max_script_length = self._parse_max_script_length(args.max_script_length)
        args.schema_name = self._parse_schema_name(args.input_path, args.schema_name, args.target_resolution)

        self.start_yamig(args)
    

    def start_yamig(self, args) -> None:
        self.logger.info('amig started')

        self.logger.debug(f'image size (tile displays): {args.target_resolution[0]//32}x{args.target_resolution[1]//32}')

        ### Preprocessing ###
        preprocessor = Preprocessor(
            args.input_path,
            args.target_resolution,
            args.max_colors
        )
        image, palette = preprocessor.run()
        
        # saving jpg
        preprocessed_image_path = args.output_path / 'preprocessed.jpg'
        self.logger.debug(f'saving preprocessed image to {str(preprocessed_image_path)}')
        image.save(preprocessed_image_path)

        ### Quadtree ###
        self.logger.info('starting quadtree')
        quadtree = QuadtreeProcessor(
            image,
            args.min_region_size,
            args.dispersion_threshold,
            palette
        )
        rects = quadtree.rects2int(quadtree.decompose(0, 0, *args.target_resolution))

        self.logger.info(f'image decomposed to {len(rects)} rects (~{len(rects)//900} processors)')

        # saving json
        rects_path = args.output_path / 'quadtree_rects.json'
        self.logger.debug(f'saving rectangles to {str(rects_path)}')
        with rects_path.open(mode='w') as file:
            json.dump(rects, file, indent=1)
        
        # saving recomposed image
        recomposed_image = quadtree.recompose(args.target_resolution, rects)
        recomposed_image_path = args.output_path / 'quadtree_recomposed.jpg'
        self.logger.debug(f'saving recomposed image to {str(recomposed_image_path)}')
        recomposed_image.save(recomposed_image_path)

        ### Mlog ###
        mlog_generator = MlogGenerator(
            args.max_script_length,
            args.display_name,
            args.target_resolution
        )
        scripts = mlog_generator.generate_mlog(rects)

        # removing previous scripts
        scripts_path = args.output_path / 'scripts'
        scripts_path.mkdir(exist_ok=True)

        for script in scripts_path.iterdir():
            os.remove(script)

        # saving scripts
        for script_i, script in enumerate(scripts, start=1):
            self.logger.debug(f'saving script {script_i}')
            with (scripts_path / f'processor_{script_i}.txt').open(mode='w') as file:
                file.write('\n'.join(script))
        

        ### Schema ###
        schema_generator = SchemaGenerator(
            scripts,
            args.target_resolution,
            args.schema_name,
            args.schema_description
        )

        schema = schema_generator.generate_schema()

        schema_path = args.output_path / f"{args.schema_name.replace(' ', '_')}.msch"
        self.logger.info(f'saving schema to {str(schema_path)}')
        schema.write_file(schema_path)
        schema.write_clipboard()


def run_cli() -> None:
    try:
        yamigcli().run_cli()
        sys.exit(0)
    
    except Exception as e:
        print(
            f'\033[31m{e.__class__.__name__}: {str(e)}.'
            + (f' Cause: {e.__cause__}\033[0m' if e.__cause__ else '\033[0m')
        )
        sys.exit(1)

if __name__ == '__main__':
    run_cli()