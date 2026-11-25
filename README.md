# Aura Soulflame

**English** · [한국어](docs/README.ko.md) · [简体中文](docs/README.zh-CN.md) · [日本語](docs/README.ja.md)

A desktop theme built around plum backgrounds, pink selection, and mint flames. Pick individual Plasma effects or the Kitty palette, then bring your own wallpapers, cursors, or Codex pet if you want them.

![The Plasma login splash reveals a central mint flame and lights the smaller flames in sequence](docs/media/splash.gif)

**Splash** (`plasma-splash`) plays after login as Plasma starts. [Static preview](docs/splash.png)

## What each component does

### KDE Plasma 6

| Colors | Night |
| --- | --- |
| <img src="docs/media/colors.png" width="380" alt="Plasma Colors shows Aura Soulflame with plum backgrounds and pink selection"> | <img src="docs/media/night.png" width="380" alt="The Night lock-screen wallpaper places a mint flame to the right on a plum gradient"> |
| `plasma-colors` sets window, text, focus, and selection colors. Choose **Aura Soulflame (Portable)** in System Settings → Colors. | `plasma-lock` adds **Aura Soulflame Night**, the flame scene under Screen Locking → Appearance → Wallpaper type. |

| Drift | Panel |
| --- | --- |
| <img src="docs/media/drift.gif" width="380" alt="Small mint and amber embers drift up the edges of a dark wallpaper"> | <img src="docs/media/panel.gif" width="258" alt="The panel widget shows a mint flame that brightens when clicked"> |
| `plasma-drift` animates embers over a gradient or your own image. Choose **Aura Soulflame Drift** in the desktop or lock-screen wallpaper picker. Turn off animation in the wallpaper's settings. | `plasma-panel` adds a flame to the panel or desktop. In Edit Mode → Add Widgets, choose **Aura Soulflame Panel**. Click the flame to wake it. |

To turn on the splash, choose **Aura Soulflame Splash** in System Settings → Splash Screen.

### Kitty

![Kitty showing the plum background, mint cursor, pink text accents, and both rows of the 16-color ANSI palette](docs/media/kitty.png)

`kitty` supplies the background, foreground, cursor, selection, tab, and ANSI colors. Preview with `kitty --config <path-to-aura-soulflame.conf>`. To keep the palette, add `include aura-soulflame.conf` after any competing preset in `kitty.conf`. Set `KITTY_CONFIG_DIRECTORY` for the installer if Kitty uses a different config directory.

### Your own assets

| Module | What you provide | Where you use it |
| --- | --- | --- |
| `cursor` | An extracted Xcursor theme with `index.theme` and `cursors/` | Linux desktop or compositor cursor settings |
| `wallpapers` | Local PNG, JPEG, or WebP files | Your OS wallpaper picker |
| `codex-pet` | `pet.json` and its referenced sprite sheet | Codex pet picker. In a compatible terminal, run `/pets` and search by the manifest ID. |
| Plasma portraits | Transparent PNGs for each pose used by the chosen component | Splash, Night, or Panel in place of the default flame |

See the [asset pack layout](docs/assets.md) for file names and `--assets` examples. For another terminal or desktop, map the roles and 16 ANSI colors in [palette.json](resources/palette.json) to its native theme format.

## Install and apply

Run these commands from the repository root with **Python 3.9 or newer**. The Kitty example is for Linux or macOS. Plasma modules require KDE Plasma 6 on Linux. On Windows, use `py -3 aura.py` for local wallpapers or a Codex pet.

```sh
python3 aura.py list
python3 aura.py plan --modules kitty
python3 aura.py install --modules kitty
python3 aura.py status --modules kitty
```

On Linux, use the same sequence with `--modules plasma-colors plasma-splash` to install the Plasma palette and splash. Add other module names as needed. The plan shows the actual destinations under your user's config and data directories. After installation, select the component in the app or desktop settings shown above.

To switch back, first select your previous theme or remove the Kitty include. Then run `python3 aura.py uninstall --modules kitty`, using the modules you installed. If you edited an installed file, the installer reports `modified` and keeps it in place.

## Apply with an AI assistant

> Read `AGENTS.md` and detect my OS, desktop, and target app. Show me an Aura Soulflame plan for the components I choose. Apply them while preserving my existing settings, check the result in the app, and show me how to undo it. My optional asset pack is at `<path>`.

[AI application guide](docs/apply-with-ai.md) · [Module catalog](modules.json) · [Credits and provenance](docs/credits.md)

The previews show the theme running on KDE Plasma 6 and Kitty in an isolated Linux session. Run `python3 -m unittest discover -s tests -v` to check installer behavior.
