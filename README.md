# New Uzbek Latin letters on a US keyboard

Type the new Uzbek Latin letters **ş ç ğ ö** (and **Ş Ç Ğ Ö**) on a standard
US (English) keyboard. These are ordinary keyboard layouts: no background
program, nothing to keep running.

There are two layouts:

- **Uzbek Latin Direct** (Windows) — the letters are on their own keys, one key
  press each: `[` = ğ, `]` = ö, `;` = ş, `'` = ç.
- **Uzbek Latin (AltGr)** (Windows, macOS, Linux) — the US layout plus
  **AltGr (right Alt) + S / C / G / O** for ş ç ğ ö. All brackets and
  punctuation stay in place, so it suits programmers.

## Download

**Windows 10/11 (64-bit): [UzbekLatin.msi](https://github.com/qo0p/newuzlat/releases/latest/download/UzbekLatin.msi)**
— one installer for both Windows layouts. Run it, choose the language
(Özbekça / Русский / English) and the layout (Direct is the default), then
restart the computer. The layout is added to your keyboard list as **UZB**;
switch to it with **Win + Space**. Run the installer again to remove it.

- SHA-256 checksum: [UzbekLatin.msi.sha256](https://github.com/qo0p/newuzlat/releases/latest/download/UzbekLatin.msi.sha256)
  (check with `Get-FileHash .\UzbekLatin.msi -Algorithm SHA256`)
- All versions: [Releases](https://github.com/qo0p/newuzlat/releases) ·
  how the installer is built: [`windows/installer/`](windows/installer/)
- macOS and Linux: see below.

## Windows — Uzbek Latin Direct

| Key | Alone | + Shift | + AltGr | + AltGr + Shift |
|-----|-------|---------|---------|-----------------|
| `[` | **ğ** | **Ğ**   | [       | {               |
| `]` | **ö** | **Ö**   | ]       | }               |
| `;` | **ş** | **Ş**   | —       | —               |
| `'` | **ç** | **Ç**   | '       | "               |
| `\` | **;** | **:**   | "       | \|              |
| `/` | /     | ?       | **\\**  | —               |

The characters these keys normally type move to AltGr on the same key, and
`\` is on AltGr + `/`. Every other key is standard US.

- **Step-by-step guides:**
  [English](windows/INSTALL-direct.md) ·
  [Русский](windows/INSTALL-direct.ru.md) ·
  [Oʻzbekcha](windows/INSTALL-direct.uz.md)
- **MSKLC package:** [`windows/uzlatdir/`](windows/uzlatdir/) — an alternative
  to the MSI: download the whole folder, run `setup.exe` as administrator,
  then restart.

## Windows — Uzbek Latin (AltGr)

| Keys      | You get         |
|-----------|-----------------|
| AltGr + S | ş  (Shift → Ş)  |
| AltGr + C | ç  (Shift → Ç)  |
| AltGr + G | ğ  (Shift → Ğ)  |
| AltGr + O | ö  (Shift → Ö)  |

Every other key types exactly as on the normal US layout.

- **Step-by-step guides:**
  [English](windows/INSTALL.md) ·
  [Русский](windows/INSTALL.ru.md) ·
  [Oʻzbekcha](windows/INSTALL.uz.md)
- **MSKLC package:** [`windows/uzlat/`](windows/uzlat/) — an alternative to
  the MSI: download the whole folder, run `setup.exe` as administrator, then
  restart.

On Windows, AltGr is the same as **Ctrl + Alt**, so left Ctrl + left Alt works
too. The MSI installs one layout at a time. Both layouts can be installed side
by side with the MSKLC packages. Don't mix the two methods: uninstall an MSKLC
install before using the MSI.

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
