import wave
import struct
import math
import os

def generate_sine_wave(frequency, duration, amplitude=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    wave_data = []
    for i in range(n_samples):
        t = float(i) / sample_rate
        wave_data.append(amplitude * math.sin(2 * math.pi * frequency * t))
    return wave_data

def save_wave_file(filename, wave_data, sample_rate=44100):
    with wave.open(filename, 'w') as wave_file:
        n_channels = 1
        sample_width = 2
        wave_file.setnchannels(n_channels)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(sample_rate)
        
        # Convert to 16-bit integers
        scaled = [int(sample * 32767) for sample in wave_data]
        wave_file.writeframes(struct.pack('h' * len(scaled), *scaled))

def create_move_sound():
    # Short high-pitched beep
    return generate_sine_wave(880, 0.05)  # A5 note, 50ms

def create_rotate_sound():
    # Medium-pitched sweep
    wave_data = []
    for i in range(int(44100 * 0.1)):  # 100ms
        t = float(i) / 44100
        freq = 440 + 220 * t  # Sweep from 440Hz to 660Hz
        wave_data.append(0.5 * math.sin(2 * math.pi * freq * t))
    return wave_data

def create_drop_sound():
    # Low thud
    return generate_sine_wave(220, 0.15, amplitude=0.7)  # A3 note, 150ms

def create_clear_sound():
    # Success sound (ascending notes)
    wave_data = []
    frequencies = [440, 554, 659, 880]  # A4, C#5, E5, A5
    for freq in frequencies:
        wave_data.extend(generate_sine_wave(freq, 0.1))
    return wave_data

def create_gameover_sound():
    # Descending notes
    wave_data = []
    frequencies = [440, 392, 349, 330]  # A4, G4, F4, E4
    for freq in frequencies:
        wave_data.extend(generate_sine_wave(freq, 0.15, amplitude=0.6))
    return wave_data

def main():
    # Create sounds directory if it doesn't exist
    sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Generate and save all sound effects
    sounds = {
        'move.wav': create_move_sound(),
        'rotate.wav': create_rotate_sound(),
        'drop.wav': create_drop_sound(),
        'clear.wav': create_clear_sound(),
        'gameover.wav': create_gameover_sound()
    }
    
    for filename, wave_data in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        save_wave_file(filepath, wave_data)
        print(f"Generated {filename}")

if __name__ == '__main__':
    main() 