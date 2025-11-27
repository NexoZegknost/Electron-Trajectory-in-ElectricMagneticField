// physics.cpp
#include <cmath>
#include <vector>

// Định nghĩa các hằng số (phải giống Python)
const double m = 9.109e-31;  // Khối lượng electron
const double q = -1.602e-19; // Điện tích electron
const double B_z = 1.0;      // Thành phần B_z

// Cấu trúc để giữ các kết quả trả về
struct Result
{
    double x[1000];
    double y[1000];
    double z[1000];
};

// Hàm chính sẽ được Python gọi
// Sử dụng extern "C" để đảm bảo tên hàm không bị thay đổi (name mangling)
extern "C"
{

    // Hàm mô phỏng đơn giản (Ví dụ: 1000 bước tích phân Euler)
    // Trong môi trường thực tế, bạn sẽ dùng bộ giải RK45 C++
    void run_simulation(
        double r0_x, double r0_y, double r0_z,
        double v0_x, double v0_y, double v0_z,
        double E_static_x, double E_static_y, double E_static_z,
        double T_MAX,
        Result *output // Con trỏ đến cấu trúc kết quả
    )
    {
        int num_steps = 1000;
        double dt = T_MAX / num_steps;

        // Trạng thái hiện tại
        double x = r0_x, y = r0_y, z = r0_z;
        double vx = v0_x, vy = v0_y, vz = v0_z;

        for (int i = 0; i < num_steps; ++i)
        {

            // 1. Tính Lực Lorentz (F = qE + q(v x B))
            // F_x = q*E_x + q*(v_y * B_z - v_z * B_y)
            double F_x = q * E_static_x + q * (vy * B_z - vz * 0.0);

            // F_y = q*E_y + q*(v_z * B_x - v_x * B_z)
            double F_y = q * E_static_y + q * (vz * 0.0 - vx * B_z);

            // F_z = q*E_z + q*(v_x * B_y - v_y * B_x)
            double F_z = q * E_static_z + q * (vx * 0.0 - vy * 0.0);

            // 2. Tính Gia tốc (a = F/m)
            double ax = F_x / m;
            double ay = F_y / m;
            double az = F_z / m;

            // 3. Tích phân Euler (Đơn giản hóa thay vì RK45)
            // Cập nhật Vận tốc
            vx += ax * dt;
            vy += ay * dt;
            vz += az * dt;

            // Cập nhật Vị trí
            x += vx * dt;
            y += vy * dt;
            z += vz * dt;

            // 4. Lưu kết quả
            output->x[i] = x;
            output->y[i] = y;
            output->z[i] = z;
        }
    }
}