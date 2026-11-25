# Apply the packaged Aura theme

The [Aura Soulflame repository](https://github.com/Bum-Boo/aura-soulflame) contains `aura.py`, `modules.json`, and app-specific application instructions. Use the checkout supplied by the user. If only the skill was supplied, its palette and Kitty config work independently. Use the repository when the requested module needs the installer.

| Target | Choose |
| --- | --- |
| Kitty on Linux or macOS | `kitty`, or preview the bundled preset with `kitty --config <preset>` |
| KDE Plasma 6 on Linux | `plasma-colors`, `plasma-splash`, `plasma-lock`, `plasma-drift`, or `plasma-panel` as requested |
| A local Xcursor theme, wallpapers, or Codex pet | `cursor`, `wallpapers`, or `codex-pet` with `--assets <pack>` |
| Other terminals, desktops, or web apps | The native config format and the palette in this skill |

In the repository, run `python3 aura.py list` and `python3 aura.py plan --modules ...` with the requested module names. Use `py -3 aura.py` on Windows for the supported local wallpaper and Codex pet modules. The plan reports the resolved destination, conflicts, and missing inputs. Follow [assets.md](https://github.com/Bum-Boo/aura-soulflame/blob/main/docs/assets.md) for the local pack layout, and keep the same selected modules and environment roots from plan through uninstall.

Install the selected modules. Choose the installed resources through the app's native settings. In Kitty, use the actual config root, preview the preset, and add its include after an existing palette when the user requests persistent activation. Restore the old include or selection before `python3 aura.py uninstall --modules ...`. Keep user-edited resources that report `modified`.

The [AI application guide](https://github.com/Bum-Boo/aura-soulflame/blob/main/docs/apply-with-ai.md) lists app-specific activation steps. Verify the module-level status and confirm visible activation independently. If you cannot see the running app, state the verified files and the remaining app check.
