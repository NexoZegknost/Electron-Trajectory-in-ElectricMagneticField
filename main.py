# main.py

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import os

# Import các module đã phân chia
from engine import run_cpp_simulation, B, lib, q, m
from interface import *
from visualization.plot_setup import *
from visualization.plot_vectors import *
from visualization.animation_core import *


# --- Hàm Chính Chạy Mô phỏng ---
def run_simulation_from_gui(entries, tmax_entry, root):
    """Quản lý luồng chương trình từ GUI, tính toán đến Visualization."""

    if lib is None:
        messagebox.showerror(
            "Lỗi C++", "Không thể tìm thấy hoặc tải thư viện ODE.dll/so."
        )
        return

    # 1. Lấy dữ liệu từ GUI
    r0, v0, E_static, tmax = get_input_values(entries, tmax_entry, root)
    if r0 is None:
        return

    # 2. Gọi C++ để tính toán
    x, y, z = run_cpp_simulation(r0, v0, E_static, tmax)
    if x is None:
        return  # Thoát nếu tính toán phân kỳ

    # 3. Chuẩn bị dữ liệu Animation
    num_total_points = len(x)
    num_frames = 1000
    indices = np.linspace(0, num_total_points - 1, num_frames, dtype=int)
    x_anim = x[indices]
    y_anim = y[indices]
    z_anim = z[indices]

    vx_full = np.gradient(x, axis=0)
    vy_full = np.gradient(y, axis=0)
    vz_full = np.gradient(z, axis=0)

    vx_anim = vx_full[indices]
    vy_anim = vy_full[indices]
    vz_anim = vz_full[indices]

    # 4. Thiết lập Plot
    title = f"Quỹ đạo của electron trong máy gia tốc hạt Cyclotron"
    fig, ax = setup_plot(x, y, z, E_static, B, title)

    # 5. Vẽ Vector
    plot_ElectricField_vector(ax, x, y, z, E_static)
    plot_MagneticField_vectors(ax, x, y, z, B)
    plot_Velocity_vector(ax, x, y, z, v0)

    # 6. Khởi tạo đối tượng Animation
    line_animated, point, line_final = create_animation_objects(
        ax, x_anim, y_anim, z_anim
    )

    # Cập nhật legend sau khi tạo tất cả các đối tượng có nhãn
    ax.legend()

    # 7. Chạy Animation
    ani = run_animation(
        fig,
        ax,
        line_animated,
        point,
        line_final,
        x_anim,
        y_anim,
        z_anim,
        vx_anim,
        vy_anim,
        vz_anim,  # <-- Dữ liệu vận tốc
        E_static,
        B,
        q,
        m,  # <-- Hằng số vật lý
        num_frames,
    )

    print(f"\nAnimation đang chạy với {num_frames} frames.")

    # >>> KHẮC PHỤC CẢNH BÁO: Đảm bảo đối tượng ani được giữ lại <<<
    # Điều này ngăn Matplotlib tự động dọn dẹp đối tượng animation
    ani._stop = False  # Khôi phục trạng thái cũ (nếu cần), hoặc
    ani.frame_seq = ani.new_frame_seq()  # <-- Sửa lỗi chính tả

    plt.show()


# --- Hàm Tạo Cửa sổ Chính ---
def create_main_window():
    root = tk.Tk()
    root.title("Nhập Tham số Chuyển động Điện Từ (C++ Engine)")

    entries, tmax_entry = create_input_fields(root)

    # Sử dụng lambda để truyền các tham số cần thiết khi nút được nhấn
    run_button = tk.Button(
        root,
        text="Chạy Mô phỏng",
        command=lambda: run_simulation_from_gui(entries, tmax_entry, root),
    )
    run_button.grid(row=len(entries) + 1, columnspan=2, pady=10)

    tk.Label(
        root, text="LƯU Ý: Tính toán C++ dùng Euler đơn giản (kém ổn định).", fg="red"
    ).grid(row=len(entries) + 2, columnspan=2, pady=5)

    root.mainloop()


# ----------------------------------------------------------------------
# --- BẮT ĐẦU CHƯƠNG TRÌNH ---
# ----------------------------------------------------------------------
if __name__ == "__main__":
    create_main_window()
