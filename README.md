# A Python Program to Model GFET Characteristics

A Python-based tool to simulate Graphene Field-Effect Transistors (GFETs) with **ambipolar transport modeling**.  
Designed to help researchers experiment with GFET characteristics **without fabricating devices** — saving time, cost, and reducing the risk of damaging sensitive samples.

---
## ✨ Features

- Specify key physical parameters: channel dimensions, oxide thickness, carrier mobility, intrinsic carrier density, etc.
- Simulates both:
  - **Transfer characteristics** (Resistance Rds vs Gate voltage Vgs)
  - **Output characteristics** (Drain current Ids vs Drain voltage Vds)
- Supports:
  - Linear, dual-linear, and logarithmic voltage sweeps.
  - Custom sweep loading from CSV files.
- Autoscaled plotting with automatic saving as PNG files.
- Exports simulated data directly to CSV files.
- Models full **ambipolar transport** behavior around the Dirac point.
- Lightweight, fast, and fully open-source!


