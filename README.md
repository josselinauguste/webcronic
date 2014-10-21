# Introduction

Notify when a [webcron](https://www.webcron.org) monitor goes down.

## Configuration

You have to create an element called 'webcronic' in the MacOS keychain containing your API credentials.

## Developement

### Required

- PyObjC
- py2app
- rumps (this fork: https://github.com/tito/rumps)

### Launch app in dev mode

    python webcronic.py

### Package the app

    python setup.py py2app


Thanks @jaredks for providing rumps. It's very simple and helpful.