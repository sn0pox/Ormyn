# Ormyn brand

| Token | Hex | Used for |
|---|---|---|
| Black | `#000000` | island pill and ear flares (tinted by the song colour while music plays) |
| Tile | `#08080A` | app icon background |
| Pale gold | `#FFE9A6` | gradient start, wordmark start, intro bloom |
| Gold | `#FFC83D` | main accent: default pill tint / bloom / backlight when a song has no artwork colour |
| Amber | `#E28E12` - `#FFB81F` | gradient end, wordmark end, eye gradient end |
| Cream | `#FFF3D1` | intro bloom end |

- **Mark:** a black pill floating on a near-black rounded tile, rimmed and lit by a pale-gold > gold > amber glow,
  with two glowing vertical slit eyes. No other face details. The startup animation is built from the same eyes.
- **Startup animation (~1.5 s):** the pill grows out of the top edge, the two eyes open from closed slits (no text),
  a single soft gold bloom, then it docks. No overshoot, no blink, no colour cycling.
- **Glow rule:** the bloom and the top-edge backlight take the dominant colour of the current album art;
  gold is only the fallback and the brand colour.
- **Fonts / glyphs:** Segoe UI and Segoe MDL2 Assets (both ship with Windows, nothing is bundled).
- **Files:** `ormyn.ico` is embedded in the exe and used for the tray; `ormyn-icon.png` (1024 px) is the master
  artwork for the repo/README; `make_icon.py` regenerates both (`pip install pillow numpy`).
- **Previous names:** DynamicIsland, Buddy, Natalya (the app migrates settings and closes old copies automatically).
