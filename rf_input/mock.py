import numpy as np

def generate_iq_samples(fs=20e6, duration=0.05):
    """
    Génère un signal IQ simulé ressemblant à un signal OFDM.
    """

    num_samples = int(fs * duration)
    t = np.arange(num_samples) / fs

    # Signal complexe simulé
    signal = np.exp(1j * 2 * np.pi * 1e6 * t)

    # Bruit
    noise = 0.1 * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))

    return signal + noise
