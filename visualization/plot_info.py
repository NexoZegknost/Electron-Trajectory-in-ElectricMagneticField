# visualization/plot_info.py

import numpy as np


# Hàm khởi tạo các đối tượng Text
def initialize_info_texts(ax):
    """
    Khởi tạo các đối tượng Text để hiển thị vị trí, vận tốc, gia tốc.
    Các đối tượng này được đặt ở góc DƯỚI BÊN PHẢI của đồ thị 3D.
    """

    # Định dạng chuỗi ban đầu
    initial_text = lambda label: f"{label}: (0.00e+00, 0.00e+00, 0.00e+00)"

    # --- ĐIỀU CHỈNH TỌA ĐỘ X CHO VỊ TRÍ PHÍA DƯỚI BÊN PHẢI ---
    X_POS = 0.3  # Gần mép phải
    Y_START = 0  # Bắt đầu từ dưới lên
    ALIGNMENT = "right"  # Căn lề phải

    # Text cho Gia tốc (a) - Đặt cao nhất trong nhóm dưới (y=0.15)
    text_a = ax.text2D(
        X_POS,
        Y_START,
        initial_text("Gia tốc a"),
        transform=ax.transAxes,
        color="darkred",
        fontsize=10,
        ha=ALIGNMENT,
    )

    # Text cho Vận tốc (v) - Đặt ở giữa (y=0.10)
    text_v = ax.text2D(
        X_POS,
        Y_START - 0.05,
        initial_text("Vận tốc v"),
        transform=ax.transAxes,
        color="darkblue",
        fontsize=10,
        ha=ALIGNMENT,
    )

    # Text cho Vị trí (r) - Đặt thấp nhất (y=0.05)
    text_r = ax.text2D(
        X_POS,
        Y_START - 0.10,
        initial_text("Vị trí r"),
        transform=ax.transAxes,
        color="black",
        fontsize=10,
        ha=ALIGNMENT,
    )

    # Trả về các đối tượng Text theo thứ tự r, v, a
    return text_r, text_v, text_a


# Hàm cập nhật các đối tượng Text (GIỮ NGUYÊN)
def update_info_texts(text_r, text_v, text_a, r_i, v_i, E_static, B, q, m):
    """
    Cập nhật các đối tượng Text với dữ liệu hiện tại (tại frame i).
    """

    # 1. Tính toán Gia tốc (a) dựa trên Định luật Lorentz: a = (q/m) * (E + v x B)
    v_cross_B = np.cross(v_i, B)
    lorentz_term = E_static + v_cross_B
    a_i = (q / m) * lorentz_term

    # 2. Hàm định dạng
    def format_vector(label, vector):
        # Định dạng từng thành phần theo ký hiệu khoa học (vd: 1.23e-07)
        return f"{label}: ({vector[0]:.2e}, {vector[1]:.2e}, {vector[2]:.2e})"

    # 3. Cập nhật nội dung Text (Thứ tự phải khớp với initialize: r, v, a)
    text_r.set_text(format_vector("Vị trí", r_i))
    text_v.set_text(format_vector("Vận tốc", v_i))
    text_a.set_text(format_vector("Gia tốc", a_i))

    return text_r, text_v, text_a
