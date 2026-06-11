import sys
from math import gcd
from pathlib import Path

import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def resample_wav(src: Path, target_sr: int, dst: Path | None = None) -> Path:
    if dst is None:
        dst = src.with_stem(f"{src.stem}_{target_sr}hz")

    orig_sr, data = wav.read(src)
    if orig_sr == target_sr:
        print(f"Ya tiene {target_sr} Hz, no se resampeló.")
        return src

    divisor = gcd(orig_sr, target_sr)
    up, down = target_sr // divisor, orig_sr // divisor

    # resample_poly opera sobre floats; restauramos el dtype original al guardar
    dtype = data.dtype
    resampled = signal.resample_poly(data.astype(np.float64), up, down, axis=0)
    resampled = np.clip(resampled, np.iinfo(dtype).min, np.iinfo(dtype).max).astype(dtype)

    wav.write(dst, target_sr, resampled)
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python resample.py <archivo.wav> <target_sr> [salida.wav]")
        print("     python resample.py data/signals/regular/audio.wav 16000")
        sys.exit(1)

    src = Path(sys.argv[1])
    target_sr = int(sys.argv[2])
    dst = Path(sys.argv[3]) if len(sys.argv) >= 4 else None

    out = resample_wav(src, target_sr, dst)
    print(f"Guardado en: {out}")
