# Applying Aura Soulflame

Apply the selected components to the user's environment. `modules.json` is the source of truth for component names, platform constraints, source paths, and destinations.

For a brief that asks you to design, port, or apply the Aura style, read [the Aura Theme Design skill](.agents/skills/aura-theme-design/SKILL.md). Keep the skill's bundled palette and Kitty preset in sync with the corresponding repository files when editing them.

1. Identify the OS, desktop session or compositor, target app, and requested effect. Use `python3 aura.py list` to resolve the actual config roots. For a different app, map roles from `resources/palette.json` to that app's native format.
2. Preview the exact selection with `python3 aura.py plan --modules …`. Pass `--assets` only for a user-supplied pack. Read `docs/assets.md` for cursors, wallpapers, portraits, or a Codex pet.
3. Act on the plan. Continue with `ready` and `installed`. Keep `present-unmanaged` entries with their existing owner. For a conflict, preserve the existing file and select a different component or coordinate a merge with its owner. Resolve missing dependencies or choose a documented manual path before applying.
4. Run `python3 aura.py install --modules …` with the same selection. Use the target app's native setting to activate it. If activation edits an existing configuration file, capture its previous state and change only the relevant setting. The installer manages installed resources in the current user account.
5. Verify each module's status through `python3 aura.py status` and confirm activation in the application. The top-level `ok` on `status` describes the query, while each module reports its own state. Report what was installed, what actually activated, and how to return to the previous setting. If the application cannot be observed, report file-level verification and the remaining manual check.

Use `docs/apply-with-ai.md` for platform-specific commands, activation, and rollback. Changes to installer behavior need a test through the CLI. Run `python3 -m unittest discover -s tests -v` from the root.
