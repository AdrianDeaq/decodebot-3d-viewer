# DecodeBot 3D Viewer

Hi, this is the 3D model from our team (Robolab#3113). This is the **v3 bot**, from 2 months before the regional round.

## To use it simply

Inside the `views/` folder, I made 2 HTML files, one for the assembled robot and one for the exploded view. Check them out:

- `views/decodebot_assembled.html`
- `views/decodebot_exploded.html`
<img width="768" height="830" alt="image" src="https://github.com/user-attachments/assets/3d2b8983-db2d-41d6-bbb0-881d242a6bf8" />


Download one and double-click it to open it in your browser (details in [Quick start](#quick-start-just-look-at-the-robot) below).

## If you want to run it on your computer

Use the Python script to open the full-detail model in a 3D window. Steps are in [Run the Python script](#run-the-python-script) below.

## What's in this repo

```
decodebot-3d-viewer/
├── README.md
├── decodebot_viewer.py
├── model/
│   └── DecodeBot_opt.glb
└── views/
    ├── decodebot_assembled.html
    └── decodebot_exploded.html
```

| File | What it is |
| --- | --- |
| `decodebot_viewer.py` | Python script that loads the model and shows it in 3D |
| `model/DecodeBot_opt.glb` | The robot's 3D model (50 parts, about 734,000 triangles) |
| `views/decodebot_assembled.html` | Ready-made browser view of the full robot |
| `views/decodebot_exploded.html` | Ready-made browser view with the parts spread apart |

## Quick start: just look at the robot

No install needed. Download `views/decodebot_assembled.html` or `views/decodebot_exploded.html` and double-click it to open in Chrome or Edge. You need an internet connection because the page loads Plotly from a CDN.

- **Drag** to rotate
- **Scroll** to zoom
- **Right-drag** to move the view

The HTML views are simplified (about 150,000 triangles) to keep them light. Use the Python script for the full-detail model.

## Run the Python script

### 1. Requirements

- [Python 3.8+](https://www.python.org/downloads/) (on Windows, tick "Add Python to PATH" during installation)
- [Node.js](https://nodejs.org) (used once to decompress the model; see the note below)

Install the Python libraries:

```
pip install trimesh numpy "pyglet<2" plotly fast-simplification
```

A warning like `trimesh.exe is installed in ... which is not on PATH` is harmless and can be ignored.

### 2. Run it

Open a terminal in the repo folder and run:

```
python decodebot_viewer.py --file model/DecodeBot_opt.glb
```

A 3D window opens. The first run takes about a minute while the model is decompressed.

### Options

| Option | What it does | Example |
| --- | --- | --- |
| `--file PATH` | Load a local `.glb` file | `--file model/DecodeBot_opt.glb` |
| `--url LINK` | Download a `.glb` from a link, then load it | `--url https://example.com/robot.glb` |
| `--explode N` | Spread the parts out. `0` is assembled, `0.5` is a good exploded view | `--explode 0.5` |
| `--html FILE` | Save an interactive browser page instead of opening a window | `--html robot.html` |

### Examples

Assembled robot in a window:

```
python decodebot_viewer.py --file model/DecodeBot_opt.glb
```

Exploded view in a window:

```
python decodebot_viewer.py --file model/DecodeBot_opt.glb --explode 0.5
```

Save an exploded view as an HTML page:

```
python decodebot_viewer.py --file model/DecodeBot_opt.glb --explode 0.5 --html my_exploded.html
```

The script also prints the name of every part in the model.

## About the .glb file

`.glb` is a standard 3D file format (binary glTF) that opens in many tools, including [Blender](https://www.blender.org), the [glTF Viewer](https://gltf-viewer.donmccurdy.com), and Windows 3D Viewer.

`DecodeBot_opt.glb` is **meshopt-compressed**, which keeps the file small (about 3.4 MB) but means some Python libraries can't read it directly. That is why the script uses Node.js: on the first run, it decompresses the model with `@gltf-transform/cli` and saves a copy named `DecodeBot_opt_plain.glb` next to the original. Later runs reuse that copy.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `'python' is not recognized` | Try `py` or `python3` instead |
| `No module named trimesh` | Run the `pip install` command above again |
| `Install Node.js ... then run again` | Install Node.js from nodejs.org, reopen the terminal, and retry |
| The 3D window doesn't open | Use `--html robot.html` and open that file in your browser |
| Download error (403 or 404) with `--url` | Download the `.glb` manually and use `--file` instead |

## Credits
Please ask me before reusing the model outside this project.
