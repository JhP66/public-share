# Skill 安装与改名指南

本包是可独立修改的 Skill 副本，包含工作指引、Codex 界面元数据、安装说明和名称同步工具；不包含邮箱密码、验证码、登录会话或收件箱数据。修改这个副本不会改动分享者的文件或仓库。

## 使用前确认

- 使用支持 Skills 的 Codex，并确认当前环境可使用 Codex 内置浏览器和 Computer Use；本 Skill 不会代替用户登录。
- 首次查邮箱时，用户需自行完成邮箱登录或验证。不要把密码、验证码或带登录会话的链接写进文件。
- 名称同步脚本需要 Python 3；它只用 Python 标准库，不需另装依赖。Skill 本身不需要运行该脚本才能查邮件。

## 安装

1. 解压分享仓库的 ZIP，进入 `skills/`，确认其中有完整的 `huaxin-mail-organizer` 文件夹（不要只复制 `SKILL.md`，也不要把 ZIP 本身放进 Skills 目录）。
2. 将整个文件夹放到个人 Codex Skills 目录 `~/.codex/skills/`。在 Finder 中可用“前往文件夹…”输入该路径；如果目录不存在，先创建它。只想在某个项目中使用时，可放入该项目的 `.agents/skills/`。
3. 新开一个 Codex 任务检查 Skill 是否出现；若未出现，重启 Codex 后再检查。

## 按需改名

Finder 里单独改文件夹名不会自动改 Skill 内容。先解压，再用包内脚本同时改文件夹名、`SKILL.md` 的 `name`、默认调用提示和 README 中的安装示例：

```sh
python3 "$HOME/Downloads/public-share/skills/huaxin-mail-organizer/scripts/rename_skill.py" \
  "$HOME/Downloads/public-share/skills/huaxin-mail-organizer" my-mail-helper \
  --display-name "我的邮件助手"
```

把示例路径换成实际解压位置；不需要更改界面显示名时，可省略 `--display-name`。名称只允许小写英文字母、数字和连字符，最长 64 个字符。若目标文件夹已存在，脚本会报错退出，不覆盖现有文件。随后把改名后的文件夹安装到 Skills 目录，并在新任务中使用。

如果已经在 Finder 里改过文件夹名，可对当前文件夹运行相同脚本并指定最终名称；它会依据文件内原有 Skill 名称同步其余内容。分享者提供的 ZIP 保持不变。
