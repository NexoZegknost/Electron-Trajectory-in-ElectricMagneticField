import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import ctypes
from matplotlib.animation import FuncAnimation

# ----------------------------------------------------------------------
# --- PHẦN 1: TÍCH HỢP C++ VÀ CÁC HẰNG SỐ ---
# ----------------------------------------------------------------------
m = 9.109e-31
q = -1.602e-19
B = np.array([0.0, 0.0, 1.0])


class Result(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double * 1000),
        ("y", ctypes.c_double * 1000),
        ("z", ctypes.c_double * 1000),
    ]


lib = None
try:
    lib = ctypes.CDLL("./ODE.dll")
    lib.run_simulation.argtypes = [
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.POINTER(Result),
    ]
    lib.run_simulation.restype = None
except OSError as e:
    print(f"Lỗi: Không thể tìm thấy hoặc tải thư viện C++ (ODE.dll/so): {e}")


# ----------------------------------------------------------------------
# --- PHẦN 2: CHỨC NĂNG GUI VÀ CHẠY MÔ PHỎNG ---
# ----------------------------------------------------------------------


def run_simulation_from_gui(entries, tmax_entry, root):
    """Lấy dữ liệu từ GUI, gọi C++ tính toán, và tạo Animation."""

    if lib is None:
        messagebox.showerror(
            "Lỗi C++",
            "Không thể tìm thấy hoặc tải thư viện ODE.dll/so. Vui lòng kiểm tra lại file biên dịch.",
        )
        return

    try:
        inputs = [float(entry.get()) for entry in entries]
        tmax = float(tmax_entry.get())
        r0 = np.array(inputs[0:3])
        v0 = np.array(inputs[3:6])
        E_static = np.array(inputs[6:9])
        root.destroy()
    except ValueError:
        messagebox.showerror(
            "Lỗi nhập liệu", "Vui lòng nhập giá trị số hợp lệ cho tất cả các trường."
        )
        return

    # --- 3. GỌI TÍNH TOÁN BẰNG C++ ---
    print("\nĐang gọi C++ tính toán quỹ đạo...")
    output_struct = Result()
    lib.run_simulation(
        r0[0],
        r0[1],
        r0[2],
        v0[0],
        v0[1],
        v0[2],
        E_static[0],
        E_static[1],
        E_static[2],
        tmax,
        ctypes.pointer(output_struct),
    )

    # 4. NHẬN DỮ LIỆU VÀ XỬ LÝ LỖI
    x = np.array(output_struct.x[:])
    y = np.array(output_struct.y[:])
    z = np.array(output_struct.z[:])

    if np.any(np.isnan(x)) or np.any(np.isinf(x)) or np.any(np.isinf(y)):
        messagebox.showerror(
            "Lỗi Phân kỳ Tính toán", f"Dữ liệu quỹ đạo bị phân kỳ. Vui lòng giảm T_MAX."
        )
        return

    # -------------------------------------------------
    # --- 5. TẠO VÀ CHẠY ANIMATION (ĐÃ TỐI ƯU) ---
    # -------------------------------------------------

    # Lấy mẫu dữ liệu cho Animation
    num_total_points = len(x)
    num_frames = 1000
    indices = np.linspace(0, num_total_points - 1, num_frames, dtype=int)

    x_anim = x[indices]
    y_anim = y[indices]
    z_anim = z[indices]

    # Thiết lập Figure và Axes
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(f"Animation Chuyển động Electron (E={E_static} V/m, B={B} T)")
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

    # Khởi tạo các đối tượng:
    (line_animated,) = ax.plot(
        x_anim[0:1],
        y_anim[0:1],
        z_anim[0:1],
        color="blue",
        label="Quỹ đạo đang đi",
        linewidth=1.5,
    )
    (point,) = ax.plot(
        [x_anim[0]],
        [y_anim[0]],
        [z_anim[0]],
        marker="o",
        color="red",
        markersize=8,
        label="Electron",
    )
    (line_final,) = ax.plot([], [], [], color="blue", linewidth=1.5, visible=False)

    # Vẽ vector E và B (Giữ nguyên)
    E_mag_norm = np.linalg.norm(E_static)
    max_displacement = np.max(np.abs(np.concatenate((x, y, z))))
    E_scale = (max_displacement / 5.0) / E_mag_norm if E_mag_norm != 0 else 0
    B_scale = (max_displacement / 5.0) / np.linalg.norm(B)

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

    ax.legend()

    # Hàm cập nhật frame cho animation
    def animate(i):
        # Cập nhật vị trí điểm electron (xảy ra trong mỗi frame)
        point.set_data_3d([x_anim[i]], [y_anim[i]], [z_anim[i]])
        line_animated.set_data_3d(x_anim[: i + 1], y_anim[: i + 1], z_anim[: i + 1])

        # BƯỚC XỬ LÝ KHI ĐẠT FRAME CUỐI
        if i == num_frames - 1:
            ani.event_source.stop()

            # Ẩn đường tạm thời
            line_animated.set_visible(False)

            # Vẽ quỹ đạo hoàn chỉnh
            line_final.set_data_3d(x_anim, y_anim, z_anim)
            line_final.set_visible(True)

            # Cập nhật VỊ TRÍ CUỐI CÙNG của điểm electron lần cuối
            point.set_data_3d([x_anim[-1]], [y_anim[-1]], [z_anim[-1]])

            # Cập nhật legend
            line_final.set_label("Quỹ đạo Hoàn chỉnh")
            ax.legend()

            # Bắt buộc vẽ lại để đảm bảo mọi đối tượng (bao gồm chấm đỏ) hiển thị
            fig.canvas.draw_idle()

        return line_animated, point

    # Tạo Animation
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=50, blit=True)

    print(f"\nAnimation đang chạy với {num_frames} frames.")

    plt.show()


# ----------------------------------------------------------------------
# --- PHẦN 3: HÀM TẠO GUI (GIỮ NGUYÊN) ---
# ----------------------------------------------------------------------


def create_gui():
    """Tạo cửa sổ GUI để nhập 9 tham số vector và thời gian mô phỏng."""
    root = tk.Tk()
    root.title("Nhập Tham số Chuyển động Điện Từ (C++ Engine)")

    fields = [
        ("Vị trí Ban đầu x0 (m):", "0.0", "r0_x"),
        ("Vị trí Ban đầu y0 (m):", "0.0", "r0_y"),
        ("Vị trí Ban đầu z0 (m):", "0.0", "r0_z"),
        ("Vận tốc Ban đầu vx (m/s):", "1e6", "v0_x"),
        ("Vận tốc Ban đầu vy (m/s):", "0.0", "v0_y"),
        ("Vận tốc Ban đầu vz (m/s):", "0.0", "v0_z"),
        ("E-trường Tĩnh Ex (V/m):", "0.0", "E_x"),
        ("E-trường Tĩnh Ey (V/m):", "0.0", "E_y"),
        ("E-trường Tĩnh Ez (V/m):", "10.0", "E_z"),
    ]

    entries = []

    for i, (label_text, default_value, name) in enumerate(fields):
        tk.Label(root, text=label_text).grid(
            row=i, column=0, padx=10, pady=2, sticky="w"
        )
        entry = tk.Entry(root)
        entry.insert(0, default_value)
        entry.grid(row=i, column=1, padx=10, pady=2)
        entries.append(entry)

    tk.Label(root, text="Tổng thời gian T_MAX (s):").grid(
        row=len(fields), column=0, padx=10, pady=5, sticky="w"
    )
    tmax_entry = tk.Entry(root)
    tmax_entry.insert(0, "1e-7")
    tmax_entry.grid(row=len(fields), column=1, padx=10, pady=5)

    run_button = tk.Button(
        root,
        text="Chạy Mô phỏng",
        command=lambda: run_simulation_from_gui(entries, tmax_entry, root),
    )
    run_button.grid(row=len(fields) + 1, columnspan=2, pady=10)

    tk.Label(
        root, text="LƯU Ý: Tính toán C++ dùng Euler đơn giản (kém ổn định).", fg="red"
    ).grid(row=len(fields) + 2, columnspan=2, pady=5)

    root.mainloop()


# ----------------------------------------------------------------------
# --- BẮT ĐẦU CHƯƠNG TRÌNH ---
# ----------------------------------------------------------------------
if __name__ == "__main__":
    create_gui()
