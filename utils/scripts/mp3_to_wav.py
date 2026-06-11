import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def convert(src: Path, dst: Path | None = None) -> Path:
    if dst is None:
        dst = src.with_suffix(".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), str(dst)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return dst


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        src = Path(sys.argv[1])
        dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else None
        out = convert(src, dst)
        print(f"Guardado en: {out}")
    else:
        mp3_files = sorted(DATA_DIR.rglob("*.mp3"))
        if not mp3_files:
            print(f"No se encontraron archivos .mp3 en {DATA_DIR}")
        else:
            for path in mp3_files:
                out = convert(path)
                print(f"{path.name} -> {out.name}")
