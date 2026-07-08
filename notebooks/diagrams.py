
import matplotlib.pyplot as plt
import numpy as np


def diagram_1():
    fig, ax = plt.subplots()
    x = np.linspace(-1, 1, 100)

    ax.plot(x, np.sqrt(1 - x**2), color="blue")
    ax.plot(x, -np.sqrt(1 - x**2), color="blue")

    ax.plot([0, 1], [0, 0], color="red")
    ax.plot([1, 1], [0, 2], color="red")
    ax.plot([0, 1], [0, 2], color="red")
    ax.plot([1 / (5**0.5), 1], [2 / (5**0.5), 0], color="red")

    ax.plot(
        [0, 1, 1 / (5**0.5), 1],
        [0, 0, 2 / (5**0.5), 2],
        "ko",
        markersize=5,
    )

    ax.annotate("$r$", (0.5, 0), (0.5, 0.1), color="red", fontsize=12)
    ax.annotate(
        "$r$",
        (0.5 / (5**0.5), 1 / (5**0.5)),
        (0.5 / (5**0.5) - 0.1, 1 / (5**0.5) + 0.1),
        color="red",
        fontsize=12,
    )
    ax.annotate("$\\theta$", (0, 0), (0.125, 0.075), color="red", fontsize=12)
    ax.annotate(
        "$r \\: \\tan(\\theta)$", (1, 1), (1.1, 1), color="red", fontsize=12
    )

    ax.set(xlim=(-2, 2), ylim=(-2, 2))
    ax.axis("off")
    plt.show()


def diagram_2():
    fig, ax = plt.subplots()
    x = np.linspace(0, 2)
    ax.set(xlim=(0, 3), ylim=(0, 3))

    ax.plot([0, 2], [2, 0], color="black")
    ax.plot([0, 1], [0, 1], color="black")

    ax.plot([1], [1], "ko")
    ax.plot([0, 2], [2, 0], "ro")

    ax.annotate(r"$\theta$", (0, 0), (0.15, 0.05), fontsize=12)
    ax.annotate(r"$\frac{\pi}{2}$", (1, 1), (0.975, 0.8), fontsize=12)
    ax.annotate(r"$L_0$", (1, 1), (1.1, 1.1), fontsize=12)

    ax.annotate(r"$L_1$", (0, 2), (0.1, 2.1), fontsize=12, color="red")
    ax.annotate(r"$L_1$", (0, 1), (2.1, 0.1), fontsize=12, color="red")

    ax.annotate(r"$a$", (1, 0), (0.95, 0.1), color="gray", fontsize=12)
    ax.annotate(r"$b$", (0, 1), (0.1, 0.95), color="gray", fontsize=12)
    ax.annotate(r"$h$", (0.5, 0.5), (0.45, 0.6), color="gray", fontsize=12)
    ax.annotate(r"$c$", (1.5, 0.5), (1.45, 0.6), color="gray", fontsize=12)
    ax.annotate(r"$d$", (0.5, 1.5), (0.45, 1.6), color="gray", fontsize=12)

    plt.show()


def diagram_3():
    fig, ax = plt.subplots()
    x_vals = np.linspace(-1, 1, 100)
    x2 = np.linspace(-2, 2, 100)
    x3 = np.linspace(-4, 4, 100)

    ax.plot(x_vals, np.sqrt(1 - x_vals**2), color="black")
    ax.plot(x_vals, -np.sqrt(1 - x_vals**2), color="black")

    ax.plot(x2, np.sqrt(4 - x2**2) + 1, color="grey")
    ax.plot(x2, -np.sqrt(4 - x2**2) + 1, color="grey")

    ax.plot(x3, np.sqrt(16 - x3**2) + 3, color="grey")
    ax.plot(x3, -np.sqrt(16 - x3**2) + 3, color="grey")

    ax.plot(0, -1, "ko")
    ax.annotate("Observer", (0, 0), (-0.5, -1.5))

    ax.plot([0, 0], [-1, 1], color="red", linestyle="dashed")
    ax.annotate(
        r"$\frac{2}{\pi}$", (0, 0), (0.2, -0.2), fontsize=12, color="red"
    )

    ax.plot(0, 1, "ro")
    ax.annotate(r"$L_0$", (0, 1), (-0.1, 1.3), color="red")

    ax.plot([-2, 2], [1, 1], "mo")
    ax.annotate(r"$L_1$", (-2, 1), (-2.3, 1.3), color="magenta")
    ax.annotate(r"$L_1$", (2, 1), (2.1, 1.2), color="magenta")
    ax.plot([-2, 2], [1, 1], linestyle="dashed", color="magenta")

    ax.plot(0, 3, "o", markerfacecolor="none", color="yellow")

    ax.plot(x3, 3 - x3, linestyle="dashed", color="blue")
    ax.plot(x3, x3 + 3, linestyle="dashed", color="blue")

    xs = [2 * np.sqrt(2), 2 * np.sqrt(2), -2 * np.sqrt(2), -2 * np.sqrt(2)]
    ys = [
        3 + 2 * np.sqrt(2),
        3 - 2 * np.sqrt(2),
        3 + 2 * np.sqrt(2),
        3 - 2 * np.sqrt(2),
    ]

    ax.plot(xs, ys, "bo")
    for x_coord, y_coord in zip(xs, ys):
        ax.annotate(
            r"$L_2$",
            (x_coord, y_coord),
            (x_coord - 0.2, y_coord + 0.3),
            color="blue",
        )

    ax.set(xlim=(-5, 5), ylim=(-2, 8))
    ax.axis("off")
    plt.show()
