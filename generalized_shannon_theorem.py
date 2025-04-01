import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# from scipy.io.wavfile import write
# import io

# Title of the application
st.title("The Generalized Shannon Theorem")

# Intro
st.markdown('''Sampling a narrowband signal with sampling frequency $F_s$ lower 
            than twice the maximum frequency of the signal does not always lead
	    to aliasing.\\
            In this example, you can adjust the sampling frequency to see how 
            it affects the spectral content of the sampled signal (in red). 
            The original signal (in blue) is a narrowband signal with 
            central frequency $F_0=1000 Hz$ and bandwidth $B=200 Hz$. \\
            Find which sampling frequencies are acceptable, and why.
            ''') 

# Choose the sampling frequency
sampling_rate = st.slider("Sampling frequency $F_s$ (Hz)", 300, 4000, 4000)

# Generate the narrowband signal
duration = 0.1 
center_frequency =1000 
bandwidth = 200 
pseudo_sampling_rate=4000   # Chosen high enough to avoid aliasing
t = np.arange(-duration,duration,1/pseudo_sampling_rate)
signal = np.cos(2 * np.pi * center_frequency * t) * np.sinc(bandwidth * t) \
    + 0.01 * np.cos(2 * np.pi * (center_frequency+bandwidth/3) * t)

# Sampling the signal
ts = np.arange(-duration,duration,1/sampling_rate)
sampled_signal = np.cos(2 * np.pi * center_frequency * ts) * np.sinc(bandwidth * ts) \
    + 0.01 * np.cos(2 * np.pi * (center_frequency+bandwidth/3) * ts)

# Spectral analysis
fig_spec, ax_spec = plt.subplots(figsize=(10, 4),tight_layout=True)

# Compute Fourier Transform of original signal
frequencies = np.fft.fftfreq(len(t), 1/pseudo_sampling_rate)
original_spectrum = 1/pseudo_sampling_rate*np.abs(np.fft.fft(signal))
frequencies=np.fft.fftshift(frequencies)
original_spectrum=np.fft.fftshift(original_spectrum)

# Compute Fourier Transform of sampled signal
sampled_frequencies = np.fft.fftfreq(len(ts), 1/sampling_rate)
sampled_spectrum = 1/sampling_rate*np.abs(np.fft.fft(sampled_signal))
sampled_frequencies=np.fft.fftshift(sampled_frequencies)
sampled_spectrum=np.fft.fftshift(sampled_spectrum)

# Show spectral content
plt.xlim(-2000, 2000)
plt.ylim(0, 0.006)
ax_spec.plot(frequencies, original_spectrum, label="Original Spectrum", linewidth=4)
ax_spec.stem([-sampling_rate/2.0,sampling_rate/2.0], [0.006,0.006], 'g', 
             label="Nyquyst frequency $F_s/2$")
s_frequencies =[]
s_spectrum=[]
for i in range (-7, 7):
    s_frequencies = np.append(s_frequencies, sampled_frequencies+i*sampling_rate)
    s_spectrum = np.append(s_spectrum, sampled_spectrum)
ax_spec.plot(s_frequencies, s_spectrum, label="Sampled Spectrum", 
             linestyle='dashed', color="red")
ax_spec.set_title("Spectral View of Original and Sampled Signals")
ax_spec.set_xlabel("Frequency (Hz)")
ax_spec.set_ylabel("Magnitude")
ax_spec.legend()
ax_spec.grid()

st.pyplot(fig_spec)

# Display the original signal and the sampled signal in [-0.01, 0.01]
fig, ax = plt.subplots(figsize=(10, 4),tight_layout=True)

# Original signal
ts_short = np.arange(-0.01,0.01,1/20000)
signal_short = np.cos(2 * np.pi * center_frequency * ts_short) * np.sinc(bandwidth * ts_short) \
    + 0.01 * np.cos(2 * np.pi * (center_frequency+bandwidth/3) * ts_short)

ax.plot(ts_short, signal_short)
ax.set_title("Original and Sampled Signals")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()

# Sampled signal
t_short = np.arange(-0.01,0.01,1/sampling_rate)
sampled_signal_short = np.cos(2 * np.pi * center_frequency * t_short) * np.sinc(bandwidth * t_short) \
    + 0.01 * np.cos(2 * np.pi * (center_frequency+bandwidth/3) * t_short)

ax.stem(t_short, sampled_signal_short, linefmt='r-', markerfmt='ro')

st.pyplot(fig)

# Audio playback
st.markdown('''Original signal''')
st.audio(signal, sample_rate=pseudo_sampling_rate)
st.markdown('''Sampled signal''')
st.audio(sampled_signal, sample_rate=sampling_rate) 

# Explanation of the generalized Shannon theorem
with st.expander("Open for comments"):
    st.write("""In this example, aliasing occurs when $F_s$ lies in:""")
    st.latex('''[0,440] \cup [450,550] \cup [600,733] \cup [900,1100] 
             \cup [1800,2200]''')
    st.write("""
            The generalized Shannon theorem states that to avoid aliasing when 
            sampling a narrowband signal (with central frequency $F_0$ 
            and bandwidth $B$), the sampling frequency must obviously be at 
            least twice the bandwidth of the signal: """)
    st.latex('''F_s>=2B''')
    st.write("""  
          Yet, not all such frequencies are acceptable, given the possible overlap 
          between positive and negative spectral images.
          This excludes the following sampling frequencies: """)
    st.latex('''[(2F_0-B)/k, (2F_0+B)/k ],''')
    st.write(""" with $k$ integer but not 0. As a matter of fact, for $k$ odd,
          values of $F_s$ in these intervals put the Nyquist frequency inside 
          a spectral image; for $k$ even, they put the zero frequency inside a 
          spectral image. In both cases, this causes aliasing. \\
          In our example, this clearly leads to excluding $F_s$ from:""")
    st.latex('''[0,400] \cup [333,440] 
          \cup [450,550] \cup [600,733] \cup [900,1100] \cup [1800,2200]''')
    st.write("""
          So, in this example, the smallest posible sampling frequency is 440 Hz. \\
          Notice, by examining the spectral content of the sampled signal, and
          by listening to it, that using sampling frequencies $F_s<2(F_0+B/2)$ 
          leads to signals in the $[0,F_s/2]$ band that are different from the 
          original signal. However, since no aliasing occurs, it is still 
          possible to recover the original signal (by further digital upsampling 
          and band-pass filtering).\\
	  \\
          _NotaBene_: for convenience, the effect of the sampling frequency on the 
         magnitude of the sampled signal spectrum has been compensated for in the 
         plot. """) 
	
