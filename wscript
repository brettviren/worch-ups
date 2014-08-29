#!/usr/bin/env python
# encoding: utf-8

import os
import sys

top = '.'
out = 'tmp'

### old way to set up worch environment: 
# if not os.path.exists('worch'):
#     assert 0 == os.system('git clone https://github.com/brettviren/worch.git')
# mydir = os.path.realpath('.')
# sys.path.insert(0,os.path.join(mydir,'worch'))
## new way:
# virtualenv venv
# source venv/bin/activate
# pip install git+git://github.com/brettviren/worch.git
###

def options(opt):
    opt.load('orchlib', tooldir='.')

def configure(cfg):
    cfg.load('orchlib', tooldir='.')

def build(bld):
    bld.load('orchlib', tooldir='.')
