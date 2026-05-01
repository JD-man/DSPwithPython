import numpy as np
import matplotlib.pyplot as plt

# 설정
fs = 1000.0               
duration = 1.0            
N = int(fs * duration)
t = np.linspace(0, duration, N, endpoint=False)

# 신호 생성 (5Hz)
f = 5.0
# 사인파
sig_sin = np.sin(2 * np.pi * f * t)
# 코사인파
sig_cos = np.cos(2 * np.pi * f * t)

# 시각화
plt.figure(figsize=(10, 4))
plt.plot(t, sig_sin, label='Sine (5Hz)')
plt.plot(t, sig_cos, label='Cosine (5Hz)', linestyle='--')
plt.title('Sine vs Cosine Wave')
plt.legend()
plt.grid(True)
plt.show()

# 사인파와 코사인파는 90∘(π/2)의 위상차를 가진다
# 이는 직교 변조(Quadrature Modulation)와 복소 신호 처리 개념을 이해하는 데 중요한 기초

############################################################################################################

from scipy import signal

# 5Hz 구형파 (Square Wave) 생성
# scipy를 통해 생성한다. sin, cos는 numpy를 통해 생성
sig_square = signal.square(2 * np.pi * f * t)

plt.figure(figsize=(10, 4))
plt.plot(t, sig_square, color='red')
plt.title('Square Wave (5Hz)')
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.show()

# 구형파는 +1과 −1 사이를 급격히 오가는 불연속적인 특징을 가짐.
# 이러한 급격한 변화는 푸리에 급수 관점에서 무한개의 고조파(Harmonics)를 포함하고 있음을 의미

############################################################################################################

# 5Hz 톱니파 생성
sawtooth_wave = signal.sawtooth(2 * np.pi * f * t)

plt.figure(figsize=(10, 4))
plt.plot(t, sawtooth_wave, color='red')
plt.title('Sawtooth Wave (5Hz)')
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.show()

# 5Hz 삼각파 생성, 톱니파에서 width = 0.5가 추가됐다.
triangle_wave = signal.sawtooth(2 * np.pi * f * t, width=0.5)

plt.figure(figsize=(10, 4))
plt.plot(t, triangle_wave, color='red')
plt.title('Triangle Wave (5Hz)')
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.show()

# width : 한 주기 안에 peak가 0~1 사이 어디에 있는지 나타냄
# 톱니파에서 peak를 0.5 위치로 옮기면 삼각파가 됨.

############################################################################################################

# 신호 합성 (주파수가 5hz인 진폭 1의 사인파와 주파수가 50인 진폭 0.3의 사인파의 합성)
sig_5hz = np.sin(2 * np.pi * 5 * t)          
sig_50hz = 0.3 * np.sin(2 * np.pi * 50 * t)
combined_sig = sig_5hz + sig_50hz

plt.figure(figsize=(10, 4))
plt.plot(t, combined_sig)
plt.title('Combined Signal (5Hz + 50Hz)')
plt.grid(True)
plt.show()


# 5Hz의 큰 흐름(기저 성분) 위에 50Hz의 작은 떨림(노이즈 혹은 고주파 성분)이 올라탄 형태
# 푸리에 변환(FFT)을 통해 복잡한 이 파형을 거꾸로 "여기에는 5Hz와 50Hz 성분이 존재한다"는 것을 추론 가능
# 복잡한 신호들은 기본적으로는 기본 파형들의 조합으로 해석할 수 있다!

# 신호처리에서의 필터링이란, 복잡한 신호를 단순한 성분들로 분해한 뒤 
# 우리가 원하는 성분만 남기거나 원치 않는 성분(노이즈)을 제거하는 과정이라고 정의할 수 있다.