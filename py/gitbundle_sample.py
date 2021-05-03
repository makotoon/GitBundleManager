# -*- coding: utf-8 -*-
#
# gitbundle_sample.py
# (https://github.com/makotoon/GitBundleManager)
#
# ======================================================================================
# Copyright (c) 2021 Makoto Maeda
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense,and/or sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ======================================================================================

import sys
import gitbundle

def main():
    gbm_cfg = sys.argv[1]
    gbm     = gitbundle.GitBundleMng(gbm_cfg)

    if len(sys.argv) > 2:
       if "--update-repo" in sys.argv[2:]:
          gbm.update_repo()

       if "--mode=genbat" in sys.argv[2:]:
          gbm.create_batch(mode="bat")
          
       if "--mode=genbash" in sys.argv[2:]:
          gbm.create_batch(mode="sh")


if __name__=='__main__':
   main()