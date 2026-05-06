import numpy as np
import matplotlib.pyplot as plt

# 우리가 사용하는 소리 데이터 y(t)는
# 우리가 원하는 소리 x(t)와
# 노이즈 n(t)가 합성된 데이터다.
# y(t) = x(t) + n(t)

# SNR : 잡음 대비 신호의 세기
# 신호의 제곱 평균 / 노이즈의 제곱 평균 (전력)
# 위의 값은 범위가 넓기 때문에 10log를 씌워줘서 데시벨값으로 사용한다.

# 가장 대표적인 잡음 모델은 백색 가우시안 모델이다.
# 중심극한정리는 독립적이고 자잘한 수많은 요인들이 합쳐지면, 그 합은 결국 가우시안 분포(정규분포)가 된다는 이론

# 실제 세계에서 잡음의 원인은 굉장히 많기 때문에 
# 중심극한정리에 의해 잡음 모델을 가우시안으로 생각할 수 있다.

fs = 1000          # 샘플링 주파수 (Hz)
duration = 1.0     # 신호 길이 (초)
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# 1. 원신호 생성 (1Hz 사인파)
fo = 5            # 원본 신호 주파수 (Hz)
signal = np.sin(2 * np.pi * fo * t)

# 2. 목표 SNR 설정 (예: 10dB)
target_snr_db = 10
sig_p = np.mean(signal**2)      # 신호 전력
sig_p_db = 10 * np.log10(sig_p) # 신호 전력(dB)

# 3. 필요한 잡음 전력 계산
# SNR_dB = sig_p_db - noise_p_db 이므로
noise_p_db = sig_p_db - target_snr_db
noise_p = 10**(noise_p_db / 10)

# noise_p_db = 10 * np.log10(noise_p) 이므로
# noise_p는 위와 같이 계산된다.

# 4. 백색 가우시안 잡음 생성
noise = np.random.normal(0, np.sqrt(noise_p), len(signal))

# np.random.normal 함수는 파라미터 표준편차를 받는다.
# 그런데 우리가 계산한 것은 전력이고, 가우시안 분표에서는 평균이 0이므로 분산과 같다.
# 여기에 루트(sqrt)를 씌워줘서 표준편차를 구해 사용한다.

# 5. 합성
y = signal + noise

# --- 시각화 ---
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axes[0].plot(t, signal, color='steelblue', linewidth=1.5)
axes[0].set_title('Original Signal')
axes[0].set_ylabel('Amplitude')
axes[0].set_ylim(-2, 2)

axes[1].plot(t, noise, color='gray', linewidth=0.8, alpha=0.8)
axes[1].set_title('Noise (Gaussian White Noise)')
axes[1].set_ylabel('Amplitude')
axes[1].set_ylim(-2, 2)

axes[2].plot(t, y, color='tomato', linewidth=0.8)
axes[2].set_title('Noisy Signal')
axes[2].set_ylabel('Amplitude')
axes[2].set_ylim(-2, 2)
axes[2].set_xlabel('Time (s)')

plt.tight_layout()
plt.show()

# 결과 확인
actual_snr = 10 * np.log10(np.mean(signal**2) / np.mean(noise**2))
print(f"Target SNR: {target_snr_db}dB / Actual SNR: {actual_snr:.2f}dB")