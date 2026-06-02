import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 샘플링(Sampling)
# 아날로그 세계의 연속 신호를 디지털로 가져오는 과정

# 한글 폰트 설정 (macOS: AppleGothic, Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# ── 파라미터 설정 ──────────────────────────────────────────────

# 원신호 설정
f0 = 60.0          # 원신호 주파수(Hz)
duration = 0.1     # 0.1초만 관측(시각화용)

# 비교할 샘플링 주파수들
fs_list = [1000, 180, 120, 50]   # 충분히 큼 -> 경계 -> 부족

# 아날로그 신호처럼 보이게 하기 위한 5000개의 점으로 원신호 표시
t_dense = np.linspace(0, duration, 5000, endpoint=False)
x_dense = np.sin(2*np.pi*f0*t_dense)

fig, axes = plt.subplots(len(fs_list), 1, figsize=(12, 10), sharex=True)

for ax, fs in zip(axes, fs_list):
    # 샘플링 주파수를 이용한 원신호 샘플링
    t = np.arange(0, duration, 1/fs)
    x = np.sin(2*np.pi*f0*t)

    ax.plot(t_dense, x_dense, linewidth=2, alpha=0.5, label='원신호 (dense)')
    ax.stem(t, x, basefmt=' ', linefmt='C1-', markerfmt='C1o', label=f'Sampled (fs={fs}Hz)')

    # Nyquist 정리
    # 샘플링시 주파수는 원신호에 포함된 가장 높은 주파수의 2배 이상이어야 한다.
    # 이 코드에서의 조건 : fs >= 2 * f0

    # Nyquist Frequency
    # 샘플링 주파수가 fs일때 fs/2
    # 처리하는 신호 안의 이보다 높은 수치의 주파수 성분은 왜곡이 일어난다.
    
    # Aliasing
    # 샘플링시 나이퀴스트 주파수 조건을 만족하지 않으면 나타나는 현상
    # 고주파 성분이 저주파 쪽에 접혀서 겹쳐보이는 현상

    # 샘플링 주파수가 1000이 아닌 모든 경우에 실시
    if fs < fs_list[0]:
       # 앨리어싱 주파수·위상 계산
       
       # step 1: fs 기준으로 폴딩
       # 만약 샘플링이 50이라면 
       # 1초뒤 원신호가 원점으로 부터 10hz 만큼 더 간곳을 샘플링
       # 2초뒤 원신호가 이전점으로부터 10hz 만큼 더 간곳을 샘플링
       # 샘플링 점들은 1초마다 10hz 만큼 움직이므로 10hz의 신호가 나온다.
       
       # 이렇게 원신호 주파수를 샘플링 주파수의 주기로 나머지 연산해서 구한다.
       # fs가 180 이라면 60, 50이라면 10

       f_fold = f0 % fs 


       # step 2: 나이퀴스트(fs_low/2)를 초과하면 부호 반전
       # 나이퀴스트 주파수의 절반을 통과해 60% 부근이라고 하면
       # 앞으로 60%가 아닌 뒤로 40%로 간것으로 파악됨.
       # 뒤로가기 때문에 기함수인 성질에 의해 부호가 반전됨.
       # 이 코드의 샘플링 주파수에서는 이 케이스가 없어 else문만 탄다.

       if f_fold > fs /2 :
           f_alias = fs - f_fold
           alias_sign = -1
       else:
           f_alias = f_fold
           alias_sign = 1

       x_alias = alias_sign * np.sin(2 * np.pi * 50 * t_dense)
       ax.plot(t_dense, x_alias, 'C1--', linewidth=1.2, alpha=0.7, label=f'앨리어스파형({f_alias:.0f} Hz)')
        

    ax.set_title(f'f0={f0}Hz, fs={fs}Hz (Nyquist freq = {fs/2:.1f}Hz)')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend(loc='upper right')

axes[-1].set_xlabel('Time (s)')
plt.tight_layout()
plt.show()

# 결론적으로 나이퀴스트 조건에 따라서 원신호 주파수의 2배인 120hz보다 낮은 주파수로 샘플링하면
# 60hz의 신호와 낮은 주파수의 신호를 구별할 수 없다.

# 위의 코드에서 50hz의 샘플링의 경우 
# 샘플링된 점을 통해서는 
# 원신호 60hz 신호와 왜곡된 10hz 신호를 구별할 수 없다.
# 디지털쪽에서는 이 두 신호가 구별이 안되니 정보 손실이 발생한다.

# 입력단계에서의 문제
# 샘플링 장치의 샘플링 주파수의 절반보다 높은 주파수 소리의 경우
# 원본신호의 저주파 부분과 섞여 영구적인 신호 오염이 될 수 있다.

# 신호처리 단계에서의 문제
# 처리 결과로 고주파음이 많이 발생하는 신호로 변경될 경우
# 신호처리가 이루어지는 환경의 샘플링 주파수의 절반보다 높은 주파수는 폴딩이 된다.
# 이러면 일정 배수의 배음이 깨져서 불협화음이 생긴다.