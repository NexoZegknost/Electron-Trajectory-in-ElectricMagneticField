# visualization/plot_vectors.py

import numpy as np


def plot_field_vectors(ax, x, y, z, E_static, B):
    """
    Vẽ các vector E và B trên axes.
    """
    E_mag_norm = np.linalg.norm(E_static)
    max_displacement = np.max(np.abs(np.concatenate((x, y, z))))
    E_scale = (max_displacement / 5.0) / E_mag_norm if E_mag_norm != 0 else 0
    B_scale = (max_displacement / 5.0) / np.linalg.norm(B)

    # Vẽ Vector E
    ax.quiver(
        0,
        0,
        0,
        E_static[0] * E_scale,
        E_static[1] * E_scale,
        E_static[2] * E_scale,
        color="darkgreen",
        length=1.0,
        arrow_length_ratio=0.15,
        label=f"Vector E",
        linewidth=2,
    )

    # Vẽ Vector B
    ax.quiver(
        0,
        0,
        0,
        B[0] * B_scale,
        B[1] * B_scale,
        B[2] * B_scale,
        color="purple",
        length=1.0,
        arrow_length_ratio=0.15,
        label=f"Vector B",
        linestyle="--",
        linewidth=2,
    )
