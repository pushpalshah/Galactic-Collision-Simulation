# Galactic-Collision-Simulation
This project is a high-fidelity Restricted N-Body Simulation that demonstrates the complex gravitational dynamics involved when two spiral galaxies collide. It uses Python to visualize the formation of tidal tails, bridges, and the eventual merger of galactic nuclei.
1. Theoretical ExplanationThe Restricted N-Body ProblemSimulating every star's gravity on every other star is computationally expensive $(O(N^2))$. This simulation uses the Restricted N-Body method:
      1. Primaries: The two galactic cores (simulating the bulge and dark matter halo) contain the system's mass.
      2. Test Particles: The stars are "massless" tracers that respond to the gravity of the cores but do not influence each other. This allows for smooth, real-         time performance.The Plummer PotentialTo avoid "numerical singularities" (infinite force at zero distance), we utilize the Plummer Potential instead of              standard point-mass gravity. This models the core as a spherical cluster of mass:
```math
\phi(r) = -\frac{G M}{\sqrt{r^2 + a^2}}\
```
Where a is the softening length. This ensures that stars passing through the center of a galaxy aren't "slingshotted" at impossible speeds.  
Dynamical Friction  
Unlike simple orbital models, these galaxies actually merge. This is achieved by simulating Dynamical Friction—a gravitational "drag" that occurs as massive        bodies move through a field of matter, causing their orbits to decay inward.  
2. Algorithm Logic  
  1. Initialization: * Set gravitational constant ($G$), mass ($M$), and softening length ($a$).  
          -  Generate two rotating disks using log-normal distribution (denser stars at the center).  
  2. Physics Integration (The Loop):  
          -  Core Dynamics: Calculate the mutual attraction between the two galactic centers, including a friction coefficient to simulate orbital decay.  
          -  Stellar Dynamics: For every star, calculate the vector sum of acceleration from both galactic cores.  
          -  Update: Apply Euler integration to update velocities and positions based on a small time step $\Delta t$.
  3. Phenomena Detection:  
          -  If Distance < Threshold:Trigger Tidal Bridge labels.
          -  If Time > Periapsis: Trigger Tidal Tail labels.
  4. Visual Rendering: Layered scatter plotting to create a "glow" effect on a black background.  
3. Simulation Flowchart
   ```mermaid 
   graph TD
    %% Global Setup
    Start((START)) --> Init[Initialize Simulation:<br/>G, M_Core, Softening, Friction]
    Init --> Gen[Generate Galaxy A & B:<br/>Log-Normal Distribution & Orbital Velocity]
    
    %% Main Physics Loop
    subgraph Physics Engine
    Gen --> Loop{Time Step < Total?}
    Loop -- Yes --> CoreGrav[Calculate Core-to-Core Gravity]
    CoreGrav --> Friction[Apply Dynamical Friction<br/>Orbital Decay]
    Friction --> StarGrav[Calculate Gravitational Pull from<br/>BOTH Cores for all N-Stars]
    StarGrav --> Update[Integrate DT:<br/>Update Positions & Velocities]
    end
    
    %% Labeling Logic
    subgraph Technical HUD
    Update --> CheckDist{Core Distance < 10?}
    CheckDist -- Yes --> LabelBridge[Label: TIDAL BRIDGE]
    CheckDist -- No --> CheckTail{Time > 800?}
    CheckTail -- Yes --> LabelTail[Label: TIDAL TAILS]
    CheckTail -- No --> Render
    LabelBridge --> Render[Render Frame:<br/>Scatter Plot + Glow Effect]
    LabelTail --> Render
    end
    
    %% Loop Back
    Render --> Loop
    Loop -- No --> End((END))

    style Physics Engine fill:#1a1a1a,stroke:#333,color:#fff
    style Technical HUD fill:#0d1117,stroke:#58a6ff,color:#fff
    style Start fill:#238636,color:#fff
    style End fill:#da3633,color:#fff
   ```
5. Key Astrophysical Phenomena Visualized
   - Tidal Stripping: The process where the outer stars are pulled away from their parent galaxy by the intruder's gravity.
   - Tidal Bridge: A stream of matter connecting the two galaxies during their closest approach (Periapsis).
   - Tidal Tails: Long, thin elongated regions of stars and gas that extend into intergalactic space.
   - Barycenter: The common center of mass around which the two galaxies orbit.
6. Usage
   - To run the simulation, ensure you have numpy and matplotlib installed:
   - pip install numpy matplotlib
   - Run the script to watch the "Cosmic Dance" in high-definition slow motion.
