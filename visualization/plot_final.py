# visualization/plot_final.py


def draw_final_state(ax, line_animated, line_final, point, x_anim, y_anim, z_anim):
    """
    Đảm bảo quỹ đạo hoàn chỉnh và điểm cuối hiển thị sau khi animation dừng.
    """
    # Ẩn quỹ đạo tích lũy tạm thời (đường đang chạy)
    line_animated.set_visible(False)

    # Vẽ quỹ đạo hoàn chỉnh
    line_final.set_data_3d(x_anim, y_anim, z_anim)
    line_final.set_visible(True)

    # Cập nhật VỊ TRÍ CUỐI CÙNG của điểm electron lần cuối
    point.set_data_3d([x_anim[-1]], [y_anim[-1]], [z_anim[-1]])

    # Cập nhật legend
    line_final.set_label("Quỹ đạo Hoàn chỉnh")
    ax.legend()
