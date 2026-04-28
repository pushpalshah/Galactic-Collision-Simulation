import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

# --- Scientific Configuration ---
G = 1.5            
M_CORE = 250.0     
PLUMMER_A = 3.0    # Softening length (prevents numerical "explosions")
FRICTION = 0.002   # Simulates Dark Matter drag (causes the merge)
N_STARS = 1500     
DT = 0.01          # Ultra-slow time step for cinematic motion
STEPS = 4000

def get_accel(p, target_p, mass):
    rel = target_p - p
    dist_sq = np.sum(rel**2, axis=-1)
    if dist_sq.ndim > 0: dist_sq = dist_sq[:, np.newaxis]
    # Plummer Potential Acceleration
    return G * mass * rel / (dist_sq + PLUMMER_A**2)**1.5

def init_galaxy(center, vel, color, name):
    pos, vels = [], []
    for _ in range(N_STARS):
        r = np.random.lognormal(mean=1.5, sigma=0.4) # Realistic star distribution
        if r > 15: r = 15
        theta = np.random.uniform(0, 2 * np.pi)
        
        p = np.array([center[0] + r * np.cos(theta), center[1] + r * np.sin(theta)])
        # Circular velocity + System velocity
        v_orb = np.sqrt((G * M_CORE * r**2) / (r**2 + PLUMMER_A**2)**1.5)
        v = np.array([-v_orb * np.sin(theta) + vel[0], v_orb * np.cos(theta) + vel[1]])
        
        pos.append(p)
        vels.append(v)
    return np.array(pos), np.array(vels), color, name

# --- Initial Setup ---
p1, v1 = np.array([-25.0, -2.0]), np.array([1.4, 0.2])
p2, v2 = np.array([25.0, 2.0]),  np.array([-1.4, -0.2])

stars1_p, stars1_v, col1, name1 = init_galaxy(p1, v1, '#00CCFF', 'Progenitor Alpha')
stars2_p, stars2_v, col2, name2 = init_galaxy(p2, v2, '#FF9900', 'Progenitor Beta')

# --- Enhanced Visualization ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 12))
fig.patch.set_facecolor('#050505')
ax.set_facecolor('#050505')

for t in range(STEPS):
    # 1. Core Physics (with Dynamical Friction)
    r_vec = p2 - p1
    dist = np.linalg.norm(r_vec)
    
    a1 = get_accel(p1, p2, M_CORE) - (v1 * FRICTION) # Adding drag
    a2 = get_accel(p2, p1, M_CORE) - (v2 * FRICTION)
    
    v1 += a1 * DT; p1 += v1 * DT
    v2 += a2 * DT; p2 += v2 * DT

    # 2. Star Physics (Dual-Potential Well)
    for p_s, v_s in [(stars1_p, stars1_v), (stars2_p, stars2_v)]:
        accel = get_accel(p_s, p1, M_CORE) + get_accel(p_s, p2, M_CORE)
        v_s += accel * DT
        p_s += v_s * DT

    # 3. Graphical HUD and Labeling
    if t % 15 == 0:
        ax.clear()
        # Draw Stars with "Glow" (Layered scatter)
        ax.scatter(stars1_p[:,0], stars1_p[:,1], s=1.5, c=col1, alpha=0.3) # Outer Glow
        ax.scatter(stars1_p[:,0], stars1_p[:,1], s=0.3, c='white', alpha=0.8) # Star Core
        
        ax.scatter(stars2_p[:,0], stars2_p[:,1], s=1.5, c=col2, alpha=0.3)
        ax.scatter(stars2_p[:,0], stars2_p[:,1], s=0.3, c='white', alpha=0.8)

        # Core Labels
        ax.text(p1[0], p1[1]+2, "NUCLEUS A", color=col1, fontsize=8, ha='center', weight='bold')
        ax.text(p2[0], p2[1]+2, "NUCLEUS B", color=col2, fontsize=8, ha='center', weight='bold')

        # Technical Overlay
        ax.text(0.02, 0.96, f"SIMULATION CLOCK: {t*DT*100:.1f} Myr", transform=ax.transAxes, color='gray')
        ax.text(0.02, 0.93, f"BARYCENTER DISTANCE: {dist:.2f} kpc", transform=ax.transAxes, color='gray')
        
        # Phenomenon Detection
        if dist < 10:
            ax.text(0.5, 0.95, "EVENT: TIDAL DISRUPTION / PERIAPSIS", color='red', 
                    ha='center', transform=ax.transAxes, fontsize=12, weight='black')
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='white', alpha=0.2, ls='--')
            ax.text((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, "TIDAL BRIDGE", color='white', fontsize=7)
        elif t > 800:
            ax.text(0.5, 0.05, "PHENOMENON: TIDAL TAIL FORMATION", color='cyan', 
                    ha='center', transform=ax.transAxes, style='italic')

        ax.set_xlim(-60, 60); ax.set_ylim(-60, 60)
        ax.axis('off')
        plt.pause(0.001)

plt.show()
