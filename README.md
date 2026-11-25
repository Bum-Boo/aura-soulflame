# Aura Soulflame

A dark plum desktop theme with pink selection, mint highlights, and animated flame effects. Use the palette across apps, install individual components, or pair the theme with artwork you can use.

![Aura Soulflame splash with mint flames on a plum gradient](docs/splash.png)

[한국어 안내](docs/README.ko.md) · [Apply with an AI assistant](docs/apply-with-ai.md) · [Asset pack format](docs/assets.md)

## Install a component

Use Python 3.9 or newer. The installer reports the planned destinations as JSON and installs files for the current user. Choose each installed item from its application's settings. This example installs Kitty's palette on Linux or macOS.

```sh
python3 aura.py list
python3 aura.py plan --modules kitty
python3 aura.py install --modules kitty
python3 aura.py status
```

| Resource | Where to use it |
| --- | --- |
| `kitty` | Linux and macOS Kitty. Add `include aura-soulflame.conf` after any competing color preset in `kitty.conf`. Set `KITTY_CONFIG_DIRECTORY` for the installer when Kitty uses a different config directory. Preview with `kitty --config /path/to/aura-soulflame.conf`. |
| `plasma-colors` | Plasma 6 System Settings → Colors → **Aura Soulflame (Portable)**. |
| `plasma-splash` | Plasma 6 System Settings → Splash Screen → **Aura Soulflame Splash**. |
| `plasma-lock` | Plasma 6 Screen Locking → Appearance → Wallpaper type → **Aura Soulflame Night**. |
| `plasma-drift` | Plasma 6 desktop wallpaper or screen-lock wallpaper → **Aura Soulflame Drift**. Browse for your own image or use the built-in gradient. The settings include an animation toggle. |
| `plasma-panel` | Plasma 6 Edit Mode → Add Widgets → **Aura Soulflame Panel**. Click the widget to wake the flame. |
| `cursor` | Linux Xcursor. Install your theme package and choose it under the desktop's Cursor settings. |
| `wallpapers` | Select one of your installed images from your operating system's wallpaper picker. |
| `codex-pet` | Install your pet package and choose it in Codex. In a compatible terminal, open `/pets` and search for the ID in `pet.json`. |

Use `--assets /path/to/asset-pack` with the three asset-only modules or with Plasma components that accept optional portraits. See the [asset pack layout](docs/assets.md) for file names and examples. For a manual port to another desktop or terminal, use the named roles and ANSI colors in [palette.json](resources/palette.json).

On KDE Plasma 6, use `python3 aura.py install --modules plasma-colors plasma-splash` after planning those modules. On Windows, use `py -3 aura.py` for local wallpapers or a Codex pet.

The planner uses the active `XDG_*`, `KITTY_CONFIG_DIRECTORY`, and `CODEX_HOME` locations when set. A differing existing file or package is reported as a conflict. An identical pre-existing resource remains under its existing owner's control. Install and removal work one component at a time after plan validation. An active desktop session can keep a component cached until you reload its app or settings view.

## Switch back

Select your previous theme or remove the Kitty include before uninstalling. The tool removes resources recorded in its receipt and reports any resource whose digest changed since install. Recover or keep edited files yourself before replacing them.

```sh
python3 aura.py uninstall --modules kitty
```

## Verify or adapt

```sh
python3 -m unittest discover -s tests -v
```

[Module catalog](modules.json) lists sources, destination roots, and platform constraints. [Credits and provenance](docs/credits.md) records the origin of the portable theme and upstream references.
