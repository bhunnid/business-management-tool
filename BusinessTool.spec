# -*- mode: python ; coding: utf-8 -*-


import sys
from pathlib import Path

project_dir = Path(sys.argv[0]).resolve().parent
alembic_files = [
    (str(path), 'alembic')
    for path in (project_dir / 'alembic').rglob('*')
    if path.is_file()
]
qss_files = [
    (str(path), 'app/ui/design_system')
    for path in (project_dir / 'app/ui/design_system').rglob('*.qss')
    if path.is_file()
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        (str(project_dir / 'alembic.ini'), '.'),
        *alembic_files,
        *qss_files,
    ],
    hiddenimports=[
        'logging.config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BusinessTool',
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
)
