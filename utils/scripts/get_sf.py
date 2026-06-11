import sys
import wave
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def get_sample_rate(wav_path: Path) -> int:
    with wave.open(str(wav_path)) as f:
        return f.getframerate()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        wav_files = [Path(sys.argv[1])]
    else:
        wav_files = sorted(DATA_DIR.rglob("*.wav"))

    if not wav_files:
        print(f"No se encontraron archivos .wav en {DATA_DIR}")
    else:
        for path in wav_files:
            sr = get_sample_rate(path)
            print(f"{path}: {sr} Hz")
