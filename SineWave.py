import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
# 샘플링 주파수 (1000 Hz) : 1초에 저장하는 샘플의 개수 (1000개)
fs = 1000.0

# 관찰 시간 (1 sec) : 관측 시간
duration = 1.0     

# 총 샘플 수 : 샘플링 주파수 * 관찰 시간
N = int(fs * duration)

# 신호 주파수 (10 Hz) : 만들려고하는 사인파의 주파수
f = 10.0                  

# 위상 (rad) : 만들려고하는 사인파의 위상. 파형이 어디에서 시작하는 가를 나타냄
phi = 0.0                 

# 진폭 : 신호의 크기
A = 1.0                   

# 1. 시간축 생성 (배열) : 샘플레이트가 1000이므로 dt = 1/1000
# endpoint가 False이므로 0부터 999까지 1000개의 시간값 배열
t = np.linspace(0, duration, N, endpoint=False)

# 2. 신호 생성 
# 사인파의 기본 형태 : 진폭 * sin(2pi * 신호 주파수 * 시간축(배열) + 위상)
sin_wave = A * np.sin(2 * np.pi * f * t + phi)

# 3. 시각화 (처음 200개만 stem으로)
plt.figure(figsize=(10, 4))
plt.stem(t[:200], sin_wave[:200], basefmt=' ')
plt.title(f'Digital Sine Wave: {f}Hz (fs={fs}Hz) - First 200 Samples')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. 결과 확인
print(f"생성된 샘플 수: {len(sin_wave)}")
print(f"신호 범위: [{np.min(sin_wave):.3f}, {np.max(sin_wave):.3f}]")

# 주파수가 10이므로 1초에 10번, 0.1초에 1번 반복하는 사인파
# 시각화를 처음 샘플 200개만 했고 샘플레이트는 1000이므로 시간상 0.2초
# 따라서 두번 반복하는 사인파가 생성된다.

# t = np.arange(0, duration, 1/fs)를 사용하지 않는 이유
# 예시로 fs가 3인 경우 이를 수천 번 더하다 보면 미세한 오차가 누적.
# 이로 인해 마지막 값 근처에서 샘플 개수가 999개가 되거나 1001개가 되는 등 N(샘플 수)이 예상과 달라질 위험.

# 실무 환경에서 신호 처리는 단순히 수식을 코드로 옮기는 과정이 아님
# Python 라이브러리 생태계의 의존성과 호환성을 얼마나 잘 관리하느냐의 싸움.