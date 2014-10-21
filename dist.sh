#!/bin/bash

python setup.py py2app
mv dist/webcronic.app dist/Webcronic.app
(cd dist && zip -r webcronic.app.zip Webcronic.app)