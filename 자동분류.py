from pathlib import Path
import shutil


DOWNLOAD_DIR = Path(r"C:\Users\student\Downloads")

EXTENSION_TO_FOLDER = {
    ".jpg": "images",
    ".jpeg": "images",
    ".csv": "data",
    ".xlsx": "data",
    ".txt": "docs",
    ".doc": "docs",
    ".pdf": "docs",
    ".zip": "archive",
}


def get_unique_path(destination: Path) -> Path:
    """같은 이름의 파일이 있으면 사용할 수 있는 새 경로를 반환합니다."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def organize_downloads() -> None:
    if not DOWNLOAD_DIR.is_dir():
        print(f"다운로드 폴더를 찾을 수 없습니다: {DOWNLOAD_DIR}")
        return

    for folder_name in set(EXTENSION_TO_FOLDER.values()):
        (DOWNLOAD_DIR / folder_name).mkdir(exist_ok=True)

    for source in DOWNLOAD_DIR.iterdir():
        if not source.is_file():
            continue

        folder_name = EXTENSION_TO_FOLDER.get(source.suffix.lower())
        if folder_name is None:
            continue

        destination_dir = DOWNLOAD_DIR / folder_name
        destination = get_unique_path(destination_dir / source.name)
        shutil.move(str(source), str(destination))
        print(f"이동 완료: {source.name} -> {destination_dir}")


if __name__ == "__main__":
    organize_downloads()