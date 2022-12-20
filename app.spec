# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [
    ('assets/textures/splash.png', './assets/textures/splash.png', "DATA"),
    ('assets/textures/icon.ico', './assets/textures/icon.ico', "DATA"),
    ('assets/ui/mainwindow.ui', './assets/ui/mainwindow.ui', "DATA"),
    ('assets/ui/add.ui', './assets/ui/add.ui', "DATA"),
    ('assets/ui/calendar.ui', './assets/ui/calendar.ui', "DATA"),
    ('assets/ui/preferences.ui', './assets/ui/preferences.ui', "DATA"),
    ('assets/lang/lang.json', './assets/lang/lang.json', "DATA")
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='N-TECH Package Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./assets/textures/icon.ico'],
)
