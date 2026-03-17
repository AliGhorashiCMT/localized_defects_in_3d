"""
render3d.py  —  Interactive 3D rendering of MEEP HDF5 output files.

Usage:
    python render3d.py <file.h5> [options]

Options:
    --dataset DSNAME   Dataset to read (default: auto-detect first dataset)
    --downsample N     Keep every Nth voxel along each axis (default: auto)
    --isovalue VAL     Isosurface value(s), comma-separated (default: auto)
    --mode MODE        'iso' for isosurface, 'vol' for volume render (default: iso)
    --out FILE.html    Save interactive HTML instead of opening browser

Examples:
    python render3d.py gyr-eps-000000.00.h5
    python render3d.py gyr-eps-000000.00.h5 --mode vol
    python render3d.py rscan-2-ez-001134.28.h5 --mode vol --downsample 4
    python render3d.py gyr-eps-000000.00.h5 --isovalue 2,8 --out struct.html
"""

import argparse
import sys
import numpy as np
import h5py
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_dataset(path, dsname=None):
    with h5py.File(path, "r") as f:
        if dsname is None:
            datasets = []
            f.visititems(lambda n, obj: datasets.append(n) if isinstance(obj, h5py.Dataset) else None)
            if not datasets:
                raise ValueError(f"No datasets found in {path}")
            dsname = datasets[0]
            print(f"Auto-selected dataset: '{dsname}'")
        data = f[dsname][:]
    return data, dsname


def downsample(data, factor):
    return data[::factor, ::factor, ::factor]


def auto_downsample(shape, max_voxels=200**3):
    n = max(shape)
    factor = 1
    while (n // factor) ** 3 > max_voxels:
        factor += 1
    return factor


def auto_isovalue(data):
    """Single isovalue just above the minimum (air/material boundary)."""
    lo, hi = data.min(), data.max()
    unique = np.unique(data.round(3))
    if len(unique) <= 20:
        # Discrete dielectric: pick just above the air value
        return float(unique[0]) + 0.1 * (float(unique[1]) - float(unique[0]))
    # Continuous field: midpoint
    return lo + 0.5 * (hi - lo)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def make_isosurface_fig(data, isovalue, title):
    nx, ny, nz = data.shape
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    z = np.linspace(0, 1, nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    fig = go.Figure()
    color = "royalblue"

    fig.add_trace(go.Isosurface(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=data.ravel(),
        isomin=isovalue, isomax=data.max(),
        surface_count=1,
        colorscale=[[0, color], [1, color]],
        showscale=False,
        opacity=0.9,
        flatshading=True,
        lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0,
                      roughness=1.0, fresnel=0.0),
        name=f"iso={isovalue:.3g}",
        caps=dict(x_show=False, y_show=False, z_show=False),
    ))

    clean_axis = dict(
        showgrid=False, zeroline=False, showline=False,
        showticklabels=False, showspikes=False,
        backgroundcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(title="", **clean_axis),
            yaxis=dict(title="", **clean_axis),
            zaxis=dict(title="", **clean_axis),
            aspectmode="data",
            bgcolor="white",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor="white",
    )
    return fig


def make_volume_fig(data, title):
    nx, ny, nz = data.shape
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    z = np.linspace(0, 1, nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    vmin, vmax = data.min(), data.max()
    # Symmetric colorscale for field data (could be negative)
    abs_max = max(abs(vmin), abs(vmax))
    if vmin < 0:
        colorscale = "RdBu"
        cmin, cmax = -abs_max, abs_max
    else:
        colorscale = "Plasma"
        cmin, cmax = vmin, vmax

    fig = go.Figure(go.Volume(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=data.ravel(),
        isomin=cmin + 0.05 * (cmax - cmin),
        isomax=cmax,
        opacity=0.1,
        surface_count=20,
        colorscale=colorscale,
        cmin=cmin, cmax=cmax,
        caps=dict(x_show=False, y_show=False, z_show=False),
    ))

    clean_axis = dict(
        showgrid=False, zeroline=False, showline=False,
        showticklabels=False, showspikes=False,
        backgroundcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(title="", **clean_axis),
            yaxis=dict(title="", **clean_axis),
            zaxis=dict(title="", **clean_axis),
            aspectmode="data",
            bgcolor="white",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor="white",
    )
    return fig


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="3D render of MEEP HDF5 data")
    parser.add_argument("file", help="Path to .h5 file")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--downsample", type=int, default=None)
    parser.add_argument("--isovalue", default=None,
                        help="Single isovalue threshold (default: auto-detect material boundary)")
    parser.add_argument("--mode", choices=["iso", "vol"], default="iso")
    parser.add_argument("--out", default=None, help="Save to HTML file")
    args = parser.parse_args()

    # --- Load ---
    print(f"Loading {args.file} ...")
    data, dsname = load_dataset(args.file, args.dataset)
    print(f"  shape={data.shape}  min={data.min():.4g}  max={data.max():.4g}")

    # --- Downsample ---
    factor = args.downsample
    if factor is None:
        factor = auto_downsample(data.shape)
    if factor > 1:
        data = downsample(data, factor)
        print(f"  downsampled by {factor}x → shape={data.shape}")

    title = f"{args.file.split('/')[-1]} — dataset: {dsname}"

    # --- Render ---
    if args.mode == "iso":
        isovalue = float(args.isovalue) if args.isovalue else auto_isovalue(data)
        print(f"  isovalue: {isovalue:.3g}")
        fig = make_isosurface_fig(data, isovalue, title)
    else:
        fig = make_volume_fig(data, title)

    # --- Show / save ---
    if args.out:
        fig.write_html(args.out)
        print(f"Saved to {args.out}")
    else:
        fig.show()


if __name__ == "__main__":
    main()
