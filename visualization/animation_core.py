# visualization/animation_core.py

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from .plot_final import draw_final_state


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
    num_frames,
    interval=50,
):
    """
    Tạo và chạy FuncAnimation.
    """

    def animate(i):
        # Cập nhật vị trí điểm electron
        point.set_data_3d([x_anim[i]], [y_anim[i]], [z_anim[i]])
        line_animated.set_data_3d(x_anim[: i + 1], y_anim[: i + 1], z_anim[: i + 1])

        # Xử lý khi Đạt FRAME CUỐI
        if i == num_frames - 1:
            ani.event_source.stop()
            # Gọi hàm vẽ trạng thái cuối cùng (Quỹ đạo và Điểm Đỏ)
            draw_final_state(
                ax, line_animated, line_final, point, x_anim, y_anim, z_anim
            )
            fig.canvas.draw_idle()

        return line_animated, point

    # Tắt Blit để tăng tính ổn định của việc vẽ lại các đối tượng
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=False)

    return ani
