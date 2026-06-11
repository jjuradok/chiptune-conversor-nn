import sys
from pathlib import Path

import numpy as np
import scipy.io.wavfile as wavfile

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def to_mono(src: Path, dst: Path | None = None) -> Path:
    if dst is None:
        dst = src.with_stem(f"{src.stem}_mono")

    sr, data = wavfile.read(src)

    if data.ndim == 1:
        print(f"{src.name}: ya es mono, no se modificó.")
        return src

    dtype = data.dtype
    mono = data.mean(axis=1).astype(dtype)
    wavfile.write(dst, sr, mono)
    return dst


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        src = Path(sys.argv[1])
        dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else None
        out = to_mono(src, dst)
        print(f"Guardado en: {out}")
    else:
        wav_files = sorted(DATA_DIR.rglob("*.wav"))
        if not wav_files:
            print(f"No se encontraron archivos .wav en {DATA_DIR}")
        else:
            for path in wav_files:
                out = to_mono(path)
                if out != path:
                    print(f"{path.name} -> {out.name}")
