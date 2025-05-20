import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from fem_baseline.fem_solver import solve_fisher_1d

# --- Résolution de l'équation ---
xs, ts, sol = solve_fisher_1d(scheme="cn")

# --- Préparation de la figure ---
fig, ax = plt.subplots()
line, = ax.plot(xs, sol[0])
ax.set_ylim(0, 1.2)
ax.set_xlim(xs[0], xs[-1])
ax.set_xlabel('x')
ax.set_ylabel('u(x,t)')
ax.set_title('Fisher-KPP: Évolution dans le temps')

# --- Fonction d'update pour chaque frame ---
def update(i):
    line.set_ydata(sol[i])
    ax.set_title(f"Fisher-KPP: t = {ts[i]:.3f}")
    return line,

# --- Animation ---
anim = FuncAnimation(fig, update, frames=len(ts), interval=30, blit=True)

# --- Export en GIF ---
anim.save("figures/fisher_kpp.gif", writer=PillowWriter(fps=30))
print("✅ Animation GIF sauvegardée dans figures/fisher_kpp.gif")
