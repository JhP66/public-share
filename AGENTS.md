# Public Share maintenance

This is a public distribution repository for selectively approved copies of projects and resources. Treat everything committed here as visible to everyone. Never mirror a private repository wholesale, automatically sync private sources, or add an item merely because it exists in a private source. Add only the specific content the owner selected, and keep private originals unchanged.

Before adding an item, inspect its source status and provenance, include only required files, exclude credentials, account/session data, private business records, caches, and unrelated work, and make the item's license and installation instructions explicit. Keep licenses scoped to the relevant item; do not imply a repository-wide license unless deliberately approved.

For Skill changes, follow the Codex Skill Creator and run its `quick_validate.py`; test changed scripts. Stage only task files, inspect the staged diff, and run `gitleaks git --pre-commit --staged --redact --no-banner`. Commit and push only to this repository's public `origin`, verify that the repository remains public and the remote branch matches the intended commit. Never force-push or change visibility without explicit authorization.
