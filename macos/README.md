# Uzbek Latin keyboard layout — macOS

Type the new Uzbek Latin letters **ş ç ğ ö** (and **Ş Ç Ğ Ö**) on a standard US
keyboard, using the **Option (⌥)** key. It is a keyboard layout — nothing runs
in the background.

(macOS has no separate AltGr key, so it uses **Option**, which is the Mac
equivalent of the AltGr layer used in the Windows and Linux versions.)

| Keys                 | Result |
|----------------------|--------|
| ⌥ Option + S         | ş  (⌥⇧S → Ş) |
| ⌥ Option + C         | ç  (⌥⇧C → Ç) |
| ⌥ Option + G         | ğ  (⌥⇧G → Ğ) |
| ⌥ Option + O         | ö  (⌥⇧O → Ö) |

Every other key types exactly as on the standard US layout.

## Source

`UzbekLatin.keylayout` — the layout, a plain-text XML file (the format macOS
loads). It was written by hand and **has not been tested on macOS**, so verify
it after installing and report anything wrong.

## Install

1. Copy **`UzbekLatin.keylayout`** into:
   - `~/Library/Keyboard Layouts/` — **recommended** (just the current user;
     this is the reliable location and the layout appears after a normal
     log out / log in), **or**
   - `/Library/Keyboard Layouts/` — all users (needs your password, and
     usually a full **restart** before the layout shows up).

   In Finder use **Go → Go to Folder…** (⇧⌘G) and paste the path. Create the
   `Keyboard Layouts` folder if it does not exist.
2. **Log out and back in** (or restart). macOS only scans for new layouts at
   login.
3. Open **System Settings → Keyboard → Text Input → Input Sources → Edit…**
4. Click **+**, choose **Others** (or scroll to the bottom) → **Uzbek Latin** →
   **Add**.
5. Switch to it from the input menu in the menu bar, or with **⌃ Space**
   (Control+Space) / the Caps Lock–as–input-switch if you use that.

## How to type

Select **Uzbek Latin** in the input menu, then hold **Option (⌥)** and press
S / C / G / O. Add **Shift** for the capitals. Everything else types normally.

## Notes

- **Gatekeeper:** a `.keylayout` is plain data, not an app, so there is no
  "unidentified developer" prompt and nothing to notarize.
- **The Option layer is dedicated to these four letters.** Standard macOS
  Option characters (å, ∂, ç via Option-c, accent dead keys, etc.) are **not**
  produced while this layout is active. Switch back to the normal **U.S.**
  input source when you need them.

## Uninstall

1. **System Settings → Keyboard → Text Input → Input Sources → Edit… →** select
   **Uzbek Latin → −** (remove).
2. Delete `UzbekLatin.keylayout` from the `Keyboard Layouts` folder you used.
3. Log out and back in.

## Build from scratch (optional)

To regenerate or tweak it with a GUI, use **Ukelele** (free). If you want to
keep all the standard macOS Option characters *and* add these four letters,
the easiest route is to open the system **U.S.** layout in Ukelele, change only
the Option / Option+Shift output of the S, C, G, O keys, and export.
