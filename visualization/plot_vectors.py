# visualization/plot_vectors.py

import numpy as np


def calculate_scale(x, y, z, vector_mag):
    """Tính toán hệ số tỷ lệ dựa trên kích thước quỹ đạo tối đa."""
    max_displacement = np.max(np.abs(np.concatenate((x, y, z))))

    # Nếu quỹ đạo quá nhỏ, sử dụng một giá trị mặc định để tỷ lệ hóa
    if max_displacement < 1e-12:
        return 1e-6 / vector_mag if vector_mag != 0 else 0

    # Tính toán tỷ lệ sao cho vector có độ dài khoảng 1/5 quỹ đạo tối đa
    return (max_displacement / 5.0) / vector_mag if vector_mag != 0 else 0


def plot_MagneticField_vectors(ax, x, y, z, B):
    B_mag = np.linalg.norm(B)

    # Tính toán hệ số tỷ lệ riêng biệt cho B
    B_scale = calculate_scale(x, y, z, B_mag)
    # Vẽ Vector B
    ax.quiver(
        0,
        0,
        0,
        B[0] * B_scale,
        B[1] * B_scale,
        B[2] * B_scale,
        color="purple",
        length=1.5,
        arrow_length_ratio=0.15,
        label=f"Vector B = {B} T",
        linewidth=2,
    )


def plot_ElectricField_vector(ax, x, y, z, E_static):
    E_mag = np.linalg.norm(E_static)

    E_scale = calculate_scale(x, y, z, E_mag)
    # Vẽ Vector E
    ax.quiver(
        0,
        0,
        0,
        E_static[0] * E_scale,
        E_static[1] * E_scale,
        E_static[2] * E_scale,
        color="red",
        length=2.0,
        arrow_length_ratio=0.15,
        label=f"Vector E = {E_static} V/m",
        linewidth=2,
    )


def plot_Velocity_vector(ax, x, y, z, v0):
    """
    Vẽ vector vận tốc ban đầu v0 (giả sử tại r0 = 0,0,0).
    """
    v0_mag = np.linalg.norm(v0)

    # Tính toán hệ số tỷ lệ cho v0 (sử dụng kích thước quỹ đạo tương tự E/B)
    v0_scale = calculate_scale(x, y, z, v0_mag)

    # Vẽ Vector v0 tại gốc (0, 0, 0)
    ax.quiver(
        0,
        0,
        0,
        v0[0] * v0_scale,
        v0[1] * v0_scale,
        v0[2] * v0_scale,
        color="orange",
        length=3.0,
        arrow_length_ratio=0.15,
        label=f"Vector v0 = {v0} m/s",
        linewidth=2,
    )
