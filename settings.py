#!/usr/bin/env python
import os

STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
IMAGE_DIR = os.path.join(STATIC_ROOT, 'images')
SCRIPT_DIR = os.path.join(STATIC_ROOT, 'js')
STYLE_DIR = os.path.join(STATIC_ROOT, 'css')
