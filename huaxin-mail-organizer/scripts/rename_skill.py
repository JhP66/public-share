#!/usr/bin/env python3
"""Rename a skill folder and synchronize its Codex metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import tempfile
from pathlib import Path


NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def atomic_write(path: Path, content: str) -> None:
    """Replace one UTF-8 text file while preserving its mode."""
    mode = stat.S_IMODE(path.stat().st_mode)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_text(path: Path) -> str:
    """Read UTF-8 text without normalizing existing line endings."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def rename_skill(source: Path, new_name: str, display_name: str | None) -> Path:
    if not NAME_PATTERN.fullmatch(new_name) or len(new_name) > 64:
        raise ValueError("新名称须为不超过 64 个字符的小写字母、数字和连字符，且不能以连字符开头或结尾。")
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"Skill 文件夹不存在或是符号链接：{source}")

    skill_file = source / "SKILL.md"
    agent_file = source / "agents" / "openai.yaml"
    readme_file = source / "README.md"
    if (
        skill_file.is_symlink()
        or agent_file.is_symlink()
        or not skill_file.is_file()
        or not agent_file.is_file()
    ):
        raise ValueError("目录中必须同时有 SKILL.md 和 agents/openai.yaml。")
    if readme_file.is_symlink():
        raise ValueError("README.md 不能是符号链接；为安全起见未修改文件。")

    skill_text = read_text(skill_file)
    agent_text = read_text(agent_file)
    frontmatter = FRONTMATTER_PATTERN.match(skill_text)
    if not frontmatter:
        raise ValueError("SKILL.md 开头没有有效的 YAML frontmatter。")

    yaml_text = frontmatter.group(1)
    name_matches = list(re.finditer(r"(?m)^name:\s*(.*?)\s*$", yaml_text))
    if len(name_matches) != 1:
        raise ValueError("frontmatter 必须恰好包含一个顶层 name 字段。")
    old_name = name_matches[0].group(1).strip().strip("\"'")
    if not NAME_PATTERN.fullmatch(old_name):
        raise ValueError(f"无法识别现有 Skill 名称：{old_name!r}")

    updated_yaml = (
        yaml_text[: name_matches[0].start(1)]
        + new_name
        + yaml_text[name_matches[0].end(1) :]
    )
    updated_skill = (
        skill_text[: frontmatter.start(1)]
        + updated_yaml
        + skill_text[frontmatter.end(1) :]
    )

    old_invocation = f"${old_name}"
    new_invocation = f"${new_name}"
    updated_agent, invocation_count = re.subn(
        re.escape(old_invocation) + r"(?![a-z0-9-])",
        lambda _match: new_invocation,
        agent_text,
    )
    if invocation_count == 0:
        raise ValueError(f"agents/openai.yaml 中找不到默认调用名 {old_invocation}；未修改文件。")

    if display_name is not None:
        updated_agent, count = re.subn(
            r"(?m)^(\s*display_name:\s*).*$",
            lambda match: match.group(1) + json.dumps(display_name, ensure_ascii=False),
            updated_agent,
            count=1,
        )
        if count != 1:
            raise ValueError("agents/openai.yaml 中找不到唯一的 display_name 字段；未修改文件。")

    target = source.parent / new_name
    if target != source and target.exists():
        raise FileExistsError(f"目标文件夹已存在：{target}")

    files_to_update = [
        (skill_file, skill_text, updated_skill),
        (agent_file, agent_text, updated_agent),
    ]
    if readme_file.is_file():
        readme_text = read_text(readme_file)
        updated_readme = readme_text.replace(old_name, new_name)
        if updated_readme != readme_text:
            files_to_update.append((readme_file, readme_text, updated_readme))

    changed: list[tuple[Path, str]] = []
    try:
        for path, original, updated in files_to_update:
            atomic_write(path, updated)
            changed.append((path, original))
        if target != source:
            source.rename(target)
    except Exception:
        for path, original in reversed(changed):
            atomic_write(path, original)
        raise

    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="同步重命名 Skill 文件夹、SKILL.md name 和默认调用提示。"
    )
    parser.add_argument("skill_dir", type=Path, help="当前 Skill 文件夹路径")
    parser.add_argument("new_name", help="新的 Skill 名称（小写字母、数字、连字符）")
    parser.add_argument("--display-name", help="可选：同时更新 Codex 界面显示名称")
    args = parser.parse_args()

    source = args.skill_dir.expanduser().absolute()
    try:
        target = rename_skill(source, args.new_name, args.display_name)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"已同步重命名：{source} -> {target}")
    updated_paths = [target / "SKILL.md", target / "agents" / "openai.yaml"]
    if (target / "README.md").is_file():
        updated_paths.append(target / "README.md")
    print("已更新：" + "、".join(str(path) for path in updated_paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
