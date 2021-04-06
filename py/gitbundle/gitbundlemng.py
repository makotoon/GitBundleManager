# -*- coding: utf-8 -*-
#
# gitbundle/gitbundlemng.py
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


import json
import os
import re
import glob
import datetime
import gitbundle

class gitbundlemng:
    """
    Git bundle manager module.

    A simple module for git repository management on Windows.
    This along with the accompanying sample application and json configuration file generates
    Windows batch files to create or merge git bundle files for synchronization of isolated 
    git repository pairs.
    Repository pairs need to be defined in the json file and there's no limitation on the number
    of repository pairs to be defined.

    This module itself only outputs windows batch files and does not offer direct git operation
    as it is intended for use in restricted environments.

    Current implementation supports synchronization of one branch per json configuration.
    Multiple branches synchronization support is under consideration and may be supported 
    in future versions.
    """

    def __init__(self, cfg_file:str):
        # Read json configurations file specified by the first argument
        f = open(cfg_file, 'r')
        self._cfg = json.load(f)


    def create_batch(self):
        """ 
        Creates windows batch files for repository synchronization.
        """

        self.__create_dir(self._cfg['config_common']['batch_output'])
        self.__create_dir(self._cfg['config_common']['bundle_output'])

        fo = open("{0}/git_bundle_out.bat".format(self._cfg['config_common']['batch_output']), "w")
        fi = open("{0}/git_bundle_in.bat".format(self._cfg['config_common']['batch_output']), "w")
        
        gbr=gitbundle.gitrepo()

        for cfg in self._cfg['config_detail'].keys():
            fo.write('@rem ### git bundle commands for {0} \n'.format( cfg ))
            
            fo.write('@rem # Switch branch\n')
            fo.write('\"{0}\" {1} {2} checkout {3} \n'.format( 
                                                       self._cfg['config_common']['git_path'] , 
                                                       self._cfg['config_common']['git_option'],
                                                       self._cfg['config_detail'][cfg]['path'],
                                                       self._cfg['config_detail'][cfg]['target_branch']
                                                     ))

            fo.write('@rem # Pull remote repository updates\n')
            fo.write('\"{0}\" {1} {2} pull \n'.format( 
                                                       self._cfg['config_common']['git_path'] , 
                                                       self._cfg['config_common']['git_option'],
                                                       self._cfg['config_detail'][cfg]['path']
                                                     ))

            fo.write('@rem # Create bundle for branch {0}\n'.format(
                                                                    self._cfg['config_detail'][cfg]['target_branch']
                                                                    ))

            bundle_name   =  self.make_bundlename(self._cfg['config_detail'][cfg]['repository_name'], 
                                                  self._cfg['config_detail'][cfg]['target_branch'],
                                                  gbr.find_branch_origin( self._cfg['config_detail'][cfg]['path'] , 
                                                                          self._cfg['config_detail'][cfg]['target_branch'] ))
            
            fo.write('\"{0}\" {1} {2} bundle create {3}/{4} {5} {6} \n\n'.format( 
                                                                                 self._cfg['config_common']['git_path'] , 
                                                                                 self._cfg['config_common']['git_option'],
                                                                                 self._cfg['config_detail'][cfg]['path'],
                                                                                 self._cfg['config_common']['bundle_output'],
                                                                                 bundle_name,
                                                                                 self._cfg['config_common']['bundle_option'],
                                                                                 self._cfg['config_detail'][cfg]['target_branch']
                                                                                 ))

            """
            # TODO : to be implemented. need to parse bundle file name.

            fi.write('@rem ### git bundle commands for {0} \n'.format( cfg ))
            fi.write('@rem # Pull remote repository updates\n')
            fi.write('\"{0}\" {1} {2} pull \n'.format( 
                                                      self._cfg['config_common']['git_path'] , 
                                                      self._cfg['config_common']['git_option'],
                                                      self._cfg['config_detail'][cfg]['path']
                                                     ))

            fi.write('@rem # Switch to branch {0}\n'.format(
                                                             self._cfg['config_detail'][cfg]['target_branch']
                                                            ))

            fi.write('\"{0}\" {1} {2} checkout {3}\n'.format( 
                                                             self._cfg['config_common']['git_path'] , 
                                                             self._cfg['config_common']['git_option'],
                                                             self._cfg['config_detail'][cfg]['path'],
                                                             self._cfg['config_detail'][cfg]['target_branch']
                                                            ))



            fi.write('\"{0}\" {1} {2} pull {3} {4}/{5}.bundle {6} \n\n'.format( 
                                                                               self._cfg['config_common']['git_path'] , 
                                                                               self._cfg['config_common']['git_option'],
                                                                               self._cfg['config_detail'][cfg]['path'],
                                                                               self._cfg['config_common']['merge_option'],
                                                                               self._cfg['config_common']['merge_input'],
                                                                               self._cfg['config_detail'][cfg]['repository_name'], 
                                                                               self._cfg['config_detail'][cfg]['target_branch']
                                                                              ))
            """

        fo.close()
        fi.close()


    def get_bundle_list(self, bundle_dir:str):
        """ 
        Retrieves bundle file list.
        If there are multiple bundle files for the same repository and branch,
        only the most recent bundle file is returned

        Parameters
        ----------
            bundle_dir : str
                directory containing bundle files

        Returns
        ----------
            bundle_info_list : list
                list of bundle files 
        """
        bundle_dir = "C:/Data/repo/git/test/bundle_test/1"

        bundle_files = glob.glob(bundle_dir + '/*.bundle')
        bundle_info_list  = []

        for bundle_file in bundle_files:
            info = self.parse_bundle_name(bundle_file.replace(bundle_dir, '').replace('\\',''))
            for bundle_info in bundle_info_list:
                if    (bundle_info['repository_name'] == info['repository_name'])\
                  and (bundle_info['branch_name']     == info['branch_name']):
                    if int(bundle_info['time']) > int(info['time']):
                        bundle_info_list[bundle_info_list.index(bundle_info)] = bundle_file
                        break
            else:
                bundle_info_list.append(bundle_info)

        return bundle_info_list



    def get_branch_name_in_bundle(self, bundle_file:str):
        """ 
        Retrieves branch names and the corresponding SHA-1 (of the latest commits) in a bundle file

        Parameters
        ----------
            bundle_file : str
                File path to the git bundle file to analyze.

        Returns
        ----------
            branch_list : list
                List of branch names and SHA-1. Each list element holds a sublist with SHA-1 (element 0) and 
                branch name (element 1) in string. 
        """
        with open(bundle_file, 'rb') as frb:
            branch_list = []
            while True:
                line = frb.readline().decode().replace('\n', '')
                if re.match("^#\s", line):
                    # skip the fisrst (header) line
                    continue
                else:
                    if line == '':
                        break
                    else: 
                        branch_list.append(line.split())
        
        return branch_list

        
    def get_config(self):
        """
        Retrieves the current list of gitbundle configurations for individual respositories.

        Returns
        -----------
            _cfg_detail: dict
                list of repsoitory configurations
        """
        return self._cfg['config_detail']


    def parse_bundle_name(self, bundle_name:str):
        """
        Parses bundle information in the file name of a bundle.

        Parameters
        ----------
        bundle_name : str
            Bundle file name

        Returns
        ----------
        bundle_info : dict
            Bundle information. 
            key = 'repository_name', 'branch_name', 'branch_origin' (commit hash id), 'branch_datetime' (yyyymmddHHMMSS)
            bundle_info['branch_origin'] value of 'NOORIGIN' means there was no root commit found for the branch
        """
        bundle_info = {}
        
        bundle_name_sp = re.match('(.*).bundle', bundle_name).split('@')

        assert len(bundle_name_sp)    == 4,  'Illegal bundle file name (1)'
        assert len(bundle_name_sp[3]) == 12, 'Illegal bundle file name (2)'

        bundle_info['repository_name'] = bundle_name_sp[0]
        bundle_info['branch_name']     = bundle_name_sp[1].replace('+', '/')
        bundle_info['branch_origin']   = bundle_name_sp[2]
        bundle_info['bundle_datetime'] = bundle_name_sp[3]

        return bundle_info

            

    def make_bundlename(self, repository_name:str, branch_name:str, branch_origin:str):
        """ 
        Generates bundle file name.

        Parameters
        ----------
            repository_name : str
                name of repository
            branch_name   : str
                name of branch
            branch_origin : str
                commit id of branch origin

        Returns
        ----------
            bundle_name : str
                name of bundle

        Notes
        ----------
            bundle file naming convention
            
            <repository_name>@<branch_name>@<branch_origin>@<bundle_date>.bundle
            
            <repository_name>   : 
                identification of the repsitory from which the bundle file was created.
            <branch_name>       : 
                branch name of the bundle wherein "+" denotes "/", 
                e.g. branch feature/func_1 being feature+func_1 
            <branch_origin>     : 
                commit ID of the branch origin.
                NOORIGIN if there is no origin or the origin is not found
            <bundle_datetime>   : 
                date and time of bundle generation (yyyymmddHHMMSS).
        """
        date_time_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d%H%M%S')
        bundle_name = "{0}@{1}@{2}@{3}.bundle".format(repository_name, 
                                                      branch_name.replace('/', '+'),
                                                      branch_origin,
                                                      date_time_now
                                                      )

        return bundle_name


    def is_my_repo(self, repo_no:str):
        """
        Checks if the specified repository number denotes the respoistory to manage.

        Parameters
        ----------
        repo_no : str
            branch name prefix (repository number )

        Returns
        ----------
        is_my_repo : bool
            True if the specifried repository number denotes the repository to manage
        """
        if repo_no == self._cfg["config_common"]["my_repo"].replace("repo",""):
            is_my_repo = True
        else:
            is_my_repo = False

        return is_my_repo


    def __create_dir(self, dir_path):
        if os.path.isdir(dir_path):
            pass
        else:    
            os.makedirs(dir_path, exist_ok=False)
