#! /bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
python3 digital_sign_builder.py
