# Uzbek Latin AltGr Keyboard Setup for Linux

This guide configures a normal **US keyboard layout** for programming while adding Uzbek Latin letters through **Right Alt (`AltGr`)**.

The result:

| Key combination | Character |
|---|---|
| `RightAlt + O` | `ö` |
| `RightAlt + Shift + O` | `Ö` |
| `RightAlt + G` | `ğ` |
| `RightAlt + Shift + G` | `Ğ` |
| `RightAlt + S` | `ş` |
| `RightAlt + Shift + S` | `Ş` |
| `RightAlt + C` | `ç` |
| `RightAlt + Shift + C` | `Ç` |

Normal US keys remain unchanged, so this setup is convenient for coding.

Tested with:

- Ubuntu 24.04
- GNOME
- Wayland
- libxkbcommon 1.6.0

---

## 1. Check that the session is Wayland

Run:

```bash
echo $XDG_SESSION_TYPE
```

Expected:

```text
wayland
```

---

## 2. Install XKB tools

On Ubuntu/Debian:

```bash
sudo apt install libxkbcommon-tools
```

---

## 3. Create user XKB directories

```bash
mkdir -p ~/.config/xkb/{symbols,rules}
```

---

## 4. Create the Uzbek symbol file

Create:

```text
~/.config/xkb/symbols/uzprog
```

with:

```xkb
partial alphanumeric_keys
xkb_symbols "letters" {
    key <AD09> { [ o, O, odiaeresis, Odiaeresis ] };
    key <AC05> { [ g, G, gbreve,     Gbreve     ] };
    key <AC02> { [ s, S, scedilla,   Scedilla   ] };
    key <AB03> { [ c, C, ccedilla,   Ccedilla   ] };
};
```

Or create it directly:

```bash
cat > ~/.config/xkb/symbols/uzprog <<'EOF_XKB'
partial alphanumeric_keys
xkb_symbols "letters" {
    key <AD09> { [ o, O, odiaeresis, Odiaeresis ] };
    key <AC05> { [ g, G, gbreve,     Gbreve     ] };
    key <AC02> { [ s, S, scedilla,   Scedilla   ] };
    key <AB03> { [ c, C, ccedilla,   Ccedilla   ] };
};
EOF_XKB
```

---

## 5. Create the custom XKB rules file

Create:

```text
~/.config/xkb/rules/evdev
```

with:

```text
! include %S/evdev

! option = symbols
  uzprog:letters = +uzprog(letters)
```

Or create it directly:

```bash
cat > ~/.config/xkb/rules/evdev <<'EOF_XKB'
! include %S/evdev

! option = symbols
  uzprog:letters = +uzprog(letters)
EOF_XKB
```

---

## 6. Configure GNOME

> [!IMPORTANT]
> If Anaconda or Conda is installed, it may provide its own `gsettings` command and shadow Ubuntu's system command.

Check:

```bash
type -a gsettings
```

If you see something similar to:

```text
/home/USER/anaconda3/bin/gsettings
/usr/bin/gsettings
```

use `/usr/bin/gsettings` explicitly in the commands below.

### Keep your existing layouts

For example, for English and Russian:

```bash
/usr/bin/gsettings set org.gnome.desktop.input-sources sources \
    "[('xkb', 'us'), ('xkb', 'ru')]"
```

If you use different layouts, keep your existing source list instead.

### Enable AltGr and the Uzbek mappings

```bash
/usr/bin/gsettings set org.gnome.desktop.input-sources xkb-options \
    "['lv3:ralt_switch', 'uzprog:letters']"
```

---

## 7. Verify GNOME settings

Check layouts:

```bash
/usr/bin/gsettings get org.gnome.desktop.input-sources sources
```

Example:

```text
[('xkb', 'us'), ('xkb', 'ru')]
```

Check XKB options:

```bash
/usr/bin/gsettings get org.gnome.desktop.input-sources xkb-options
```

Expected:

```text
['lv3:ralt_switch', 'uzprog:letters']
```

---

## 8. Verify dconf directly

```bash
dconf read /org/gnome/desktop/input-sources/sources
```

and:

```bash
dconf read /org/gnome/desktop/input-sources/xkb-options
```

Example:

```text
[('xkb', 'us'), ('xkb', 'ru')]
['lv3:ralt_switch', 'uzprog:letters']
```

If `gsettings` and `dconf` show different values, you are probably using a different `gsettings` binary, commonly because Conda/Anaconda shadows `/usr/bin/gsettings`.

Check with:

```bash
type -a gsettings
```

---

## 9. Test that XKB can compile the configuration

> [!IMPORTANT]
> Anaconda may also provide its own `xkbcli`.

Check:

```bash
type -a xkbcli
```

Use the system binary explicitly:

```bash
/usr/bin/xkbcli
```

Compile the keyboard map:

```bash
/usr/bin/xkbcli compile-keymap \
    --layout us \
    --options lv3:ralt_switch,uzprog:letters \
    >/tmp/uzbek-keymap.xkb
```

Check the generated keymap:

```bash
grep -E 'odiaeresis|gbreve|scedilla|ccedilla|ISO_Level3_Shift' \
    /tmp/uzbek-keymap.xkb
```

You should see entries containing:

```text
odiaeresis
Odiaeresis
gbreve
Gbreve
scedilla
Scedilla
ccedilla
Ccedilla
ISO_Level3_Shift
```

---

## 10. Test the actual live Wayland keymap

Run:

```bash
/usr/bin/xkbcli interactive-wayland
```

Press `RightAlt`.

It should report:

```text
ISO_Level3_Shift
```

Then test:

```text
RightAlt + o
RightAlt + g
RightAlt + s
RightAlt + c
```

Expected Unicode output:

```text
ö
ğ
ş
ç
```

Also test uppercase:

```text
RightAlt + Shift + o -> Ö
RightAlt + Shift + g -> Ğ
RightAlt + Shift + s -> Ş
RightAlt + Shift + c -> Ç
```

Exit with:

```text
Ctrl+C
```

---

## 11. Final key mapping

Normal US keys are unchanged:

```text
o -> o
g -> g
s -> s
c -> c
```

Uzbek letters:

```text
RightAlt + o -> ö
RightAlt + g -> ğ
RightAlt + s -> ş
RightAlt + c -> ç
```

Uppercase:

```text
RightAlt + Shift + o -> Ö
RightAlt + Shift + g -> Ğ
RightAlt + Shift + s -> Ş
RightAlt + Shift + c -> Ç
```

---

## 12. Optional: disable Conda `base` auto-activation

If Conda automatically activates `(base)` in every terminal, its programs may appear before system programs in `PATH`.

Disable automatic base activation:

```bash
conda config --set auto_activate_base false
```

Open a new terminal and check:

```bash
which gsettings
which xkbcli
```

Ideally:

```text
/usr/bin/gsettings
/usr/bin/xkbcli
```

---

## Troubleshooting

### Right Alt still produces `Alt_R`

Run:

```bash
/usr/bin/xkbcli interactive-wayland
```

If `RightAlt` reports:

```text
Alt_R
```

instead of:

```text
ISO_Level3_Shift
```

check:

```bash
/usr/bin/gsettings get org.gnome.desktop.input-sources xkb-options
```

It must contain:

```text
'lv3:ralt_switch'
```

### Custom letters compile but do not work in GNOME

Compare:

```bash
/usr/bin/gsettings get org.gnome.desktop.input-sources xkb-options
```

with:

```bash
dconf read /org/gnome/desktop/input-sources/xkb-options
```

They should be identical.

If they are not, run:

```bash
type -a gsettings
```

and make sure you are using:

```text
/usr/bin/gsettings
```

### `xkbcli` reports paths under Anaconda

If errors refer to a path such as:

```text
/home/USER/anaconda3/share/X11/xkb
```

use:

```bash
/usr/bin/xkbcli
```

instead of plain:

```bash
xkbcli
```

### Check the current desktop/session

```bash
echo $XDG_CURRENT_DESKTOP
echo $XDG_SESSION_DESKTOP
echo $DESKTOP_SESSION
echo $XDG_SESSION_TYPE
```

Typical Ubuntu GNOME Wayland values are similar to:

```text
XDG_CURRENT_DESKTOP=ubuntu:GNOME
XDG_SESSION_DESKTOP=ubuntu-wayland
DESKTOP_SESSION=ubuntu-wayland
XDG_SESSION_TYPE=wayland
```

---

## Files created by this setup

```text
~/.config/xkb/symbols/uzprog
~/.config/xkb/rules/evdev
```

No system XKB files under `/usr/share/X11/xkb` need to be modified.

---

## Removing the custom Uzbek mappings

Remove the custom XKB options:

```bash
/usr/bin/gsettings set org.gnome.desktop.input-sources xkb-options '[]'
```

If you had other XKB options before this setup, restore those instead of replacing the list with `[]`.

Optionally remove the custom files:

```bash
rm ~/.config/xkb/symbols/uzprog
rm ~/.config/xkb/rules/evdev
```

---

## Summary

This setup keeps a normal US programming keyboard and adds the Uzbek Latin characters through `AltGr`:

```text
AltGr + O -> Ö/ö
AltGr + G -> Ğ/ğ
AltGr + S -> Ş/ş
AltGr + C -> Ç/ç
```

This avoids switching to a separate Uzbek keyboard layout while coding.
