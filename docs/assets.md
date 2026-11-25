# Asset packs

The [included character pack](../assets/character) has portraits, a cursor theme, six wallpapers, and a Codex pet. Run the installer with `--assets assets/character` to use it, or point to a pack of your own with the layout below. See the [full theme collection](extended-themes.md) for previews and activation steps.

```text
my-assets/
  portraits/
    awake.png
    sleep.png
    lean.png
    look-left.png
    look-right.png
  cursor/
    index.theme
    cursors/
      default
      left_ptr
  wallpapers/
    dusk.png
  pet/
    pet.json
    spritesheet.webp
```

- **Portraits:** use transparent PNGs of the same subject and framing. Splash and Night use `awake` and `sleep`. Panel uses `awake`, `lean`, `look-left`, and `look-right`. Plan shows which files are required by the selected components. Drift accepts a wallpaper image from its settings.
- **Cursor:** provide an extracted Xcursor theme with an Xcursor `cursors/default` file or an alias to one. Cursor aliases use relative links within the theme. The installer places the pack in the user icon directory as `AuraSoulflameCursor`.
- **Wallpapers:** select a directory of regular PNG, JPG, JPEG, or WebP files. After install, browse to the destination reported in `plan` to select an image in your OS.
- **Codex pet:** include `pet.json` and the PNG or WebP named in `spritesheetPath`. The manifest's `id` names the destination directory. Test the atlas layout against the client you intend to run. [Codex pet atlas contract](https://github.com/openai/skills/blob/main/skills/.curated/hatch-pet/references/codex-pet-contract.md)

```sh
python3 aura.py plan --assets ~/my-assets --modules codex-pet wallpapers
python3 aura.py install --assets ~/my-assets --modules codex-pet wallpapers
```

On Linux with Plasma 6, add `plasma-splash` or `cursor` as needed. For Windows, use `py -3 aura.py plan --assets C:/my-assets --modules codex-pet`.

Keep your source artwork with your asset pack. Use material with suitable permissions for the way you intend to share the pack. The public theme can be paired with different characters, drawings, or photos without modifying its QML.
