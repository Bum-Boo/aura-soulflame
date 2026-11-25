#!/usr/bin/env python3
"""Inspect, install, and remove individual Aura Soulflame resources."""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import struct
import sys
import tempfile
from contextlib import contextmanager, nullcontext
from pathlib import Path

REPO = Path(__file__).resolve().parent
CATALOG = json.loads((REPO / "modules.json").read_text(encoding="utf-8"))
MODULES = CATALOG["modules"]
PET_ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def absolute_env(name, default):
    value = os.environ.get(name)
    path = Path(value).expanduser() if value else default
    return (path if path.is_absolute() else default).resolve()


def locations():
    home = Path.home()
    config = absolute_env("XDG_CONFIG_HOME", home / ".config")
    return {
        "kitty": absolute_env("KITTY_CONFIG_DIRECTORY", config / "kitty"),
        "data": absolute_env("XDG_DATA_HOME", home / ".local/share"),
        "codex": absolute_env("CODEX_HOME", home / ".codex"),
        "state": absolute_env("XDG_STATE_HOME", home / ".local/state") / "aura-soulflame",
    }


def target_path(root, relative):
    relative = Path(relative)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError(f"Invalid destination: {relative}")
    path = root / relative
    for parent in path.parents:
        if parent.is_symlink():
            raise ValueError(f"Destination parent is a symbolic link: {parent}")
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"Destination parent is not a directory: {parent}")
        if parent == root:
            break
    return path


def fingerprint(path, *, check_links=False):
    root = path.resolve()
    digest = hashlib.sha256()
    entries = sorted(path.rglob("*")) if path.is_dir() and not path.is_symlink() else []
    for entry in [path, *entries]:
        name = entry.relative_to(path).as_posix()
        mode = entry.lstat().st_mode
        if stat.S_ISLNK(mode):
            link = entry.readlink()
            if check_links and (link.is_absolute() or not entry.resolve(strict=True).is_relative_to(root)):
                raise ValueError(f"Asset link leaves its module: {entry}")
            record = (name, "link", str(link))
        elif stat.S_ISDIR(mode):
            record = (name, "directory")
        elif stat.S_ISREG(mode):
            with entry.open("rb") as handle:
                file_hash = hashlib.sha256()
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    file_hash.update(block)
            record = (name, "file", file_hash.hexdigest())
        else:
            raise ValueError(f"Expected a regular file, directory or relative link: {entry}")
        digest.update(json.dumps(record).encode("utf-8") + b"\n")
    return digest.hexdigest()


def copy_path(source, target):
    if source.is_dir():
        shutil.copytree(source, target, symlinks=True)
    else:
        shutil.copy2(source, target)


def image_size(image):
    with image.open("rb") as handle:
        data = handle.read(32)
    if image.suffix.lower() == ".png" and len(data) >= 24 and data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    if image.suffix.lower() == ".webp" and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X" and len(data) >= 30:
            return tuple(1 + int.from_bytes(data[i:i + 3], "little") for i in (24, 27))
        if data[12:16] == b"VP8L" and data[20:21] == b"/" and len(data) >= 25:
            bits = int.from_bytes(data[21:25], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if data[12:16] == b"VP8 " and data[23:26] == b"\x9d\x01\x2a" and len(data) >= 30:
            return tuple(value & 0x3FFF for value in struct.unpack("<HH", data[26:30]))
    raise ValueError(f"Unable to read image dimensions: {image}")


def pet_dimensions(pet):
    if "frame" not in pet:
        return (1536, 2288 if pet.get("spriteVersionNumber") == 2 else 1872)
    frame = pet["frame"]
    keys = ("width", "height", "columns", "rows")
    if not isinstance(frame, dict) or any(type(frame.get(key)) is not int or frame[key] <= 0 for key in keys):
        raise ValueError("A custom Codex frame grid needs positive integer dimensions")
    return frame["width"] * frame["columns"], frame["height"] * frame["rows"]


def pack_source(module, source, stage):
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"Expected an asset directory: {source}")
    if module == "wallpapers":
        files = sorted(path for path in source.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)
        if not files or any(path.is_symlink() or not path.is_file() for path in files):
            raise ValueError(f"Supply regular PNG, JPEG or WebP files in {source}")
        stage.mkdir()
        for path in files:
            shutil.copy2(path, stage / path.name)
    elif module == "cursor":
        index = source / "index.theme"
        if not index.is_file() or not (source / "cursors").is_dir():
            raise ValueError("A cursor pack needs index.theme and a cursors directory")
        fingerprint(source, check_links=True)
        with (source / "cursors/default").open("rb") as handle:
            if handle.read(4) != b"Xcur":
                raise ValueError("The cursor pack needs an Xcursor file at cursors/default")
        copy_path(source, stage)
    else:
        manifest = source / "pet.json"
        if manifest.is_symlink() or not manifest.is_file():
            raise ValueError("A Codex pet pack needs a regular pet.json file")
        pet = json.loads(manifest.read_text(encoding="utf-8"))
        pet_id = pet.get("id") if isinstance(pet, dict) else None
        if not isinstance(pet_id, str) or not PET_ID.fullmatch(pet_id):
            raise ValueError("pet.json needs an alphanumeric id with optional hyphens or underscores")
        sprite = Path(str(pet.get("spritesheetPath", "spritesheet.webp")))
        if sprite.name != str(sprite) or sprite.suffix.lower() not in {".png", ".webp"}:
            raise ValueError("Use a plain PNG or WebP filename in spritesheetPath")
        image = source / sprite
        if image.is_symlink() or not image.is_file():
            raise ValueError(f"Pet image missing: {image}")
        if image_size(image) != pet_dimensions(pet):
            raise ValueError(f"Sprite dimensions do not match the Codex grid declared by {manifest}")
        stage.mkdir()
        shutil.copy2(manifest, stage / manifest.name)
        shutil.copy2(image, stage / sprite)
        return pet_id
    return None


def stage_resource(module, spec, assets, stage):
    if "pack" in spec:
        if assets is None or not os.path.lexists(assets / spec["pack"]):
            raise ValueError(f"Supply --assets with a {spec['pack']}/ directory")
        return pack_source(module, assets / spec["pack"], stage)

    copy_path(REPO / spec["source"], stage)
    if "shared" not in spec:
        return None
    ui = stage / spec["shared"]
    shared = REPO / "themes/plasma/shared"
    shutil.copy2(shared / "AuraFlame.qml", ui)
    entrypoint = ui / "main.qml"
    if module != "plasma-panel":
        entrypoint = ui / "AuraScene.qml"
        shutil.copy2(shared / entrypoint.name, entrypoint)
    portraits = assets / "portraits" if assets is not None else None
    if portraits is not None and os.path.lexists(portraits):
        if portraits.is_symlink() or not portraits.is_dir():
            raise ValueError(f"Expected a portrait directory: {portraits}")
        filenames = [name + ".png" for name in spec["portraits"]]
        for name in filenames:
            image = portraits / name
            if image.is_symlink() or not image.is_file():
                raise ValueError(f"Portrait pack needs a regular PNG at {image}")
            with image.open("rb") as handle:
                if handle.read(8) != b"\x89PNG\r\n\x1a\n":
                    raise ValueError(f"Invalid portrait PNG: {image}")
        art = ui / "art"
        art.mkdir()
        for name in filenames:
            shutil.copy2(portraits / name, art / name)
        text = entrypoint.read_text(encoding="utf-8")
        marker = "readonly property bool portraitPack: false"
        if text.count(marker) != 1:
            raise ValueError(f"Portrait setting missing in {entrypoint}")
        entrypoint.write_text(text.replace(marker, marker.replace("false", "true")), encoding="utf-8")
    return None


def read_state(path):
    if path.parent.is_symlink() or path.is_symlink():
        raise ValueError(f"Receipt path is a symbolic link: {path}")
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("installed"), dict):
        raise ValueError(f"Invalid receipt file: {path}")
    records = data["installed"]
    for module, record in records.items():
        if (module not in MODULES or not isinstance(record, dict) or not isinstance(record.get("target"), str)
                or not isinstance(record.get("sha256"), str)):
            raise ValueError(f"Invalid receipt for {module} in {path}")
    return records


def write_state(path, records):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump({"schema": 1, "installed": records}, handle, indent=2)
        handle.write("\n")
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def locked(state_dir):
    if state_dir.is_symlink():
        raise ValueError(f"Receipt directory is a symbolic link: {state_dir}")
    state_dir.mkdir(parents=True, exist_ok=True)
    lock = state_dir / "install.lock"
    try:
        lock.touch(exist_ok=False)
    except FileExistsError as exc:
        raise ValueError(f"Another install or removal holds {lock}") from exc
    try:
        yield
    finally:
        lock.unlink()


def receipt_target(module, spec, roots, receipt):
    relative = spec["target"]
    if module == "codex-pet":
        pet_id = Path(receipt["target"]).name
        if not PET_ID.fullmatch(pet_id):
            raise ValueError("Invalid pet id in receipt")
        relative = f"{relative}/{pet_id}"
    path = target_path(roots[spec["root"]], relative)
    if str(path) != receipt["target"]:
        raise ValueError(f"Use the original home and XDG paths to manage {module}: {receipt['target']}")
    return path


def plan_item(module, spec, roots, asset_dir, stage, receipt):
    if sys.platform not in spec["platforms"]:
        return {"status": "unsupported", "reason": f"Unsupported platform: {sys.platform}"}
    try:
        pet_id = stage_resource(module, spec, asset_dir, stage)
        relative = f"{spec['target']}/{pet_id}" if pet_id else spec["target"]
        path = target_path(roots[spec["root"]], relative)
        expected = fingerprint(stage)
        if receipt and receipt_target(module, spec, roots, receipt) != path:
            raise ValueError(f"Remove the previous {module} before installing a different one")
        if path.is_symlink():
            return {"status": "conflict", "target": str(path), "reason": "Destination is a symbolic link"}
        if path.exists():
            current = fingerprint(path)
            if current != expected or (receipt and current != receipt["sha256"]):
                return {"status": "conflict", "target": str(path), "reason": "Destination already has different content"}
            return {"status": "installed" if receipt else "present-unmanaged", "target": str(path), "sha256": expected}
        return {"status": "ready", "target": str(path), "sha256": expected}
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        return {"status": "unavailable", "reason": str(exc)}


def add_resource(source, target, expected):
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        target.mkdir()
        try:
            shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
            if fingerprint(target) != expected:
                raise ValueError(f"Installed files did not match: {target}")
        except BaseException:
            shutil.rmtree(target)
            raise
    else:
        with target.open("xb") as destination:
            try:
                with source.open("rb") as content:
                    shutil.copyfileobj(content, destination)
                destination.flush()
                if fingerprint(target) != expected:
                    raise ValueError(f"Installed file did not match: {target}")
            except BaseException:
                destination.close()
                target.unlink()
                raise


def remove_resource(path):
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def inspect_receipt(module, roots, receipt):
    if not receipt:
        return {"status": "unmanaged"}
    try:
        path = receipt_target(module, MODULES[module], roots, receipt)
        if not os.path.lexists(path):
            return {"status": "missing", "target": str(path)}
        unchanged = not path.is_symlink() and fingerprint(path) == receipt["sha256"]
        return {"status": "installed" if unchanged else "modified", "target": str(path)}
    except (OSError, ValueError, KeyError) as exc:
        return {"status": "conflict", "reason": str(exc)}


def execute(args):
    roots = locations()
    if args.command == "list":
        return {"ok": True, "version": CATALOG["version"], "platform": sys.platform,
                "locations": {key: str(value) for key, value in roots.items()}, "modules": MODULES}

    path = roots["state"] / "receipts.json"
    lock = locked(path.parent) if args.command in {"install", "uninstall"} else nullcontext()
    with lock:
        records = read_state(path)
        selected = list(dict.fromkeys(args.modules or MODULES))
        if args.command in {"status", "uninstall"}:
            results = {}
            for module in selected:
                result = inspect_receipt(module, roots, records.get(module))
                results[module] = result
                if args.command == "uninstall" and result["status"] in {"installed", "missing"}:
                    if result["status"] == "installed":
                        remove_resource(Path(result["target"]))
                    del records[module]
                    write_state(path, records)
                    result["status"] = "removed"
            ok = args.command == "status" or all(result["status"] in {"removed", "unmanaged"} for result in results.values())
            return {"ok": ok, "modules": results}

        assets = args.assets.expanduser().resolve(strict=True) if args.assets else None
        with tempfile.TemporaryDirectory(prefix="aura-soulflame-") as tmp:
            stages = {module: Path(tmp) / module for module in selected}
            results = {module: plan_item(module, MODULES[module], roots, assets, stages[module], records.get(module))
                       for module in selected}
            ok = all(result["status"] in {"ready", "installed", "present-unmanaged"} for result in results.values())
            if args.command == "install" and ok:
                for module, result in results.items():
                    if result["status"] != "ready":
                        continue
                    target = Path(result["target"])
                    add_resource(stages[module], target, result["sha256"])
                    records[module] = {"target": str(target), "sha256": result["sha256"]}
                    try:
                        write_state(path, records)
                    except OSError:
                        if fingerprint(target) == result["sha256"]:
                            remove_resource(target)
                        raise
                    result["status"] = "installed"
            return {"ok": ok, "modules": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="show available resources and destination roots as JSON")
    for name in ("plan", "install", "status", "uninstall"):
        command = commands.add_parser(name)
        command.add_argument("--modules", nargs="+", required=name != "status", choices=MODULES)
        if name in {"plan", "install"}:
            command.add_argument("--assets", type=Path, help="optional local asset directory")
    args = parser.parse_args()
    try:
        result = execute(args)
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
