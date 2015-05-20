#!/usr/bin/env python

import shutil
import os

shutil.rmtree('admin')
shutil.rmtree('java')
shutil.rmtree('css')
shutil.rmtree('filetree')
shutil.rmtree('fonts')
shutil.rmtree('images')
shutil.rmtree('js')
shutil.rmtree('jspanel')

os.remove('local_settings.pyc')
