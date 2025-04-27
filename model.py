import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class GFETSimulatorAmbipolar:
    def __init__(self, channel_length, channel_width, tox, mobility, intrinsic_carrier_density,
                 dielectric_const=3.9, v_dirac=0.0):
        self.L = channel_length  # meters
        self.W = channel_width   # meters
        self.tox = tox           # meters
        self.mu = mobility       # m^2/Vs
        self.n0 = intrinsic_carrier_density  # 1/m^2
        self.epsilon_0 = 8.854e-12  # F/m
        self.kappa = dielectric_const  # relative permittivity of oxide
        self.Cox = self.kappa * self.epsilon_0 / self.tox  # Oxide capacitance per unit area
        self.q = 1.602e-19  # Elementary charge
        self.Vdirac = v_dirac  # Dirac point voltage
        print(f"Initialized Ambipolar GFET with Cox={self.Cox:.2e} F/m^2, Vdirac={self.Vdirac} V")

    def carrier_density(self, Vgs):
        """
        Calculate total carrier density including both electrons and holes.
        """
        return np.sqrt(self.n0**2 + (self.Cox / self.q * (Vgs - self.Vdirac))**2)

    def drain_current(self, Vgs, Vds):
        """
        Ambipolar transport model for GFET.
        """
        n = self.carrier_density(Vgs)
        Ids = self.mu * (self.W / self.L) * self.q * n * Vds
        return Ids

    def sweep(self, Vgs_range, Vds_range, sweep_type='linear', num_points=100):
        """
        Simulate I-V or Transfer characteristics.
        """
        if sweep_type == 'linear':
            Vgs_values = np.linspace(*Vgs_range, num_points)
            Vds_values = np.linspace(*Vds_range, num_points)
        elif sweep_type == 'log':
            Vgs_values = np.logspace(np.log10(Vgs_range[0]), np.log10(Vgs_range[1]), num_points)
            Vds_values = np.logspace(np.log10(Vds_range[0]), np.log10(Vds_range[1]), num_points)
        elif sweep_type == 'dual-linear':
            Vgs_values = np.concatenate([
                np.linspace(Vgs_range[0], (Vgs_range[0]+Vgs_range[1])/2, num_points//2),
                np.linspace((Vgs_range[0]+Vgs_range[1])/2, Vgs_range[1], num_points//2)
            ])
            Vds_values = np.concatenate([
                np.linspace(Vds_range[0], (Vds_range[0]+Vds_range[1])/2, num_points//2),
                np.linspace((Vds_range[0]+Vds_range[1])/2, Vds_range[1], num_points//2)
            ])
        else:
            raise ValueError("Invalid sweep_type. Choose from 'linear', 'log', or 'dual-linear'.")

        results = []
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Ids = self.drain_current(Vgs, Vds)
                results.append((Vgs, Vds, Ids))
        
        df = pd.DataFrame(results, columns=['Vgs', 'Vds', 'Ids'])
        return df

    def load_custom_sweep(self, Vgs_csv_path, Vds_csv_path):
        
        Vgs_values = pd.read_csv(Vgs_csv_path).values.flatten()
        Vds_values = pd.read_csv(Vds_csv_path).values.flatten()
        results = []

        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Ids = self.drain_current(Vgs, Vds)
                results.append((Vgs, Vds, Ids))
        
        df = pd.DataFrame(results, columns=['Vgs', 'Vds', 'Ids'])
        return df

    def export_to_csv(self, df, filename):
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")

    def plot_transfer(self, df, fixed_Vds, save_dir='plots'):
        
        subset = df[np.isclose(df['Vds'], fixed_Vds, atol=1e-3)]
        plt.figure()
        plt.plot(subset['Vgs'], subset['Ids'], marker='o')
        plt.xlabel('Vgs (V)')
        plt.ylabel('Ids (A)')
        plt.title(f'Transfer Characteristics at Vds = {fixed_Vds} V')
        plt.grid(True)
        plt.autoscale(enable=True, axis='both', tight=True)
        plt.tight_layout()
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        filename = f"{save_dir}/transfer_Vds_{fixed_Vds:.2f}V.png"
        plt.savefig(filename, dpi=300)
        print(f"Transfer plot saved as {filename}")
        plt.show()

    def plot_output(self, df, fixed_Vgs, save_dir='plots'):
        """
        Plot Ids vs Vds for a fixed Vgs value with autoscaling.
        Saves the plot automatically as PNG.
        """
        subset = df[np.isclose(df['Vgs'], fixed_Vgs, atol=1e-3)]
        plt.figure()
        plt.plot(subset['Vds'], subset['Ids'], marker='s')
        plt.xlabel('Vds (V)')
        plt.ylabel('Ids (A)')
        plt.title(f'I-V Characteristics at Vgs = {fixed_Vgs} V')
        plt.grid(True)
        plt.autoscale(enable=True, axis='both', tight=True)
        plt.tight_layout()

        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        filename = f"{save_dir}/output_Vgs_{fixed_Vgs:.2f}V.png"
        plt.savefig(filename, dpi=300)
        print(f"Output plot saved as {filename}")
        plt.show()
