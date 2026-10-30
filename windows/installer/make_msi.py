#!/usr/bin/env python3
"""Build UzbekLatin.msi — one MSI that installs either Uzbek Latin layout.

Runs inside the Docker image from ./Dockerfile (use ./build.sh). Two steps:

1. wixl (msitools) builds the base MSI: files, registry, embedded cab and the
   standard install sequences. wixl cannot build dialogs, so
2. the installer screens are written as raw MSI tables (.idt files) and
   imported with msibuild.

The installer asks for the UI language (Uzbek by default, Russian, English),
then which layout to install (Uzbek Latin Direct by default, or AltGr).

All UI text is in STRINGS; the Uzbek text uses the new Latin alphabet
(ö ğ ş ç). Uzbek and Russian together need a Unicode database, so the MSI
uses code page 65001 (UTF-8).
"""
import hashlib
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "UzbekLatin.msi"
WORK = HERE / "build"

VERSION = "1.0.2"
UPGRADE_CODE = "D74A6185-9BE0-4D69-9479-B7A8F5231B5E"
MANUFACTURER = "Azamat Musakhanov"
PRODUCT = "Uzbek Latin Keyboard"
CODEPAGE = 65001

LANGS = ("uz", "ru", "en")          # first one is the default UI language


def keys(text):
    # no line breaks inside "AltGr + \ = x"
    return text.replace(" = ", " = ").replace("AltGr + ", "AltGr + ")


STRINGS = {
    "T_TITLE": (
        "Özbek lotin klaviaturasi",
        "Узбекская латинская раскладка",
        "Uzbek Latin Keyboard"),
    "T_LAYOUT_HEAD": (
        "Qaysi klaviatura tartibini örnatamiz?",
        "Какую раскладку установить?",
        "Which keyboard layout should be installed?"),
    "T_ALTGR_LABEL": (
        "Uzbek Latin (AltGr) — dasturçilar uçun",
        "Uzbek Latin (AltGr) — для программистов",
        "Uzbek Latin (AltGr) — for programmers"),
    "T_DIRECT_DESC": tuple(map(keys, (
        "Harflar alohida tugmalarda: [ = ğ, ] = ö, ; = ş, ' = ç (Shift bilan bosh harf), "
        "\\ = ; va :. AltGr: [ ] { } ' \" | öşa tugmalarda, AltGr + \\ = \", AltGr + / = \\. "
        "Tavsiya etiladi.",
        "Буквы на отдельных клавишах: [ = ğ, ] = ö, ; = ş, ' = ç (с Shift заглавные), "
        "\\ = ; и :. AltGr: [ ] { } ' \" | на тех же клавишах, AltGr + \\ = \", AltGr + / = \\. "
        "Рекомендуется.",
        "Letters on their own keys: [ = ğ, ] = ö, ; = ş, ' = ç (Shift for capitals), "
        "\\ = ; and :. AltGr: [ ] { } ' \" | on the same keys, AltGr + \\ = \", AltGr + / = \\. "
        "Recommended."))),
    "T_ALTGR_DESC": (
        "ş ç ğ ö harflari öng Alt (AltGr) + S, C, G, O bilan yoziladi. "
        "Qavslar va tiniş belgilari öz joyida qoladi.",
        "Буквы ş ç ğ ö набираются правым Alt (AltGr) + S, C, G, O. "
        "Скобки и знаки препинания остаются на своих местах.",
        "The letters ş ç ğ ö are typed with Right Alt (AltGr) + S, C, G, O. "
        "Brackets and punctuation stay where they are."),
    "T_BACK": ("< Orqaga", "< Назад", "< Back"),
    "T_INSTALL": ("Örnatiş", "Установить", "Install"),
    "T_CANCEL": ("Bekor qiliş", "Отмена", "Cancel"),
    "T_FINISH": ("Tayyor", "Готово", "Finish"),
    "T_REMOVE": ("Öçiriş", "Удалить", "Remove"),
    "T_PROGRESS": (
        "Örnatilmoqda, iltimos kuting...",
        "Идёт установка, подождите...",
        "Installing, please wait..."),
    "T_DONE_HEAD": ("Örnatiş tugadi", "Установка завершена", "Installation complete"),
    "T_RESTART": (
        "Kompyuterni qayta işga tuşiring!",
        "Перезагрузите компьютер!",
        "Restart the computer!"),
    "T_DONE_BODY": (
        "Qayta işga tuşirgandan söng tartibni Win + Space bilan tanlang. Kompyuterdagi boşqa "
        "foydalanuvçilar uni özlari qöşadi: Settings > Time and Language > Language and "
        "region > Uzbek (Latin) > Language options > Add a keyboard.",
        "После перезагрузки выберите раскладку сочетанием Win + Пробел. Другие пользователи "
        "компьютера добавляют её сами: Параметры > Время и язык > Язык и регион > "
        "Узбекский (латиница) > Параметры языка > Добавить клавиатуру.",
        "After the restart, select the layout with Win + Space. Other users of this PC add "
        "it themselves: Settings > Time and Language > Language and region > Uzbek (Latin) "
        "> Language options > Add a keyboard."),
    "T_MAINT_HEAD": (
        "Klaviatura tartibi allaqaçon örnatilgan",
        "Раскладка уже установлена",
        "The layout is already installed"),
    "T_MAINT_BODY": (
        "Uni öçiriş uçun «Öçiriş» tugmasini bosing. Boşqa tartibni örnatiş uçun "
        "avval şu tartibni öçiring, söng örnatuvçini qayta işga tuşiring.",
        "Чтобы удалить её, нажмите «Удалить». Чтобы установить другую раскладку, сначала "
        "удалите эту, затем снова запустите установщик.",
        "Click Remove to uninstall it. To install the other layout, remove this one first, "
        "then run the installer again."),
    "T_REMOVING": (
        "Öçirilmoqda, iltimos kuting...",
        "Идёт удаление, подождите...",
        "Removing, please wait..."),
    "T_REMOVED_HEAD": ("Öçirildi", "Удалено", "Removed"),
    "T_REMOVED_BODY": (
        "Klaviatura tartibi öçirildi.",
        "Раскладка удалена.",
        "The keyboard layout was removed."),
    "T_CANCELLED": (
        "Örnatiş bekor qilindi. Kompyuterga heç narsa örnatilmadi.",
        "Установка отменена. Ничего не было установлено.",
        "Setup was cancelled. Nothing was installed."),
    "T_FATAL": (
        "Örnatişda xatolik yuz berdi. Kompyuterga heç narsa örnatilmadi.",
        "При установке произошла ошибка. Ничего не было установлено.",
        "Setup failed. Nothing was installed."),
}

# On MaintDlg -> Remove, these display properties take the "removing" texts.
REMOVE_OVERRIDES = {"T_PROGRESS": "T_REMOVING",
                    "T_DONE_HEAD": "T_REMOVED_HEAD",
                    "T_DONE_BODY": "T_REMOVED_BODY"}

# id, component condition ("OR REMOVE" so uninstall can always remove it), dll, source folder
LAYOUTS = [
    ("Direct", 'LAYOUT <> "altgr" OR REMOVE', "UzLatDir.dll", HERE.parent / "uzlatdir"),
    ("AltGr", 'LAYOUT = "altgr" OR REMOVE', "UzLat.dll", HERE.parent / "uzlat"),
]

# Registering the layout and adding it to the user's keyboard list is done by
# KbdMsi.dll, Microsoft's custom-action DLL from MSKLC (Microsoft-signed). It is
# copied unchanged out of the MSKLC-built MSI and called exactly as MSKLC does.
MSKLC_MSI = HERE.parent / "uzlatdir" / "UzLatDir_amd64.msi"
LCID = "0443"   # Uzbek (Latin)

# ---------------------------------------------------------------- base (wixl)

def guid(name):
    return str(uuid.uuid5(uuid.UUID(UPGRADE_CODE), name)).upper()


def xml(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def base_wxs():
    comps64, comps32, refs = [], [], []
    for lid, cond, dll, src in LAYOUTS:
        comps64.append(f"""
        <Component Id="c{lid}64" Guid="{guid(lid + '64')}" Win64="yes">
          <File Id="f{lid}64" Name="{dll}" Source="{src / 'amd64' / dll}" KeyPath="yes" />
        </Component>""")
        comps32.append(f"""
        <Component Id="c{lid}32" Guid="{guid(lid + '32')}">
          <File Id="f{lid}32" Name="{dll}" Source="{src / 'wow64' / dll}" KeyPath="yes" />
        </Component>""")
        refs += [f'<ComponentRef Id="c{lid}64" />', f'<ComponentRef Id="c{lid}32" />']
    return f"""<?xml version="1.0" encoding="utf-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="{PRODUCT}" Language="1091" Version="{VERSION}"
           Manufacturer="{MANUFACTURER}" UpgradeCode="{UPGRADE_CODE}">
    <Package InstallerVersion="500" Compressed="yes" InstallScope="perMachine"
             Description="Uzbek Latin keyboard layouts (Direct and AltGr)" Manufacturer="{MANUFACTURER}" />
    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
    <Media Id="1" Cabinet="layouts.cab" EmbedCab="yes" />
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="System64Folder">{''.join(comps64)}
      </Directory>
      <Directory Id="SystemFolder">{''.join(comps32)}
      </Directory>
    </Directory>
    <Feature Id="Main" Level="1">
      {chr(10).join('      ' + r for r in refs).strip()}
    </Feature>
  </Product>
</Wix>
"""

# ------------------------------------------------------------- UI (.idt)

def write_idt(name, cols, types, keys, rows):
    def cell(v):
        v = "" if v is None else str(v)
        assert "\t" not in v and "\n" not in v, (name, v)
        return v
    lines = ["\t".join(cols), "\t".join(types), "\t".join([name] + keys)]
    lines += ["\t".join(cell(c) for c in r) for r in rows]
    (WORK / f"{name}.idt").write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")


# Control attribute bits
VIS, EN, NOPREFIX, PROGRESS_BLOCKS = 1, 2, 0x20000, 0x10000
TEXT, BTN, GROUP, LINE, BAR = VIS | EN | NOPREFIX, VIS | EN, VIS | EN, VIS, VIS | PROGRESS_BLOCKS
MODAL, MODELESS = 3, 1

dialogs, controls, events, mappings, radios = [], [], [], [], []


def dialog(id_, first, default, cancel, attrs=MODAL):
    dialogs.append((id_, 50, 50, 370, 270, attrs, "[T_TITLE]", first, default, cancel))


def ctl(dlg, id_, type_, x, y, w, h, attrs, text="", prop=None, nxt=None):
    controls.append((dlg, id_, type_, x, y, w, h, attrs, prop, text, nxt, None))


def ev(dlg, control, event, arg, cond="1", order=1):
    events.append((dlg, control, event, arg, cond, order))


def msi_escape(text):
    # SetProperty arguments are Formatted: [\x] gives a literal x
    return "".join(f"[\\{c}]" if c in "[]{}" else c for c in text)


def line(dlg):
    ctl(dlg, "Line", "Line", 0, 234, 370, 0, LINE)


def build_ui():
    # 1. language
    dialog("LangDlg", "Lang", "Next", "Cancel")
    ctl("LangDlg", "Head", "Text", 20, 20, 330, 40, TEXT,
        r"{\Bold}Tilni tanlang / Выберите язык / Choose language")
    ctl("LangDlg", "Lang", "RadioButtonGroup", 40, 75, 290, 70, GROUP, prop="LANG", nxt="Next")
    line("LangDlg")
    ctl("LangDlg", "Next", "PushButton", 214, 243, 66, 17, BTN, "OK", nxt="Cancel")
    ctl("LangDlg", "Cancel", "PushButton", 290, 243, 66, 17, BTN, "[T_CANCEL]", nxt="Lang")
    for n, (val, label) in enumerate([("uz", "Özbekça"), ("ru", "Русский"), ("en", "English")], 1):
        radios.append(("LANG", n, val, 0, 24 * (n - 1), 290, 18, label, None))
    for i, lang in enumerate(LANGS):
        for key, vals in STRINGS.items():
            ev("LangDlg", "Next", f"[{key}]", msi_escape(vals[i]), f'LANG = "{lang}"', 1)
    ev("LangDlg", "Next", "NewDialog", "LayoutDlg", "NOT Installed", 2)
    ev("LangDlg", "Next", "NewDialog", "MaintDlg", "Installed", 2)
    ev("LangDlg", "Cancel", "EndDialog", "Exit")

    # 2. layout
    dialog("LayoutDlg", "Layout", "Install", "Cancel")
    ctl("LayoutDlg", "Head", "Text", 20, 15, 330, 30, TEXT, r"{\Bold}[T_LAYOUT_HEAD]")
    ctl("LayoutDlg", "Layout", "RadioButtonGroup", 20, 55, 330, 150, GROUP, prop="LAYOUT", nxt="Back")
    ctl("LayoutDlg", "DirectDesc", "Text", 38, 73, 312, 45, TEXT, "[T_DIRECT_DESC]")
    ctl("LayoutDlg", "AltGrDesc", "Text", 38, 148, 312, 45, TEXT, "[T_ALTGR_DESC]")
    line("LayoutDlg")
    ctl("LayoutDlg", "Back", "PushButton", 142, 243, 66, 17, BTN, "[T_BACK]", nxt="Install")
    ctl("LayoutDlg", "Install", "PushButton", 214, 243, 66, 17, BTN, "[T_INSTALL]", nxt="Cancel")
    ctl("LayoutDlg", "Cancel", "PushButton", 290, 243, 66, 17, BTN, "[T_CANCEL]", nxt="Layout")
    radios.append(("LAYOUT", 1, "direct", 0, 0, 330, 16, "Uzbek Latin Direct", None))
    radios.append(("LAYOUT", 2, "altgr", 0, 75, 330, 16, "[T_ALTGR_LABEL]", None))
    ev("LayoutDlg", "Back", "NewDialog", "LangDlg")
    ev("LayoutDlg", "Install", "EndDialog", "Return")
    ev("LayoutDlg", "Cancel", "EndDialog", "Exit")

    # already installed -> remove
    dialog("MaintDlg", "Remove", "Remove", "Cancel")
    ctl("MaintDlg", "Head", "Text", 20, 20, 330, 30, TEXT, r"{\Bold}[T_MAINT_HEAD]")
    ctl("MaintDlg", "Body", "Text", 20, 60, 330, 120, TEXT, "[T_MAINT_BODY]")
    line("MaintDlg")
    ctl("MaintDlg", "Remove", "PushButton", 214, 243, 66, 17, BTN, "[T_REMOVE]", nxt="Cancel")
    ctl("MaintDlg", "Cancel", "PushButton", 290, 243, 66, 17, BTN, "[T_CANCEL]", nxt="Remove")
    for target, src in REMOVE_OVERRIDES.items():
        ev("MaintDlg", "Remove", f"[{target}]", f"[{src}]", "1", 1)
    ev("MaintDlg", "Remove", "Remove", "ALL", "1", 2)
    ev("MaintDlg", "Remove", "EndDialog", "Return", "1", 3)
    ev("MaintDlg", "Cancel", "EndDialog", "Exit")

    # progress (modeless, shown while files are copied)
    dialog("ProgressDlg", "Bar", None, None, MODELESS)
    ctl("ProgressDlg", "Head", "Text", 20, 40, 330, 30, TEXT, r"{\Bold}[T_PROGRESS]")
    ctl("ProgressDlg", "Bar", "ProgressBar", 20, 90, 330, 15, BAR, "Progress")
    line("ProgressDlg")
    mappings.append(("ProgressDlg", "Bar", "SetProgress", "Progress"))

    # end screens
    for dlg, head, body in [("ExitDlg", "T_DONE_HEAD", "T_DONE_BODY"),
                            ("UserExitDlg", None, "T_CANCELLED"),
                            ("FatalErrorDlg", None, "T_FATAL")]:
        dialog(dlg, "Finish", "Finish", "Finish")
        if head:
            ctl(dlg, "Head", "Text", 20, 20, 330, 30, TEXT, rf"{{\Bold}}[{head}]")
        if dlg == "ExitDlg":
            ctl(dlg, "Restart", "Text", 20, 55, 330, 25, TEXT, r"{\Bold}[T_RESTART]")
        ctl(dlg, "Body", "Text", 20, 90 if dlg == "ExitDlg" else 60 if head else 30,
            330, 140, TEXT, f"[{body}]")
        line(dlg)
        ctl(dlg, "Finish", "PushButton", 290, 243, 66, 17, BTN, "[T_FINISH]", nxt="Finish")
        ev(dlg, "Finish", "EndDialog", "Return")

    WORK.mkdir(exist_ok=True)
    write_idt("Dialog",
              ["Dialog", "HCentering", "VCentering", "Width", "Height", "Attributes", "Title",
               "Control_First", "Control_Default", "Control_Cancel"],
              ["s72", "i2", "i2", "i2", "i2", "I4", "L128", "s50", "S50", "S50"],
              ["Dialog"], dialogs)
    write_idt("Control",
              ["Dialog_", "Control", "Type", "X", "Y", "Width", "Height", "Attributes",
               "Property", "Text", "Control_Next", "Help"],
              ["s72", "s50", "s20", "i2", "i2", "i2", "i2", "I4", "S72", "L0", "S50", "L50"],
              ["Dialog_", "Control"], controls)
    write_idt("ControlEvent",
              ["Dialog_", "Control_", "Event", "Argument", "Condition", "Ordering"],
              ["s72", "s50", "s50", "s255", "S255", "I2"],
              ["Dialog_", "Control_", "Event", "Argument", "Condition"], events)
    write_idt("EventMapping",
              ["Dialog_", "Control_", "Event", "Attribute"],
              ["s72", "s50", "s50", "s50"],
              ["Dialog_", "Control_", "Event"], mappings)
    write_idt("RadioButton",
              ["Property", "Order", "Value", "X", "Y", "Width", "Height", "Text", "Help"],
              ["s72", "i2", "s64", "i2", "i2", "i2", "i2", "L64", "L50"],
              ["Property", "Order"], radios)
    write_idt("TextStyle",
              ["TextStyle", "FaceName", "Size", "Color", "StyleBits"],
              ["s72", "s32", "i2", "I4", "I2"],
              ["TextStyle"],
              [("Def", "Segoe UI", 9, None, None), ("Bold", "Segoe UI", 12, None, 1)])

# ------------------------------------------------------------------ helpers

def run(*cmd, cwd=None):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True, cwd=cwd)


def export_rows(msi, table):
    """Rows of an existing table, keyed by its first column."""
    WORK.mkdir(exist_ok=True)   # export also dumps binary streams into ./Binary/
    out = subprocess.run(["msiinfo", "export", str(msi), table], cwd=WORK,
                         check=True, capture_output=True, text=True).stdout
    lines = out.replace("\r", "").split("\n")
    header, rows = lines[:3], [l.split("\t") for l in lines[3:] if l]
    return header, rows


def reimport(msi, table, header, rows):
    text = "\r\n".join(header + ["\t".join(r) for r in rows]) + "\r\n"
    (WORK / f"{table}.idt").write_text(text, encoding="utf-8")
    run("msibuild", msi, "-i", WORK / f"{table}.idt")


def kbdmsi_dll():
    """KbdMsi.dll bytes, taken from the MSKLC-built MSI's Binary table."""
    _, rows = export_rows(MSKLC_MSI, "Binary")
    name = next(r[0] for r in rows if r[0].startswith("CustomActionDll"))
    data = subprocess.run(["msiinfo", "extract", str(MSKLC_MSI), f"Binary.{name}"],
                          check=True, capture_output=True).stdout
    assert data[:2] == b"MZ" and "KbdMsi.dll".encode("utf-16-le") in data, "not KbdMsi.dll"
    return data


def check_strings():
    for key, vals in STRINGS.items():
        assert len(vals) == len(LANGS), key
        for lang, v in zip(LANGS, vals):
            if len(msi_escape(v)) > 255:
                sys.exit(f"{key}/{lang}: {len(msi_escape(v))} chars (with [\\x] escapes), "
                         "MSI limit for this text is 255")


def main():
    check_strings()
    WORK.mkdir(exist_ok=True)
    for lid, *_, src in LAYOUTS:
        for arch in ("amd64", "wow64"):
            if not any((src / arch).glob("*.dll")):
                sys.exit(f"missing {src / arch} — build the layout with MSKLC first")

    (WORK / "base.wxs").write_text(base_wxs(), encoding="utf-8")
    msi = WORK / "UzbekLatin.msi"
    run("wixl", "-a", "x64", "-o", msi, WORK / "base.wxs")

    (WORK / "_ForceCodepage.idt").write_text(f"\r\n\r\n{CODEPAGE}\t_ForceCodepage\r\n", encoding="ascii")
    run("msibuild", msi, "-i", WORK / "_ForceCodepage.idt")

    # Component conditions (wixl has no <Condition>): pick the chosen layout
    header, rows = export_rows(msi, "Component")
    col = header[0].split("\t").index("Condition")
    conds = {f"c{lid}{bits}": cond for lid, cond, *_ in LAYOUTS for bits in ("64", "32")}
    for r in rows:
        r += [""] * (len(header[0].split("\t")) - len(r))
        if r[0] in conds:
            r[col] = conds.pop(r[0])
        if r[0].endswith("32"):
            r[3] = "0"          # wixl -a x64 marks every component 64-bit
    assert not conds, f"components not found: {conds}"
    reimport(msi, "Component", header, rows)

    build_ui()
    for t in ("Dialog", "Control", "ControlEvent", "EventMapping", "RadioButton", "TextStyle"):
        run("msibuild", msi, "-i", WORK / f"{t}.idt")

    # Property: add UI defaults (Uzbek), choices, and mark LAYOUT secure
    header, rows = export_rows(msi, "Property")
    props = dict((r[0], r[1]) for r in rows)
    props.update({"DefaultUIFont": "Def", "LANG": LANGS[0], "LAYOUT": "direct",
                  "ARPNOMODIFY": "1", "ARPNOREPAIR": "1"})
    props.update({k: v[0] for k, v in STRINGS.items()})
    secure = [s for s in props.get("SecureCustomProperties", "").split(";") if s]
    props["SecureCustomProperties"] = ";".join(dict.fromkeys(secure + ["LAYOUT"]))
    reimport(msi, "Property", header, [[k, v] for k, v in props.items()])

    # InstallUISequence: show our dialogs
    header, rows = export_rows(msi, "InstallUISequence")
    rows = [r for r in rows if r[0] not in {"LangDlg", "ProgressDlg", "ExitDlg",
                                            "UserExitDlg", "FatalErrorDlg"}]
    seq = {r[0]: int(r[2]) for r in rows if r[2].lstrip("-").isdigit()}
    rows += [["LangDlg", "NOT REMOVE", str(seq["CostFinalize"] + 50)],
             ["ProgressDlg", "", str(seq["ExecuteAction"] - 10)],
             ["ExitDlg", "", "-1"], ["UserExitDlg", "", "-2"], ["FatalErrorDlg", "", "-3"]]
    reimport(msi, "InstallUISequence", header, rows)

    # Ask to restart after an interactive install (UILevel 5 = full UI), so
    # silent installs (/qn) never reboot on their own.
    header, rows = export_rows(msi, "InstallExecuteSequence")
    finalize = next(int(r[2]) for r in rows if r[0] == "InstallFinalize")
    rows = [r for r in rows if r[0] != "ScheduleReboot"]
    rows.append(["ScheduleReboot", "NOT REMOVE AND UILevel = 5", str(finalize + 50)])

    # KbdMsi custom actions, same entry points, types and timing as MSKLC:
    #   CA01 register layout (deferred, as SYSTEM; data = "<dll path>|<LCID>")
    #   CA03 add it to the installing user's keyboard list (deferred, as user)
    #   CA04 remove it from the user's list, CA02 unregister (on uninstall)
    installing = " OR ".join(f"$c{lid}64 = 3" for lid, *_ in LAYOUTS)
    removing = " OR ".join(f"$c{lid}64 = 2" for lid, *_ in LAYOUTS)
    actions = [("KbdRemoveFromList", 1025, "KbdMsi", "CA04", removing, 3450)]
    for n, (lid, *_rest) in enumerate(LAYOUTS):
        actions.append((f"KbdSetData{lid}", 51, "KbdRegister", f"[#f{lid}64]|{LCID}",
                        f"$c{lid}64 = 3", 4030 + n))
    actions += [("KbdRegister", 3073, "KbdMsi", "CA01", installing, 4050),
                ("KbdUnregister", 3073, "KbdMsi", "CA02", removing, 4060),
                ("KbdAddToList", 1025, "KbdMsi", "CA03", installing, 4065)]
    rows = [r for r in rows if not r[0].startswith("Kbd")]
    rows += [[a, cond, str(seq)] for a, _t, _s, _tg, cond, seq in actions]
    reimport(msi, "InstallExecuteSequence", header, rows)
    write_idt("CustomAction", ["Action", "Type", "Source", "Target"],
              ["s72", "i2", "S72", "S255"], ["Action"],
              [(a, t, src, tg) for a, t, src, tg, _c, _q in actions])
    run("msibuild", msi, "-i", WORK / "CustomAction.idt")

    # Binary table with KbdMsi.dll (binary cells reference files in WORK/Binary/)
    (WORK / "Binary").mkdir(exist_ok=True)
    (WORK / "Binary" / "KbdMsi.dll").write_bytes(kbdmsi_dll())
    write_idt("Binary", ["Name", "Data"], ["s72", "v0"], ["Name"], [("KbdMsi", "KbdMsi.dll")])
    run("msibuild", msi, "-i", "Binary.idt", cwd=WORK)   # msibuild reads Binary/ from cwd

    OUT.write_bytes(msi.read_bytes())
    # SHA-256 in sha256sum format, so `sha256sum -c UzbekLatin.msi.sha256` works
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    checksum = OUT.with_name(OUT.name + ".sha256")
    checksum.write_text(f"{digest}  {OUT.name}\n", encoding="ascii")
    print(f"\nbuilt {OUT} ({OUT.stat().st_size} bytes)\nSHA-256 {digest} -> {checksum.name}")


if __name__ == "__main__":
    main()
