# Installing the Uzbek Latin keyboard

This adds an **Uzbek Latin** keyboard to Windows so you can type the letters
**ş ç ğ ö** (and **Ş Ç Ğ Ö**) on a normal keyboard. It is just a keyboard
layout — nothing runs in the background.

## What you received

A folder (or zip) containing **`setup.exe`** and one or more **`.msi`** files.
Keep them together — `setup.exe` needs the `.msi` files next to it.

## Install

1. If you were given a zip, **unzip it first** (right-click → Extract All).
   Do not run `setup.exe` from inside the zip.
2. **Right-click `setup.exe` → Run as administrator.**
3. If Windows shows **"Windows protected your PC"**, click **More info → Run
   anyway**. (This appears because the installer is not signed; it is safe.)
4. Let it finish. It installs for **all users** on the PC.
5. **Restart the computer.** This step is required — the keyboard is not fully
   active until you reboot, and skipping it can make the taskbar flicker.

## Turn it on (after the reboot)

First check the taskbar (bottom-right, by the clock): if a **UZB** indicator is
already there, the installer added it for you — skip to "How to type". If not,
add it:

1. Open **Settings → Time & Language → Language & region**.
2. If **Uzbek (Latin)** is not in the language list: **Add a language**, find
   **Uzbek (Latin)**, then **Next → Install**. Untick the optional features
   (display language, speech, handwriting) — only the keyboard is needed — and
   do **not** set it as the Windows display language.
3. Click the **⋯** next to **Uzbek → Language options**. Under **Keyboards**,
   click **Add a keyboard** and choose **"Uzbek Latin"**. (This is the key step:
   adding the language alone gives the *default* Uzbek keyboard, not this one.)
   If a default **Uzbek** keyboard was also added and you don't want it, click
   it → **Remove**.
4. A **UZB** indicator now appears in the taskbar. Switch keyboards with
   **Win + Space** (hold Win, tap Space), or click the **UZB / ENG** indicator.

## How to type the letters

Switch to **UZB**, then hold the **right Alt** key (AltGr) and press a letter:

| Keys                              | You get |
|-----------------------------------|---------|
| Right Alt + S                     | ş       |
| Right Alt + Shift + S             | Ş       |
| Right Alt + C / G / O             | ç / ğ / ö |
| Right Alt + Shift + C / G / O     | Ç / Ğ / Ö |

Every other key types exactly as normal. Switch back to **ENG** with Win + Space
for ordinary English typing.

## Uninstall

1. **Settings → Time & Language → Language & region →** the Uzbek entry's
   **⋯ → Language options →** under Keyboards, **Remove** "Uzbek Latin".
2. **Settings → Apps → Installed apps →** find **"Uzbek Latin" → Uninstall**.
3. **Restart the computer.**
