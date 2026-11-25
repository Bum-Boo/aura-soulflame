# Design an Aura Soulflame port

Use [palette.json](palette.json) as the starting point. Resolve roles to actual components in the target app before copying colors into a config.

| Role | Use |
| --- | --- |
| `background`, `foreground` | Main canvas or terminal background and normal text |
| `window`, `surface`, `navy` | Raised panels, controls, title bars, and terminal tabs |
| `muted` | Secondary text on a verified dark surface |
| `accent` | Focus, active borders, or a small number of interactive accents |
| `selection`, `foreground` | Filled selection and its readable selected text |
| `mint` | Links, the cursor, and restrained visual highlights |
| `gold`, `error`, `success` | Neutral attention, errors, and success with text or icon cues |
| `visited`, `ansi` | Visited links or the ordered 16-color terminal palette |

`accent` is lighter than the filled `selection`. Use the ivory foreground on selection. On a mint-filled control, start with the deep plum foreground. Check any other pairing against its actual background. Leave enough visual space around decorative flames, and use static or reduced-motion states for backgrounds and long-lived surfaces when supported.

## Export and check

From the skill directory, use the bundled script. It writes to stdout and can run independently of the repository.

```sh
python3 scripts/palette.py css > aura-soulflame.css
python3 scripts/palette.py contrast
python3 scripts/palette.py contrast --palette path/to/adapted-palette.json --pair focus:surface:3 --pair selected-text:selection:4.5
```

The CSS exports custom properties on `:root` for an isolated preview. For an app with multiple themes, map them under the existing theme selector or token scope before applying. A custom palette can define just its `colors` roles. The contrast report checks six common pairs by default. Use `--pair foreground:background:minimum` for controls and state colors from your adaptation. Supply one flag per pair. Check backgrounds after transparency and overlays are composited. The thresholds distinguish normal text from non-text focus markers. [WCAG text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [WCAG non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

For Kitty, [the bundled config](../assets/aura-soulflame.conf) is a ready preset. For another terminal, keep the `ansi` values in their original index order when mapping them to the platform's palette. For apps with opacity or transparency, compare the theme in the real window with a typical background and with any compositor effects enabled.

Show the resulting theme using native preview, a local screenshot, or a small rendering of representative components. If the task includes export, include only files the user wants to share and use public or authorized imagery.
