# physics_engine.py

import ctypes
import numpy as np
from tkinter import messagebox

# --- Hằng số Vật lý ---
m = 9.109e-31
q = -1.602e-19
B = np.array([0.0, 0.0, 1.0])


# Định nghĩa cấu trúc Result C++ trong Python
class Result(ctypes.Structure):
    # Kích thước mảng phải khớp với num_steps (1000) trong code C++
    _fields_ = [
        ("x", ctypes.c_double * 1000),
        ("y", ctypes.c_double * 1000),
        ("z", ctypes.c_double * 1000),
    ]


# --- Tải Thư viện C++ ---
lib = None
try:
    # Thay đổi đường dẫn nếu ODE.dll không nằm cùng thư mục gốc
    lib = ctypes.CDLL("./engine/ODE.dll")

    lib.run_simulation.argtypes = [
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,  # r0
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,  # v0
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,  # E_static
        ctypes.c_double,  # T_MAX
        ctypes.POINTER(Result),  # Output pointer
    ]
    lib.run_simulation.restype = None

except OSError as e:
    # Lỗi này chỉ in ra console, lỗi hiển thị sẽ được xử lý trong main.py
    print(f"LỖI: Không thể tìm thấy hoặc tải thư viện C++ (ODE.dll/so): {e}")


# --- Hàm Chính Tính toán ---
def run_cpp_simulation(r0, v0, E_static, tmax):
    """
    Gọi hàm C++ để tính toán quỹ đạo electron và trả về mảng dữ liệu.
    """
    if lib is None:
        raise RuntimeError("Thư viện C++ (ODE.dll) chưa được tải thành công.")

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

    x = np.array(output_struct.x[:])
    y = np.array(output_struct.y[:])
    z = np.array(output_struct.z[:])

    # Kiểm tra tính phân kỳ của dữ liệu
    if np.any(np.isnan(x)) or np.any(np.isinf(x)) or np.any(np.isinf(y)):
        messagebox.showerror(
            "Lỗi Phân kỳ Tính toán",
            f"Dữ liệu quỹ đạo bị phân kỳ (NaN/Inf). Vui lòng giảm T_MAX.",
        )
        return None, None, None  # Trả về None nếu lỗi

    return x, y, z
