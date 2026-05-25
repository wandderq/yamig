# yamig
yet another mindustry image generator

yamig uses tiled logic displays and microprocessors

for now it only works in CLI (mby i'll make a mod for Mindustry)

**the project is still raw and contains many errors, inaccuracies, workarounds, and typos (feel free to open bug reports on GitHub)**

## Usage
```
usage: yamig [-h] [-o OUTPUT_PATH] [-O] [-C] [-r RESOLUTION] [-c MAX_COLORS] [-t DISPERSION_THRESHOLD]
             [-s MIN_REGION_SIZE] [-l MAX_SCRIPT_LEN] [-N SCHEMA_NAME] [-D SCHEMA_DESC] [-v | -q | --silent]
             input_path

yet another mindustry image generator v0.1.1

positional arguments:
  input_path            input image path

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT_PATH
                        output directory (default: derived from args)
  -O, --onefile         save only .msch file
  -C, --copy-to-clipboard
                        copy schematic to clipboard
  -r, --resolution RESOLUTION
                        target resolution (format: WxH[b/px]) (default: 5x5b)
  -c, --max-colors MAX_COLORS
                        max target image colors (default: 64) (up to 15% loss)
  -t, --dispersion-threshold DISPERSION_THRESHOLD
                        quadtree color dispersion threshold (default: 600)
  -s, --min-region-size MIN_REGION_SIZE
                        min quadtree region size (px) (default: 8)
  -l, --max-script-len MAX_SCRIPT_LEN
                        max lines of script in each processor (default: 100)
  -N, --schema-name SCHEMA_NAME
                        schematic name (default: derived from args)
  -D, --schema-desc SCHEMA_DESC
                        schematic description (default: derived from args)
  -v, --verbose         verbose mode (debug logs)
  -q, --quiet           quiet mode (warn/err logs)
  --silent              silent mode (no logs)
```
## TODO
- [ ] find and fix typos
- [ ] more logging
- [x] -q/--quiet mode
- [ ] schema tags
- [x] onefile mode (without preoprocessed.jpg, recomposed.jpg, scripts/, etc.)
- [x] -C/--copy-to-clipboard instead of automatically copying
- [ ] make this readme more organized and readable

## Licensing
this project is distributed under the **MIT License**

full license text: [LICENSE](https://github.com/wandderq/yamig/blob/main/LICENSE)

