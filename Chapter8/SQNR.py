# SQNR (신호 대 양자화 잡음비): 
# "진짜 살리고 싶은 내 목소리나 기타 소리가 이 양자화 잡음보다 얼마나 더 큰가?"를 나타내는 척도
# 이 값이 클수록 잡음이 안 들리는 깨끗한 음질이라는 뜻

# SQNR = 10 * log10 ⁡* (Psignal / Pnoise) , P는 전력
# 전력은 각 신호의 제곱평균으로 구한다

# 신호의 경우 진폭 A인 정현파라고 하면
# 신호값인 Asin(wx)를 제곱 후 반각 공식을 사용 cos 부분은 평균이 0이므로 사라져
# 상수 부분인 A^2 / 2만 남는다.

# 양자화 잡음의 경우
# 균일분포로 가정했으므로 전력은 분산과 같다. (분산 = 오차의 제곱 * 확률)
# 잡음의 제곱에 확률밀도함수인 1 / Δ를 곱한 후 (균일분포이므로 그래프의 너비가 1이 되기 위해선 높이가 1 / Δ)
# 잡음의 범위인 ±Δ/2 범위에 적분을 한다.
# 적분의 결과로 Δ^2 / 12가 나온다.

# 이를 가지고 SQNR의 식에 대입하면
# 6.02 * n + 1.76 [dB]이 나온다.

# SQNR의 이론값과 측정값의 차이
import numpy as np
import matplotlib.pyplot as plt

# 원신호
fs = 44100
duration = 1.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
x = np.sin(2 * np.pi * 1000 * t)  # 풀스케일 정현파

# 양자화
def quantize(signal, n_bits):
    levels = 2 ** n_bits
    delta = 2.0 / levels
    x_q = delta * np.round(signal / delta)
    return np.clip(x_q, -1.0, 1.0 - delta)

# SQNR 계산, 이 함수에서는 실제로 제곱평균을 구해 전력을 계산한다.
def compute_sqnr(x, x_q):
    signal_power = np.mean(x ** 2)
    noise_power = np.mean((x_q - x) ** 2)
    return 10 * np.log10(signal_power / noise_power)

bit_depths = range(1, 17)
sqnr_measured = []
sqnr_theory = []

for n in bit_depths:
    x_q = quantize(x, n)
    # 실제 전력을 사용한 측정값
    sqnr_measured.append(compute_sqnr(x, x_q))
    # 위의 정리들에서 구한 이론값
    sqnr_theory.append(6.02 * n + 1.76)

plt.figure(figsize=(10, 5))
plt.plot(list(bit_depths), sqnr_theory, 'b--', label='이론값: 6.02n + 1.76 dB', linewidth=2)
plt.plot(list(bit_depths), sqnr_measured, 'ro-', label='측정값', markersize=6)
plt.xlabel('비트 깊이 (bits)')
plt.ylabel('SQNR (dB)')
plt.title('비트 깊이에 따른 SQNR: 이론값 vs 측정값')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(list(bit_depths))
plt.tight_layout()
plt.show()

# 비트깊이를 1비트 올릴 때마다, 깨끗한 소리의 마진(다이나믹 레인지)이 약 6dB씩 늘어난다
# 소리의 압력(진폭) 기준으로 2배 깨끗해지고, 전력(힘) 기준으로 4배 깨끗해진다는 뜻.

# 최근 AI 분야에서는 화질 분야와 정반대로 '의도적인 비트 축소'가 핵심 트렌드
# 거대 언어 모델(LLM)을 디바이스 메모리에 올리기 위해
# 기존 32-bit 부동소수점 가중치를 8-bit 심지어 2-bit 정수형으로 양자화.

# SQNR이 다소 희생되더라도, NPU에서의 추론 속도와 메모리 효율을 극대화하는 것이 실무적으로 훨씬 더 유리하기 때문
