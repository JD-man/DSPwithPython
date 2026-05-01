import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. 간단한 사인파 생성
fs = 1000  # 샘플링 주파수 (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # 1초 길이
freq = 10  # 10Hz 사인파

sine_wave = np.sin(2 * np.pi * freq * t)

# 2. 시각화
plt.figure(figsize=(10, 4))
plt.plot(t[:200], sine_wave[:200])  # 처음 200개 샘플만 시각화
plt.title('10 Hz Sine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()

print("!!! NumPy, SciPy, Matplotlib 정상 작동 !!!")
print(f"NumPy 버전: {np.__version__}")