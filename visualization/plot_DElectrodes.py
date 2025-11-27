# visualization/plot_dees.py

import numpy as np


def plot_dees(ax, R_max, H, gap, color="orange", alpha=0.3):
    # ... (Phần 1. Định nghĩa các tham số hình học - GIỮ NGUYÊN) ...
    u = np.linspace(0, np.pi, 50)  # Góc từ 0 đến Pi (nửa hình tròn)
    v = np.linspace(0, R_max, 2)
    theta, r = np.meshgrid(u, v)
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    Z_top = np.full_like(X, H / 2)
    Z_bottom = np.full_like(X, -H / 2)

    # 2. Tạo Dee 1 (Phần dương của trục Y)

    # Vẽ Bề mặt trên và dưới của Dee 1
    ax.plot_surface(X, Y, Z_top, color=color, alpha=alpha, shade=False)
    ax.plot_surface(X, Y, Z_bottom, color=color, alpha=alpha, shade=False)

    # VẼ THÀNH BÊN CONG CHO DEE 1 (SỬA LỖI BROADCASTING)
    # Lưới: 50 góc (u) và 2 chiều cao (H/2, -H/2)

    # Tạo lưới cho thành bên (Side Wall)
    u_side = np.linspace(0, np.pi, 50)  # Góc
    z_side = np.array([-H / 2, H / 2])  # Chiều cao

    # r_max là bán kính cố định cho thành bên
    R_fixed = R_max

    # Tạo lưới tọa độ cho bề mặt đứng (X, Z) trên hình tròn bán kính R_fixed
    # Chúng ta muốn lặp lại R_fixed 2 lần (cho Zmin và Zmax) và lặp lại u_side 2 lần (cho Zmin và Zmax)

    # Tạo ma trận góc và chiều cao (2 x 50)
    Theta_wall, Z_wall = np.meshgrid(u_side, z_side)  # Shape (2, 50)

    # Tính tọa độ X, Y tại bán kính R_fixed
    X_wall = R_fixed * np.cos(Theta_wall)  # Shape (2, 50)
    Y_wall = R_fixed * np.sin(Theta_wall)  # Shape (2, 50)

    # Vẽ thành bên cong cho Dee 1
    ax.plot_surface(X_wall, Y_wall, Z_wall, color=color, alpha=alpha, shade=False)

    # 3. Tạo Dee 2 (Phần âm của trục Y)

    # Sử dụng góc từ Pi đến 2*Pi
    u2 = np.linspace(np.pi, 2 * np.pi, 50)
    theta2, r2 = np.meshgrid(u2, v)

    X2 = r2 * np.cos(theta2)
    Y2 = r2 * np.sin(theta2)

    # Vẽ Bề mặt trên và dưới của Dee 2
    ax.plot_surface(X2, Y2, Z_top, color=color, alpha=alpha, shade=False)
    ax.plot_surface(X2, Y2, Z_bottom, color=color, alpha=alpha, shade=False)

    # VẼ THÀNH BÊN CONG CHO DEE 2 (SỬA LỖI BROADCASTING)

    # Tạo ma trận góc và chiều cao (2 x 50) cho phần thứ 2
    Theta2_wall, Z2_wall = np.meshgrid(u2, z_side)  # Shape (2, 50)

    # Tính tọa độ X, Y tại bán kính R_fixed
    X2_wall = R_fixed * np.cos(Theta2_wall)  # Shape (2, 50)
    Y2_wall = R_fixed * np.sin(Theta2_wall)  # Shape (2, 50)

    # Vẽ thành bên cong cho Dee 2
    ax.plot_surface(X2_wall, Y2_wall, Z2_wall, color=color, alpha=alpha, shade=False)

    # 4. Vẽ khe hở (Gap)

    # ... (Logic vẽ khe hở - GIỮ NGUYÊN) ...
    x_gap = np.linspace(0, R_max, 2)
    z_gap = np.linspace(-H / 2, H / 2, 2)
    X_gap, Z_gap = np.meshgrid(x_gap, z_gap)
    Y_left = np.full_like(X_gap, -gap / 2)
    Y_right = np.full_like(X_gap, gap / 2)

    # Vẽ mặt phẳng cắt cho Dee 1 (bên trái khe hở)
    void_color = "lightblue"

    ax.plot_surface(X_gap, Y_left, Z_gap, color=void_color, alpha=0.5, shade=False)
    ax.plot_surface(-X_gap, Y_left, Z_gap, color=void_color, alpha=0.5, shade=False)

    # Vẽ mặt phẳng cắt cho Dee 2 (bên phải khe hở)
    ax.plot_surface(X_gap, Y_right, Z_gap, color=void_color, alpha=0.5, shade=False)
    ax.plot_surface(-X_gap, Y_right, Z_gap, color=void_color, alpha=0.5, shade=False)

    return [ax.get_children()[-1]]
