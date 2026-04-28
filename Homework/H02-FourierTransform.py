# type: ignore
import matplotlib.pyplot as plt
import numpy as np

# 设置字体和图像大小
plt.rcParams["font.size"] = 12
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# --- 原函数 f(x) ---
x = np.linspace(-6, 6, 500)
f = np.where(np.abs(x) <= 4, 10, 0)

axes[0].plot(x, f, "b-", linewidth=2)
axes[0].set_title(r"$f(x)$")
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(-2, 12)
axes[0].axhline(0, color="black", linewidth=0.5)
axes[0].axvline(0, color="black", linewidth=0.5)

# --- 傅里叶变换 F(ω) ---
omega = np.linspace(-10, 10, 1000)
# 避免除零，手动处理 ω=0 处的值
F = np.zeros_like(omega)
nonzero = omega != 0
F[nonzero] = 20 * np.sin(4 * omega[nonzero]) / omega[nonzero]
F[~nonzero] = 80  # ω=0 处的极限值

axes[1].plot(omega, F, "r-", linewidth=2, label=r"$F(\omega)$")
axes[1].plot(omega, np.abs(F), "g--", linewidth=1.5, alpha=0.7, label=r"$|F(\omega)|$")
axes[1].set_title(r"Fourier Transform $F(\omega)$")
axes[1].set_xlabel(r"$\omega$")
axes[1].set_ylabel(r"$F(\omega)$")
axes[1].grid(True, alpha=0.3)
axes[1].axhline(0, color="black", linewidth=0.5)
axes[1].axvline(0, color="black", linewidth=0.5)
axes[1].legend()
axes[1].set_xlim(-10, 10)

plt.tight_layout()
plt.show()
