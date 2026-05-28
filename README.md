# yamig
**Yet Another Mindustry Image Generator** — converts PNG/JPG images into Mindustry schematics.

**⚠️ Project Status: WIP** - the tool may contain bugs and rough edges.


## Features
- works only with **tile displays** and **micro processors**
- fully customizable schematic generation:
  - image resolution & scaling
  - color quantization limits
  - quadtree optimization parameters
  - schematic metadata (name, description)
  - output format options


## Installation
Python 3.12 or higher is required.

### From GitHub (recommended via pipx)
```bash
pipx install git+https://github.com/wandderq/yamig.git
```


## Dependencies
- `pillow` - image processing
- `numpy` - array operations
- `scipy` - cKDTree (will be removed in future)
- `pymsch` - schematic generating

## Usage
### Positional arguments
| argument | description |
|----------|-------------|
|`input_path`|input image path (PNG/JPG)|

### Options
| option | description |
|--------|-------------|
|`-h, --help`|show help message|
|`-o, --output`|output directory (default: derived from input)|
|`-O, --onefile`|save only `.msch` file|
|`-C, --copy-to-clipboard`|copy schematic to clipboard|
|`-r, --resolution`|target resolution (format: `WxH[b/px]`) (default: `5x5b`)|
|`-c, --max-colors`|max colors in output (default: `64`) (up to 15% loss)|
|`-d, --dispersion-threshold`|quadtree color dispersion threshold (default: `600`)|
|`-s, --min-region-size`|min quadtree region size in pixels (default: `8`)|
|`-l, --max-script-len`|max lines per processor script (default: `1000`)|
|`-N, --schema-name`|schematic name (default: derived from input)|
|`-D, --schema-desc`|schematic description (default: derived from input)|
|`-v, --verbose`|verbose mode (debug logs)|
|`-q, --quiet`|quiet mode (warnings/errors only)|
|`--silent`|silent mode (no logs)|


## Examples
1. basic usage
```bash
yamig picture.jpg 
```
2. custom resolution and output
```bash
yamig picture.jpg --onefile -o . -r  800x600px
```
3. higher quality
```bash
yamig picture.jpg -r 16x9b -c 128 -s 2 -d 200
```
4. accelerated rendering (but more processors)
```bash
yamig picture.jpg -l 300 -N "fast picture"
```

## License
Distributed under [MIT License](https://github.com/wandderq/yamig/blob/main/LICENSE) - free to use, modify, and distribute

---
<p align=center><i>because there can never be enough mindustry image generators</i></p>
