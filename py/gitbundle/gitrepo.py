# -*- coding: utf-8 -*-
#
# gitbundle/gitrepo.py
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


import git
import re
from git import repo
 
class GitRepo:
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


    def update_repository(self, repo_path:str) -> None:
        """
        Updates local repository according to the latest remote repository state.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
        """
        self.update_remote_branch_info(repo_path)
        remote_branch_list = self.get_remote_branch_list(repo_path)
        local_branch_list  = self.get_local_branch_list(repo_path)
        self.delete_remotely_deleted_branch(repo_path, remote_branch_list, local_branch_list)
        self.add_remotely_added_branch(repo_path, remote_branch_list, local_branch_list)
        

    def update_remote_branch_info(self, repo_path:str) -> None:
        """
        Updates branch information of local repository according to the latest remote repository, i.e.
        deletes remotely deleted branches and add remotely added branches.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
        """
        repo        = git.Repo(repo_path)
        
        repo.git.fetch('--prune')
        # the commmand return contains deleted branch information which can be used for
        # local branch management (removal) 

        # @TODO: for tag removal. 
        #repo.git.fetch("remotes/origin", "--prune", "'refs/tags/*:refs/tags/*'")


    def get_remote_branch_list(self, repo_path:str) -> list:
        """
        Retrieves latest list of branches in remote repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.

        Returns
        ----------
            remote_branch_list : list
                list of remote branches
        """
        repo        = git.Repo(repo_path)
        remote_branch_list = repo.git.branch('-r').replace('\r\n','\n').replace('* ','').replace(' ','').split('\n')
        for i in range(len(remote_branch_list)):
            remote_branch_list[i] = 'remotes/' + remote_branch_list[i]
            if re.search(r'HEAD', remote_branch_list[i]):
               del remote_branch_list[i]

        return remote_branch_list


    def get_local_branch_list(self, repo_path:str) -> list:
        """
        Retrieves latest list of branches in local repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.

        Returns
        ----------
            local_branch_list : list
                list of local branches
        """
        repo        = git.Repo(repo_path)
        local_branch_list = repo.git.branch('-l').replace('\r\n','\n').replace('* ','').replace(' ','').split('\n')
        for remote_branch in local_branch_list:
            if re.search(r'HEAD', remote_branch):
               del local_branch_list[local_branch_list.index(remote_branch)]

        return local_branch_list



    def delete_remotely_deleted_branch(self, repo_path:str, remote_branch_list:list, local_branch_list:list) -> None:
        """
        Delete branches that don't exist in remote repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
            remote_branch_list : list
                list of local branches
            local_branch_list : list
                list of local branches
        """        
        repo        = git.Repo(repo_path)
        
        for local_branch in local_branch_list:
            for remote_branch in remote_branch_list:
                if remote_branch == 'remotes/origin/' + local_branch:
                    pass
                else:
                    repo.git.branch('-d', local_branch)
                    
        
    def add_remotely_added_branch(self, repo_path:str, remote_branch_list:list, local_branch_list:list) -> None:
        """
        Adds/creates branches that only exists in remote repository.
        
        Parameters
        ----------
            repo_path : str
                Directory path to the repository.
            remote_branch_list : list
                list of local branches
            local_branch_list : list
                list of local branches
        """
        repo        = git.Repo(repo_path)
        
        for remote_branch in remote_branch_list:
            for local_branch in local_branch_list:
                if remote_branch == 'remotes/origin/' + local_branch:
                    pass
                else:
                    repo.git.checkout('-b', local_branch, remote_branch)
                    


