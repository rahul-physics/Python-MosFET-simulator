from model import GFETSimulatorAmbipolar
# Initialize the simulator
gfet = GFETSimulatorAmbipolar(
    channel_length=1e-6,   # 1 micron
    channel_width=10e-6,   # 10 micron
    tox=300e-9,            # 300 nm
    mobility=0.1,          # 0.1 m^2/Vs
    intrinsic_carrier_density=1e16,  # 1e16 carriers/m^2
    v_dirac=0.2            # Dirac point at 0.2 V
)

# Perform sweep
df_transfer = gfet.sweep(Vgs_range=(-1, 1), Vds_range=(0.1, 0.1), sweep_type='linear', num_points=100)
df_output = gfet.sweep(Vgs_range=(0.5, 0.05), Vds_range=(0, 1), sweep_type='linear', num_points=100)

# Plot and save transfer and output characteristics
gfet.plot_transfer(df_transfer, fixed_Vds=0.1)
gfet.plot_output(df_output, fixed_Vgs=0.5)

# Export the simulation results to CSV
gfet.export_to_csv(df_transfer, 'gfet_transfer_data.csv')
gfet.export_to_csv(df_output, 'gfet_output_data.csv')
