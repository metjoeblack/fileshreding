
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any
from humanize import naturalsize


def move_file_to_destination(current_dir, destination_dir):
    for file_path_obj in Path(current_dir).glob("*.txt"):
        new_path = Path(destination_dir) / "archive" / file_path_obj.name
        file_path_obj.replace(new_path)


def exercise_path_obj():
    print(Path.cwd())
    print(Path.home())
    my_path = Path("/user/shangguan/realpython/folder/test.txt")
    info = ("name", "stem", "suffix", "anchor", "parent")
    for item in info:
        print(f"{item} ===> {getattr(my_path, item)!r}")

    print(my_path.parent.parent)


def read_write_file():
    path_obj = Path(__file__).parent.joinpath("data", "test.md")
    with path_obj.open(mode="r", encoding="utf-8") as md_file:
        content = md_file.read()
        print(content)

    content = path_obj.read_text(encoding="utf-8", newline=" ")
    path_obj.write_text(content, encoding="utf-8", newline="\n")



def rename_file():
    txt_path = Path(__file__).parent.joinpath("data", "test.txt")
    print(txt_path)
    md_path = txt_path.with_suffix(".md")
    print(md_path)
    new_md_path = md_path.with_name("new.md")
    print(new_md_path)
    new_name_path = txt_path.with_stem("hello")
    print(new_name_path)

    # txt_path.replace(md_path)

def copy_file():
    source_path = Path(__file__).parent.joinpath("data", "test.txt")
    destination_path = source_path.with_stem("new_test")
    destination_path.write_bytes(source_path.read_bytes())


def move_delete_file():
    source_path = Path(__file__).parent.joinpath("data", "test.txt")
    destination_path = source_path.with_stem("new_test")

    try:
        with destination_path.open(mode="xb") as fp:
            fp.write(source_path.read_bytes())
    except FileExistsError:
        print(f"File {destination_path} already exists.")
    else:
        source_path.unlink()


def directory_tree(directory: Path) -> None:
    print(f"+ {directory}")
    for path in sorted(directory.rglob("*")):
        depth = len(path.relative_to(directory).parts)
        prefix = "F" if path.is_file() else "D"
        print(f"{" " * 4 * depth}+ [{prefix}]{path.name}")


def relative_parts():
    file_path = Path(r"G:\just_test\dire1\good.txt")
    print(file_path.parts)
    print(file_path.relative_to(Path(r"G:\just_test")).parts)


def get_most_recently_modified_file(directory: Path):
    time, file = max(
        (file.stat().st_mtime, file)
        for file in directory.rglob("*")
    )
    print(datetime.fromtimestamp(time), file)


def unique_path(directory: Path, name_pattern: str):
    counter = 0
    while True:
        counter += 1
        new_path = directory / name_pattern.format(counter)
        if not  new_path.exists():
            yield new_path


def scan_large_files(
    root_dir: str | Path,
    size_threshold: int = 10 * 1024 * 1024,
    days_old: int | None = None,
    exclude_dirs: set[str | Path] | None = None,
    output_file: Optional[str | Path] = None,
):
    root_path = Path(root_dir).expanduser().resolve()
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    exclude_dirs = exclude_dirs or set()
    cutoff_ts = (
        None if days_old is None else
        (datetime.now() - timedelta(days=days_old)).timestamp()
    )

    results: list[dict[str, Any]] = []
    for item in root_path.rglob("*"):
        if item.is_file():
            if any(
                    part in exclude_dirs
                    for part in item.relative_to(root_path).parts
            ):
                continue
            file_size, file_mtime = item.stat().st_size, item.stat().st_mtime
            if (
                file_size >= size_threshold
                and cutoff_ts is None
                or file_mtime < cutoff_ts
            ):
                modified_time = datetime.fromtimestamp(file_mtime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                results.append(
                    {
                        "path": item,
                        "size": naturalsize(file_size),
                        "modified": modified_time,
                    }
                )

    print(f"\nscan finished, {len(results)} large files found.")

    for idx, file in enumerate(results, start=1):
        print(
            f"{idx:>3}. {file.get('size')}:<10 "
            f"{file.get('modified')} {file.get('path')}"
        )

    if output_file is not None:
        output_path = Path(output_file).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wt", encoding="utf-8") as out_fp:
            out_fp.write("Large file scanning report\n")
            out_fp.write(f"Generating time: {datetime.now():%F %T}\n")
            out_fp.write(f"scanning root dir: {root_path}\n")
            out_fp.write(
                f"File size threshold: {naturalsize(size_threshold)}\n"
            )
            if days_old is not None:
                out_fp.write(f"Time threshold: {days_old} ago.\n")
                out_fp.write(f"-" * 80 + '\n')

    return results


def find_files(source_dir: Path, target_dir: Path):
    counter = 0
    for file in Path(source_dir).rglob("*"):
        if not (target_dir / file.absolute().relative_to(source_dir)).exists():
            print(file.absolute())
        counter += 1
    print(counter)


def how_many_files(source_dir: Path):
    counter, vol = 0 , 0.0
    for entry in Path(source_dir).rglob("*"):
        if entry.is_file():
            counter += 1
            vol += entry.stat().st_size
    return counter, vol


if __name__ == '__main__':
    # exercise_path_obj()
    # read_write_file()
    # rename_file()
    # directory_tree(Path(r"G:\just_test"))
    # get_most_recently_modified_file(Path(r"G:\just_test"))
    # find_files(
    #     Path(r"/home/shangguan/Downloads/Enthusiasm"),
    #     Path(r"/media/shangguan/My Passport/Enthusiasm")
    # )
    print(how_many_files(Path(r"/home/shangguan/Downloads/Enthusiasm")))
    print(how_many_files(Path(r"/media/shangguan/My Passport/Enthusiasm")))
    pass
