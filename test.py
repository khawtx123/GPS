import numpy as np
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(42)

# Generate time points
t = np.linspace(0, 10, 500)

# Generate clean sensor data (sine wave)
clean_data = np.sin(t)

# Generate noise
noise = np.random.normal(0, 0.4, t.shape)
noise2 = np.random.normal(0, 0.05, t.shape)
frequency = 60  # Frequency of the vibration noise
vibration_noise = 0.2 * np.sin(2 * np.pi * frequency * t)
vibration_noise2 = 0.2 * np.sin(2 * np.pi * 12 * t)

# Generate noisy sensor data by adding noise to clean data
noisy_data = clean_data + noise + vibration_noise
clean_data = clean_data + noise2 + vibration_noise2

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(t, clean_data, label='After Truss', linewidth=2)
plt.plot(t, noisy_data, label='Before Truss', linewidth=1, alpha=0.7)
plt.title('IMU Sensor Logger Data')
plt.xlabel('Time')
plt.ylabel('Sensor Value')
plt.legend()
plt.grid(True)
plt.show()
