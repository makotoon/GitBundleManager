# -*- coding: utf-8 -*-
#
# gitbundle/gitrepo.py
# (https://github.com/makotoon/git_bundle_manager)
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


import git
import re
 
class gitrepo:
    """
    Git repository manager module.

    This is a simple module to handle minor operations using GitPython.
    """

    def find_branch_origin(self, repo_path, branch_name) -> str:
        """
        Finds the HASH ID (SHA-1) of the commit from which a specified branch originated.

        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
            branch_name : str
                Branch name to check the origin.

        Returns
        ----------
            commit_id_origin : str
                Commit ID (SHA-1 HASH) of the root origin of the specified branch.

        Notes
        ----------
            This implementation uses git reflog to determine the origin of 
            a branch and is subject to any limitations of the command.
        """

        repo        = git.Repo(repo_path)
        try:
            reflog      = repo.git.reflog(('show','--no-abbrev', branch_name))
            reflog_list = reflog.split("\n") 
            for ref in reflog_list:
                if re.search(r'branch: Created from', ref):
                    commit_id_origin = ref.split()[0]
            
            if not('commit_id_origin' in locals()):
                commit_id_origin = 'NOORIGIN'
        except:
            commit_id_origin = 'NOORIGIN'
            pass
                 
        return commit_id_origin
        

    def find_branch(self, repo_path:str, branch_name:str) -> bool:
        """
        Finds if specified branch exists in the specified repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
            branch_name : str
                Branch name to check.

        Returns
        ----------
            exist : bool
                True if specified branch exists in the repository. False otherwise.
        """
        
        repo        = git.Repo(repo_path)
        
        try:
            repo.rev_parse(branch_name)
            exist = True
        except:
            exist = False

        return exist

        
    def find_commit_id(self, repo_path:str, commit_id:str) -> bool:
        """
        Finds if specified branch exists in the specified repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
            commit_id : str
                Commit ID (SHA1 HASH) to check.

        Returns
        ----------
            exist : bool
                True if specified branch exists in the repository. False otherwise.
        """
        
        repo        = git.Repo(repo_path)
        
        try:
            repo.rev_parse(commit_id)
            exist = True
        except:
            exist = False

        return exist



