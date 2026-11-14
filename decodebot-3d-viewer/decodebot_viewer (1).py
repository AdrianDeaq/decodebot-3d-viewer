"""
View the HSGS RoboLads DecodeBot GLB model in 3D with Python.

Install:  pip install trimesh numpy "pyglet<2" plotly fast-simplification
Also needed (one time): Node.js from nodejs.org. The site's GLB is meshopt-compressed,
and this script uses it to decompress the file automatically.
Usage:
  python decodebot_viewer.py --url https://31113robolads.vercel.app/<path>/DecodeBot.web.glb
  python decodebot_viewer.py --file DecodeBot.web.glb
  python decodebot_viewer.py --file DecodeBot.web.glb --explode 0.6
  python decodebot_viewer.py --file DecodeBot.web.glb --html robot.html   (browser view, no OpenGL needed)

Find the real URL: open the /cad page, press F12 -> Network tab -> reload,
filter by "glb", right-click the DecodeBot.web.glb request -> Copy link address.
"""
import argparse
import os
import shutil
import subprocess
import urllib.request

import numpy as np
import trimesh


def download(url, path="DecodeBot.web.glb"):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())
    print(f"Downloaded -> {path}")
    return path


def decompress(path):
    """The site's GLB uses EXT_meshopt_compression, which trimesh can't read.
    Decompress it once with gltf-transform (needs Node.js)."""
    out = os.path.splitext(path)[0] + "_plain.glb"
    if os.path.exists(out):
        return out
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        raise SystemExit("Install Node.js from https://nodejs.org then run again "
                         "(needed to decompress the model).")
    print("Decompressing model (first run only, may take a minute)...")
    subprocess.run([npx, "-y", "@gltf-transform/cli", "copy", path, out], check=True)
    return out


def load_robot(path):
    try:
        return trimesh.load(path, force="scene")
    except Exception:
        return trimesh.load(decompress(path), force="scene")


def explode(scene, factor):
    """Push every part radially away from the robot's center (like the site's EXPLODE mode)."""
    out = scene.copy()
    center = scene.bounds.mean(axis=0)
    size = float(np.linalg.norm(scene.extents))
    for node in list(out.graph.nodes_geometry):
        world, gname = out.graph[node]
        geom = out.geometry[gname]
        part_center = (world @ np.append(geom.centroid, 1.0))[:3]
        direction = part_center - center
        norm = np.linalg.norm(direction)
        if norm < 1e-9:
            continue
        moved = world.copy()
        moved[:3, 3] += direction / norm * factor * size
        out.graph.update(frame_to=node, matrix=moved)
    return out


def export_html(scene, path, max_faces=150000):
    import plotly.graph_objects as go

    meshes = [m for m in scene.dump(concatenate=False) if isinstance(m, trimesh.Trimesh)]
    total = sum(len(m.faces) for m in meshes)
    ratio = min(1.0, max_faces / max(total, 1))
    print(f"{total} faces -> simplifying to ~{int(total * ratio)} for the browser")

    fig = go.Figure()
    for i, m in enumerate(meshes):
        if ratio < 1.0 and len(m.faces) > 400:
            try:
                keep = max(200, int(len(m.faces) * ratio))
                m = m.simplify_quadric_decimation(face_count=keep)
            except Exception as e:
                print("  (skipped simplify for one part:", e, ")")
        try:
            rgb = m.visual.to_color().face_colors[:, :3].mean(axis=0).astype(int)
        except Exception:
            rgb = (150, 150, 160)
        v, f = m.vertices, m.faces
        fig.add_trace(go.Mesh3d(
            x=v[:, 0], y=v[:, 1], z=v[:, 2], i=f[:, 0], j=f[:, 1], k=f[:, 2],
            color=f"rgb({rgb[0]},{rgb[1]},{rgb[2]})", flatshading=True,
            name=f"part_{i}", opacity=1.0))
    fig.update_layout(scene=dict(aspectmode="data"), margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html(path, include_plotlyjs="cdn")
    print(f"Wrote {path} - open it in your browser")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--file")
    ap.add_argument("--explode", type=float, default=0.0, help="0 = assembled, ~0.5 = exploded")
    ap.add_argument("--html", help="export an interactive HTML instead of opening a window")
    args = ap.parse_args()

    path = args.file or (download(args.url) if args.url else None)
    if not path:
        ap.error("give --url or --file")

    scene = load_robot(path)
    print(f"{len(scene.geometry)} meshes, size {scene.extents}")
    for name in scene.geometry:
        print(" -", name)

    if args.explode > 0:
        scene = explode(scene, args.explode)

    if args.html:
        export_html(scene, args.html)
    else:
        scene.show()  # drag to rotate, scroll to zoom


if __name__ == "__main__":
    main()
