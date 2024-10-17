import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Parameters
num_bits = int(1e6)  # Number of bits
energy_per_bit = 1   # Energy per bit (Eb)
snr_db_range = np.arange(1, 21)  # SNR range in dB
snr_linear = 10 ** (snr_db_range / 10)  # SNR in linear scale

# Initialize arrays to store results
theoretical_ber = np.zeros(len(snr_db_range))
simulated_ber = np.zeros(len(snr_db_range))

# Q-function definition
def q_function(x):
    return 0.5 * erfc(x / np.sqrt(2))

# Loop over each SNR value
for idx, snr_db in enumerate(snr_db_range):
    noise_power = energy_per_bit / snr_linear[idx]
    noise_std_dev = np.sqrt(noise_power / 2)

    # Generate random bits (0 or 1)
    transmitted_bits = np.random.randint(0, 2, num_bits)
    transmitted_symbols = 2 * transmitted_bits - 1  # BPSK modulation

    # Add noise
    noise = noise_std_dev * np.random.randn(num_bits)
    received_signal = transmitted_symbols + noise

    # Decision: received > 0 means 1, else 0
    received_bits = received_signal > 0
    bit_errors = np.sum(transmitted_bits != received_bits)
    simulated_ber[idx] = bit_errors / num_bits

    # Minimum measurable BER to avoid log(0)
    if simulated_ber[idx] == 0:
        simulated_ber[idx] = 1 / num_bits

    # Theoretical BER calculation
    theoretical_ber[idx] = q_function(np.sqrt(2 * snr_linear[idx]))

    # Set BER to a minimum value for small numbers
    if theoretical_ber[idx] < 1e-6:
        theoretical_ber[idx] = 1e-6
        simulated_ber[idx] = 1e-6

# Print the results to the console
print('SNR(dB)   Simulated BER    Theoretical BER')
for idx in range(len(snr_db_range)):
    print(f'{snr_db_range[idx]:6.2f} {simulated_ber[idx]:14.10f} {theoretical_ber[idx]:18.10f}')

# Plot the results
plt.figure()
plt.semilogy(snr_db_range, theoretical_ber, 'b-o', markersize=6, linewidth=1.5, label='Theoretical BER')
plt.semilogy(snr_db_range, simulated_ber, 'r-*', markersize=6, linewidth=1.5, label='Simulated BER')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.title('BER vs SNR for BPSK Modulation')
plt.legend()
plt.grid(True)
plt.show()
