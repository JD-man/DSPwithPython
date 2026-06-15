import numpy as np
import matplotlib.pyplot as plt

# 아날로그 신호를 디지털로 변환(ADC: Analog-to-Digital Conversion)하는 과정
# 1. 샘플링(Sampling): 시간축으로 연속 신호를 일정한 시간 간격마다 값을 읽어 이산 수열로 변환하는 작업
# 2. 양자화(Quantization): 아날로그 신호의 진폭을 유한한 디지털 레벨로 나누는 과정

# 일반적인 균일 양자화(Uniform Quantization)
# 신호가 표현될 수 있는 최대 범위를 [xmin,xmax]로 잡고 이를 2n개의 레벨로 나눈다.
# 비트 깊이(Bit-depth), 또는 양자화 비트 수(n)는 아날로그 신호의 진폭을 몇 개의 디지털 레벨로 나눌 것인지를 결정
# 비트 수(비트 깊이): n
# 레벨 수: L=2n
# 양자화 간격(step size): Δ= (xmax − xmin) / 2n

# 비트 깊이가 클수록 아날로그 신호의 진폭을 더 잘게 쪼개어 세밀하게 표현할 수 있으므로 
# 원본 신호에 더 가까워지만 비용이 많이 든다.

# 이런 과정을 거쳐서 무한한 정밀도의 아날로그 신호가 디지털화 되므로
# 디지털화된 진폭 수치는 아날로그와 오차가 발생할 수 밖에 없다.
# -> 양자화 오차 또는 양자화 잡음이라고 부름

# 비트 깊이에 따른 샘플링 및 양자화 오차 비교 코드

# 원본 신호 생성 (1kHz 사인파, 샘플링 44100Hz)
fs = 44100
t = np.linspace(0, 0.005, int(fs * 0.005), endpoint=False)
x = np.sin(2 * np.pi * 1000 * t)  # Xmax = 1, Xmin = -1

def quantize(signal, n_bits):
    """균일 양자화: n_bits 비트로 양자화"""
    levels = 2 ** n_bits
    delta = 2.0 / levels  # Xmax - Xmin = 2

    # 양자화시 진폭을 제한된 단계로 반올림(또는 버림)하여 할당
    # xq[n] = Δ⋅round(x[n] / Δ)
    x_q = delta * np.round(signal / delta) 
    # 클리핑: 범위 초과 방지
    x_q = np.clip(x_q, -1.0, 1.0 - delta)
    return x_q

bit_depths = [2, 4, 8, 16]

fig, axes = plt.subplots(len(bit_depths), 2, figsize=(14, 10))
fig.suptitle('비트 깊이별 양자화 오차 비교', fontsize=14)

for i, n in enumerate(bit_depths):
    x_q = quantize(x, n)
    error = x_q - x # e[n] = xq[n] − x[n]

    axes[i, 0].plot(t * 1000, x, 'b-', alpha=0.5, label='원본', linewidth=1)
    axes[i, 0].step(t * 1000, x_q, 'r-', alpha=0.8, label=f'{n}-bit 양자화', linewidth=1)
    axes[i, 0].set_title(f'{n}-bit: {2**n}개 레벨, Δ = {2/2**n:.4f}')
    axes[i, 0].legend(fontsize=8)
    axes[i, 0].set_ylabel('진폭')

    axes[i, 1].plot(t * 1000, error, 'g-', linewidth=0.8)
    axes[i, 1].axhline(2/(2**(n+1)), color='r', linestyle='--', alpha=0.5, label=f'+Δ/2 = {1/2**n:.4f}')
    axes[i, 1].axhline(-2/(2**(n+1)), color='r', linestyle='--', alpha=0.5, label=f'-Δ/2')
    axes[i, 1].set_title(f'{n}-bit 양자화 오차')
    axes[i, 1].legend(fontsize=8)
    axes[i, 1].set_ylabel('오차')

for ax in axes[-1]:
    ax.set_xlabel('시간 (ms)')

plt.tight_layout()
plt.show()

# 결과 : bit_depths([2, 4, 8, 16])가 16으로 갈수록 정밀해짐.
# 변환된 디지털 신호 파형을 확대해 보면 부드러운 곡선이 아니라 층이 지는 계단 현상(Staircase effect)을 띠게 된다.
# 비트 깊이가 낮을수록 이 계단 현상이 두드러 진다.

# 양자화 오차는 ±Δ/2 범위에 균일하게 분포한다고 가정
# 균일 양자화(Uniform Quantization)의 핵심 가정이며, 이 가정 위에서 SQNR 공식이 유도된다.




