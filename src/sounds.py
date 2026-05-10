import queue
import threading
import time

from src import constants as c

_sd = None
_np = None

try:
    import sounddevice as sd
    import numpy as np
    _sd = sd
    _np = np
except ImportError:
    pass


def _value_to_freq(value: int) -> float:
    ratio = (value - c.MIN_VAL) / max(c.MAX_VAL - c.MIN_VAL, 1)
    return 200.0 + ratio * 1800.0   # 200 Hz → 2000 Hz


class SoundPlayer:
    """
    Plays short sine-wave tones mapped to bar height.
    Uses a single persistent OutputStream to avoid per-tone stream
    creation, which crashes macOS PortAudio/AUHAL.
    Silent if sounddevice is not installed.
    """

    MIN_INTERVAL = 0.04
    RATE = 22050

    def __init__(self):
        self._last_play = 0.0
        self._lock = threading.Lock()
        self._queue: queue.Queue = queue.Queue(maxsize=4)
        if _sd is not None and _np is not None:
            t = threading.Thread(target=self._audio_loop, daemon=True)
            t.start()

    def value_to_freq(self, value: int) -> float:
        return _value_to_freq(value)

    def play(self, frequency: float, duration: float = 0.045, volume: float = 0.25):
        if _sd is None or _np is None:
            return
        now = time.monotonic()
        with self._lock:
            if now - self._last_play < self.MIN_INTERVAL:
                return
            self._last_play = now
        try:
            self._queue.put_nowait((frequency, duration, volume))
        except queue.Full:
            pass

    def _make_wave(self, frequency: float, duration: float, volume: float) -> "_np.ndarray":
        n = int(self.RATE * duration)
        t = _np.linspace(0, duration, n, endpoint=False)
        wave = (_np.sin(2 * _np.pi * frequency * t) * volume).astype(_np.float32)
        fade = max(1, int(self.RATE * 0.008))
        wave[:fade]  *= _np.linspace(0, 1, fade, dtype=_np.float32)
        wave[-fade:] *= _np.linspace(1, 0, fade, dtype=_np.float32)
        return wave.reshape(-1, 1)  # (n_samples, 1 channel)

    def _audio_loop(self):
        try:
            with _sd.OutputStream(samplerate=self.RATE, channels=1, dtype="float32") as stream:
                while True:
                    try:
                        freq, dur, vol = self._queue.get(timeout=1.0)
                    except queue.Empty:
                        continue
                    try:
                        stream.write(self._make_wave(freq, dur, vol))
                    except Exception:
                        pass
        except Exception:
            pass
