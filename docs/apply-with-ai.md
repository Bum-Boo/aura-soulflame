# Apply Aura Soulflame with an AI assistant

## Use the skill

The [Aura Theme Design skill](../.agents/skills/aura-theme-design/SKILL.md) is in `.agents/skills/aura-theme-design/` for repository-scoped discovery in Codex. To use it across repositories, extract the `aura-theme-design/` folder from the [skill ZIP](https://github.com/Bum-Boo/aura-soulflame/releases/latest/download/aura-theme-design.zip) into `~/.agents/skills/`. Use `$aura-theme-design` in your request. In another Agent Skills client, register the extracted folder or ask the assistant to read its `SKILL.md` and use its relative resources. [Codex skill discovery](https://developers.openai.com/codex/skills)

The extracted skill includes the Aura palette, a Kitty preset, CSS export, and contrast checks. Use the repository checkout for the Plasma packages and `aura.py` installer.

A request to give your assistant

> Use `$aura-theme-design` to apply Aura Soulflame to my current desktop or terminal. Detect my environment and show me the plan for the components I ask for. Apply them through the native settings and show me how to switch back. My optional art pack is at `<path>`.

## Detect and choose

| Environment | Pick |
| --- | --- |
| KDE Plasma 6 on Linux | `plasma-colors`, plus any requested Plasma effects. Verify the Plasma version with `plasmashell --version` and list the packages with `kpackagetool6`. |
| Kitty | `kitty`. Locate the actual config with Kitty's **Show Configuration** action or its command-line diagnostics when several config roots exist. |
| GNOME, a tiling compositor, or another terminal | Read `resources/palette.json`. Map `background`, `foreground`, `selection`, `accent`, `mint`, and `ansi` to the matching settings in that app's existing theme file. |
| Linux desktop with Xcursor | `cursor` with a user-supplied theme. Use the session's cursor picker or documented compositor setting. |
| Codex app or terminal | `codex-pet` with a validated pack. Apply in the client's pet picker. Terminal rendering depends on the terminal graphics setup. |

`python3 aura.py list` reports the resolved roots. Check app-specific preferences if the app was started with a custom config path. On existing installations, inspect the current theme, include ordering, and target file before applying changes.

## Preview and apply

Example for a Linux machine running KDE Plasma and Kitty

```sh
python3 aura.py plan --modules kitty plasma-colors
python3 aura.py install --modules kitty plasma-colors
python3 aura.py status --modules kitty plasma-colors
```

Choose only modules supported on the machine. On macOS, the Kitty example uses `--modules kitty`. On Windows, call the script with `py -3 aura.py` for the documented asset modules. Each JSON entry reports its destination and state. A conflict or missing asset produces exit code 2 and prevents the selected install. A subsequent runtime I/O failure may leave earlier components installed. Check each module's `status`, especially `modified`, `conflict`, or `unmanaged`, before proceeding. Keep the same user and XDG roots throughout the install.

- **Kitty:** set `KITTY_CONFIG_DIRECTORY` for the planner and installer to the detected `kitty.conf` directory when it differs from the listed Kitty root. Open a preview with `kitty --config <installed-file>`. For persistent use, add the relative include after the existing color preset, then reload. Check the rendered background and selection colors.
- **Plasma:** prefer the System Settings choices in the README. `plasma-apply-colorscheme --list-schemes` can verify that the scheme is visible. `plasma-apply-colorscheme AuraSoulflamePortable` applies this scheme in an active Plasma session when the user requests activation. For effects, check the component appears in its corresponding settings page and preview it there.
- **Codex:** verify the requested pet ID appears in the pet picker and its preview runs. On Codex terminal, `/pets` filters by ID. Pick the custom entry if the user wants it active.
- **Other apps:** use the native theme or export format. Keep the previous theme selection and verify the installed config with the target application.

## Undo

Restore the former app theme or remove the one line added to its config. Then run `python3 aura.py uninstall --modules …` on the installed components. The receipts in the state directory record file and tree digests. A resource edited after installation is reported as `modified` and stays in place. If an interrupted process leaves an `install.lock`, confirm the installer is no longer running before removing the stale lock file.
