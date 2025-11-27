# visualization/plot_setup.py

import matplotlib.pyplot as plt
import numpy as np


def setup_plot(x, y, z, E_static, B, title):
    """
    Tạo figure và axes 3D, thiết lập giới hạn trục dựa trên dữ liệu quỹ đạo.
    Trả về fig, ax.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(title)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    # Tính toán giới hạn trục an toàn
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    z_min, z_max = z.min(), z.max()

    max_range = np.array([x_max - x_min, y_max - y_min, z_max - z_min]).max() / 2.0
    mid_x, mid_y, mid_z = (
        (x_max + x_min) * 0.5,
        (y_max + y_min) * 0.5,
        (z_max + z_min) * 0.5,
    )
    if max_range < 1e-12:
        max_range = 1e-6

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    return fig, ax
