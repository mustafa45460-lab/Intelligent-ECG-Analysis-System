import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# 1. Load the simulated ECG data
file_path = "../data/ecg_sample.txt"
raw_data = []
with open(file_path, "r") as file:
    for line in file:
        raw_data.append(float(line.strip()))
raw_data = np.array(raw_data)

# 2. Introduce artificial high-frequency noise
np.random.seed(42)
noise = np.random.normal(0, 0.4, len(raw_data))
noisy_ecg = raw_data + noise

# 3. Apply the Digital Lowpass Butterworth Filter
fs = 100.0       # Sampling frequency (100 Hz)
cutoff = 15.0    # Cutoff frequency (15 Hz)
nyq = 0.5 * fs
normal_cutoff = cutoff / nyq
b, a = butter(4, normal_cutoff, btype='low', analog=False)
filtered_ecg = lfilter(b, a, noisy_ecg)

# 4. Intelligent Peak Detection Algorithm on the Cleaned Signal
# We set a threshold of 1.2V to capture peaks from the filtered data safely
threshold = 1.2
peaks_x = []
peaks_y = []

for index, voltage in enumerate(filtered_ecg):
    if voltage > threshold:
        # Check if it is the local maximum within a window of 10 samples
        window_start = max(0, index - 5)
        window_end = min(len(filtered_ecg), index + 5)
        if voltage == max(filtered_ecg[window_start:window_end]):
            if index not in peaks_x:
                peaks_x.append(index)
                peaks_y.append(voltage)

# 5. Calculate Heart Rate (BPM)
# The signal spans 10 seconds, so multiplying by 6 yields beats per minute
heart_rate = len(peaks_x) * 6
print(f"Calculated Heart Rate from Clean Signal: {heart_rate} BPM")

# 6. Plot and compare with peak markers
plt.figure(figsize=(12, 6))

# Subplot 1: Noisy Raw Signal
plt.subplot(2, 1, 1)
plt.plot(noisy_ecg, color='orange', label="Noisy ECG (Raw Signal)")
plt.title("Intelligent ECG Processing and Decision Support System")
plt.ylabel("Voltage")
plt.grid(True)
plt.legend()

# Subplot 2: Filtered Signal with Detected R-Peaks
plt.subplot(2, 1, 2)
plt.plot(filtered_ecg, color='green', label="Filtered ECG (Clean Signal)")
plt.scatter(peaks_x, peaks_y, color='red', marker='v', s=100, label=f"Detected Peaks ({heart_rate} BPM)")
plt.xlabel("Sample Index")
plt.ylabel("Voltage")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()