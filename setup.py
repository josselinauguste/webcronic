from setuptools import setup

APP = ['webcronic.py']
DATA_FILES = [
    'webcronic-small.png',
    'icon.icns'
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'includes': ['keychain']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
