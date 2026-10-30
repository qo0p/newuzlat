# New Uzbek Latin letters on a US keyboard

Type the new Uzbek Latin letters **ş ç ğ ö** (and **Ş Ç Ğ Ö**) on a standard
US (English) keyboard, without switching away from the layout you already use.

In every case you hold **AltGr (the right Alt key)** and press a letter:

| Keys                          | You get |
|-------------------------------|---------|
| AltGr + S                     | ş  (Shift → Ş) |
| AltGr + C                     | ç  (Shift → Ç) |
| AltGr + G                     | ğ  (Shift → Ğ) |
| AltGr + O                     | ö  (Shift → Ö) |

Every other key types exactly as on the normal US layout.

## Download

**Windows 10/11 (64-bit): [UzbekLatin.msi](https://github.com/qo0p/newuzlat/releases/latest/download/UzbekLatin.msi)**
— one installer for both Windows layouts. Run it, choose the language
(Özbekça / Русский / English) and the layout, then restart the computer. The
layout is added to your keyboard list; switch to it with **Win + Space**.

- SHA-256 checksum: [UzbekLatin.msi.sha256](https://github.com/qo0p/newuzlat/releases/latest/download/UzbekLatin.msi.sha256)
  (check with `Get-FileHash .\UzbekLatin.msi -Algorithm SHA256`)
- All versions: [Releases](https://github.com/qo0p/newuzlat/releases) ·
  how the installer is built: [`windows/installer/`](windows/installer/)
- macOS and Linux: see below.

## Windows

The single installer above is the easiest way. The per-layout MSKLC packages
below install the same layouts.

A keyboard layout you install once (no background program, nothing to run).

- **Installer:** [`windows/uzlat/`](windows/uzlat/) — download the folder and run
  `setup.exe` as administrator, then reboot.
- **Step-by-step guides:**
  [English](windows/INSTALL.md) ·
  [Русский](windows/INSTALL.ru.md) ·
  [Oʻzbekcha](windows/INSTALL.uz.md)

After installing, the layout appears as **UZB** in the taskbar; switch to it
with **Win + Space**.

### Windows — "Direct" variant (no AltGr)

An alternative layout, **Uzbek Latin Direct**, puts the letters on their own
keys so each is a single key press:

| Key | Alone | + Shift |
|-----|-------|---------|
| `[` | ğ     | Ğ       |
| `]` | ö     | Ö       |
| `;` | ş     | Ş       |
| `'` | ç     | Ç       |
| `\` | ;     | :       |

The characters these keys normally type (`[ ] { } ' " |`) move to AltGr on
the same key; AltGr + `\` types `"` and `\` is on AltGr + `/`. Every other key is standard US.

- **Installer:** [`windows/uzlatdir/`](windows/uzlatdir/) — run `setup.exe` as
  administrator, then reboot.
- **Step-by-step guides:**
  [English](windows/INSTALL-direct.md) ·
  [Русский](windows/INSTALL-direct.ru.md) ·
  [Oʻzbekcha](windows/INSTALL-direct.uz.md)

Both Windows layouts can be installed side by side.

## macOS

A keyboard layout (`.keylayout`) that uses the **Option (⌥)** key — the Mac
equivalent of the AltGr layer. No background program.

- **Layout:** [`macos/UzbekLatin.keylayout`](macos/UzbekLatin.keylayout) — copy
  into `~/Library/Keyboard Layouts/`, log out/in, then enable **Uzbek Latin**
  in System Settings → Keyboard → Input Sources.
- **Step-by-step guides:**
  [English](macos/README.md) ·
  [Русский](macos/README.ru.md) ·
  [Oʻzbekcha](macos/README.uz.md)

On macOS the letters are typed with **Option + S / C / G / O** (Shift for
capitals).

## Ubuntu / Linux

A custom XKB mapping (Ubuntu 24.04, GNOME on Wayland) that adds the AltGr layer
without changing your system files or switching layouts.

- **Guide:** [`ubuntu/README.md`](ubuntu/README.md)

