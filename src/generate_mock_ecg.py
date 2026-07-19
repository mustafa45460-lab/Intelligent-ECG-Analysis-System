import numpy as np

# 1. Generate time array (1000 points over 10 seconds)
times = np.linspace(0, 10, 1000)

# 2. Simulate basic heart rhythm using a modified sine wave
ecg_signal = np.sin(2 * np.pi * 1.2 * times) 

# 3. Add sharp R-peaks to simulate real heartbeat pulses
for i in range(len(ecg_signal)):
    if i % 150 == 0:  # Every 150 samples, add a strong pulse
        ecg_signal[i] += 2.5
    elif i % 150 == 20: # T-wave simulation
        ecg_signal[i] += 0.6

# 4. Save the generated signal to the data file
np.savetxt("../data/ecg_sample.txt", ecg_signal, fmt="%.4f")
print("Data file successfully updated with mock ECG signal!")