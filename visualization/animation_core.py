# visualization/animation_core.py

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from .plot_final import draw_final_state
from .plot_info import *


def create_animation_objects(ax, x_anim, y_anim, z_anim):
    """
    Khởi tạo các đối tượng Line và Point cho animation.
    """
    # line_animated: Đường màu xanh tạm thời (quỹ đạo tích lũy)
    (line_animated,) = ax.plot(
        x_anim[0:1],
        y_anim[0:1],
        z_anim[0:1],
        color="blue",
        label="Quỹ đạo đang đi",
        linewidth=1.5,
    )

    # point: Vị trí hiện tại/cuối cùng của electron (màu đỏ)
    (point,) = ax.plot(
        [x_anim[0]],
        [y_anim[0]],
        [z_anim[0]],
        marker="o",
        color="red",
        markersize=8,
        label="Electron",
    )

    # line_final: Đường màu xanh SẼ ĐƯỢC VẼ VĨNH VIỄN (ban đầu ẩn)
    (line_final,) = ax.plot([], [], [], color="blue", linewidth=1.5, visible=False)

    return line_animated, point, line_final


def run_animation(
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
    vz_anim,
    E_static,
    B,
    q,
    m,
    num_frames,
    interval=50,
):
    """
    Tạo và chạy FuncAnimation.
    """
    text_r, text_v, text_a = initialize_info_texts(ax)

    def animate(i):
        # Lấy vị trí và vận tốc hiện tại
        r_i = np.array([x_anim[i], y_anim[i], z_anim[i]])
        v_i = np.array([vx_anim[i], vy_anim[i], vz_anim[i]])

        # Cập nhật vị trí điểm electron
        point.set_data_3d([x_anim[i]], [y_anim[i]], [z_anim[i]])
        line_animated.set_data_3d(x_anim[: i + 1], y_anim[: i + 1], z_anim[: i + 1])

        point.set_data_3d([r_i[0]], [r_i[1]], [r_i[2]])
        line_animated.set_data_3d(x_anim[: i + 1], y_anim[: i + 1], z_anim[: i + 1])

        update_info_texts(text_r, text_v, text_a, r_i, v_i, E_static, B, q, m)

        # Xử lý khi Đạt FRAME CUỐI
        if i == num_frames - 1:
            ani.event_source.stop()
            draw_final_state(
                ax, line_animated, line_final, point, x_anim, y_anim, z_anim
            )
            fig.canvas.draw_idle()

        return line_animated, point, text_r, text_v, text_a

    # Tắt Blit để tăng tính ổn định của việc vẽ lại các đối tượng
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=False)

    return ani
