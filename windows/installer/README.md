# Single-file MSI installer (both layouts)

**`UzbekLatin.msi`** is one self-contained file that installs either Windows
layout. The user downloads only the MSI, double-clicks it, and:

1. picks the installer language: **Özbekça** (default), Русский or English;
2. picks the layout: **Uzbek Latin Direct** (default) or **Uzbek Latin
   (AltGr) — for programmers** (keeps brackets and punctuation in place);
3. clicks Install. It installs for all users (Windows asks for admin rights).

After Finish, Windows asks to restart the computer (the finish screen also
says so in bold). After the restart the layout is already in the keyboard list
of the user who installed it — pick it with **Win + Space**. Other users of the
PC add it once under Settings → Time & Language → Language & region → Uzbek
(Latin) → Language options → Add a keyboard. Running the MSI again when a
layout is installed offers to remove it.

## Build (Docker, any OS)

```
./build.sh
```

It builds a small Ubuntu image with **msitools** and writes `UzbekLatin.msi`
here. No Windows or WiX needed. The MSI packs the layout DLLs from
`../uzlatdir/` (Direct) and `../uzlat/` (AltGr), both 64-bit and 32-bit (wow64)
copies, so rebuild the MSI after rebuilding a layout with MSKLC.

How it works (`make_msi.py`):

1. `wixl` builds the base MSI: files, registry, embedded cab, install steps.
2. `wixl` can't do dialogs or component conditions, so those are written as raw
   MSI tables (`.idt`) and imported with `msibuild`.

**All UI text (Uzbek / Russian / English) is in `STRINGS` in `make_msi.py`.**
The Uzbek text uses the new Latin alphabet (ö ğ ş ç). To hold Uzbek and
Russian in one MSI, the database uses code page 65001 (UTF-8). Don't use
`[ ] {` in the texts: the MSI treats them as formatting codes (the build stops
with an error if you do).

## What it installs

| Layout | DLL (System32 + SysWOW64) |
|--------|---------------------------|
| Uzbek Latin Direct | `UzLatDir.dll` |
| Uzbek Latin (AltGr) | `UzLat.dll` |

Registering the layout with Windows and adding it to the installing user's
keyboard list is done by **`KbdMsi.dll`**, Microsoft's custom-action DLL from
MSKLC (signed by Microsoft). The build copies it unchanged out of the
MSKLC-built `../uzlatdir/UzLatDir_amd64.msi` and calls it with the same entry
points, data and timing as MSKLC's own installer, so the result is the same as
installing with MSKLC's `setup.exe`. Uninstalling removes the layout from the
keyboard list, unregisters it and deletes the DLLs.

## Verify the download

Each build also writes **`UzbekLatin.msi.sha256`** with the file's SHA-256
checksum. To check a downloaded MSI against it:

- **Windows (PowerShell):** `Get-FileHash .\UzbekLatin.msi -Algorithm SHA256`
  — compare the hash with the one in `UzbekLatin.msi.sha256`.
- **Windows (Command Prompt):** `certutil -hashfile UzbekLatin.msi SHA256`
- **Linux / macOS:** `sha256sum -c UzbekLatin.msi.sha256` (prints `OK`).

The MSI gets a new product code and timestamp on every build, so the checksum
changes with each rebuild. Always publish the MSI and its `.sha256` together.

## Silent install (no UI)

```
msiexec /i UzbekLatin.msi /qn                 (Direct layout)
msiexec /i UzbekLatin.msi LAYOUT=altgr /qn    (AltGr layout)
msiexec /x UzbekLatin.msi /qn                 (uninstall)
```

Silent installs never restart the computer by themselves; restart it after.

## Notes

- **One layout per install.** To switch, uninstall ("Uzbek Latin Keyboard" in
  Settings → Apps), then run the MSI again and pick the other one.
- **Remove older MSKLC installs first.** If "Uzbek Latin" or "Uzbek Latin
  Direct" was installed with an MSKLC `setup.exe`, uninstall it before using
  this MSI. Both use the same DLL names in `System32`.
- 64-bit Windows only (Windows 11 is 64-bit only anyway).
- Unsigned, so SmartScreen may show "unknown publisher → Run anyway".
- **Test on real Windows.** Wine renders the installer screens fine, but it
  can't run `KbdMsi.dll` (MSKLC's own installer fails under Wine the same way)
  and doesn't show the restart prompt. Windows Installer also doesn't
  officially document UTF-8 databases, so check that the Uzbek letters display
  correctly.
- If you installed a test build of this MSI before, uninstall it first or make
  sure the new build has a higher `VERSION` in `make_msi.py`, so it upgrades
  instead of installing next to the old one.
