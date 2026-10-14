# Repository instructions

This public repository distributes exactly one Codex Skill: `huaxin-mail-organizer/`. Keep other personal Skills, mailbox contents, downloaded attachments, credentials, verification codes, and login-session data out of this repository.

For Skill edits, inspect Git status first, use the Codex Skill Creator guidance, run its `quick_validate.py`, and exercise any changed scripts. Stage only files for the current change, inspect the staged diff, and run `gitleaks git --pre-commit --staged --redact --no-banner` before committing. Push only to this repository's authorized public origin; verify the remote visibility and that its branch points to the intended commit. Never force-push. The public visibility is intentional; do not change it or publish other Skills without the owner's explicit authorization.
