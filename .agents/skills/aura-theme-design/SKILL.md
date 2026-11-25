---
name: aura-theme-design
description: Design, port, or apply an Aura Soulflame theme for a desktop, terminal, or app. Use when the user asks for Aura's plum backgrounds, pink accents, mint highlights, or existing KDE or Kitty modules and wants them adapted to a target environment.
license: MIT
---

# Aura Theme Design

Choose the branch that matches the request. A design or preview request ends with an artifact that can be reviewed. An application request also includes installation, activation where supported, and a way back to the previous setting.

## Design or port

1. Identify the target app, OS, and the existing theme or token format. For a new design, derive roles from [references/palette.json](references/palette.json). Preserve the app's typography and component states unless the brief changes them.
2. Map deep plum to the canvas, warmer surfaces to stacked UI, pink to selection or focus, and mint to links or a few highlights. Keep normal text ivory and give status colors a label or icon. Read [references/design.md](references/design.md) for role mapping, contrast checks, and visual previews. Reuse [assets/aura-soulflame.conf](assets/aura-soulflame.conf) for Kitty.
3. Produce a native theme file or a narrow configuration change. Smoke-test the result in the target app when available. Inspect text, focus, selection, disabled text, and any high-frequency motion against the real backgrounds. Report the artifact and the checks you could observe.

## Apply the supplied theme

Use [references/apply.md](references/apply.md) to choose the supported Plasma, Kitty, and local-asset modules. Locate the supplied repository checkout before running its installer. Report the planned destinations, preserve conflicting files, and use native settings to activate the theme. A file-level `installed` status and visible activation are separate checks.

When switching an existing setting, record its former value. Give undo steps for both the app setting and the installed resource. Use the user's selected assets and scope for any exported or shared theme.
