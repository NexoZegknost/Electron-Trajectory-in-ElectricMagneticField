# gui_interface.py

import tkinter as tk
from tkinter import messagebox
import numpy as np


def create_input_fields(root):
    """Tạo các trường nhập liệu và nút bấm trong cửa sổ Tkinter."""
    fields = [
        ("Vị trí Ban đầu x0 (m):", "10", "r0_x"),
        ("Vị trí Ban đầu y0 (m):", "10", "r0_y"),
        ("Vị trí Ban đầu z0 (m):", "6", "r0_z"),
        ("Vận tốc Ban đầu vx (m/s):", "1e6", "v0_x"),
        ("Vận tốc Ban đầu vy (m/s):", "1e6", "v0_y"),
        ("Vận tốc Ban đầu vz (m/s):", "1e6", "v0_z"),
        ("E-trường Tĩnh Ex (V/m):", "6.0", "E_x"),
        ("E-trường Tĩnh Ey (V/m):", "8.0", "E_y"),
        ("E-trường Tĩnh Ez (V/m):", "10.0", "E_z"),
    ]

    entries = []

    for i, (label_text, default_value, _) in enumerate(fields):
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
    tmax_entry.insert(0, "1e-9")
    tmax_entry.grid(row=len(fields), column=1, padx=10, pady=5)

    return entries, tmax_entry


def get_input_values(entries, tmax_entry, root):
    """Lấy và chuyển đổi dữ liệu từ Tkinter entries thành các vector Numpy."""
    try:
        inputs = [float(entry.get()) for entry in entries]
        tmax = float(tmax_entry.get())

        r0 = np.array(inputs[0:3])
        v0 = np.array(inputs[3:6])
        E_static = np.array(inputs[6:9])

        root.destroy()

        return r0, v0, E_static, tmax

    except ValueError:
        messagebox.showerror(
            "Lỗi nhập liệu", "Vui lòng nhập giá trị số hợp lệ cho tất cả các trường."
        )
        return None, None, None, None
