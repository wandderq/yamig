# yamig
yet another mindustry image generator

yamig uses tiled logic displays and microprocessors

for now it only works in CLI (mby i'll make a mod for Mindustry)

**the project is still raw and contains many errors, inaccuracies, workarounds, and typos (feel free to open bug reports on GitHub)**

## Usage
```
usage: yamig [-h] [-o OUTPUT_PATH] [-r TARGET_RESOLUTION] [-c MAX_COLORS] [-R MIN_REGION_SIZE] [-t DISPERSION_THRESHOLD] [-l MAX_SCRIPT_LENGTH] [-d DISPLAY_NAME]
             [-N SCHEMA_NAME] [-D SCHEMA_DESCRIPTION] [-v]
             input_path

yet another mindustry image generator

positional arguments:
  input_path            input image filepath

options:
  -h, --help            show this help message and exit
  -o, --output-path OUTPUT_PATH
                        output directory (default: derived from input_path)
  -r, --target-resolution TARGET_RESOLUTION
                        target resolution (default: 320x192)
  -c, --max-colors MAX_COLORS
                        max colors in the target image (default: 64) (may be inaccurate, +-15% after quadtree)
  -R, --min-region-size MIN_REGION_SIZE
                        minimal quadtree region size (px) (default: 8)
  -t, --dispersion-threshold DISPERSION_THRESHOLD
                        quadtree color dispersion threshold (default: 600)
  -l, --max-script-length MAX_SCRIPT_LENGTH
                        max lines of script in each processor (default: 1000)
  -d, --display-name DISPLAY_NAME
                        display to draw to (default: display1)
  -N, --schema-name SCHEMA_NAME
                        output schematic name (default: derived from other args)
  -D, --schema-description SCHEMA_DESCRIPTION
                        output schematic description (default: None)
  -v, --verbose         debug logs
```

## Licensing
this project is distributed under the **MIT License**

full license text: [LICENSE](https://github.com/wandderq/yamig/blob/main/LICENSE)
