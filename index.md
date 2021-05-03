# GitBundleManager

##  Summary

Simple toolkit for git repository management on Windows.

Basically built on python and designed specifically for synchronization of isolated git repository pairs.  An "isolated git repository pair" here means a pair of git repositories that don't have direct access to each other but need to synchronize. Repository management in such restricted environments can be troublesome depending on the frequency of synchronization and the number of repositories. This tool kit utilizes the [git bundle command](https://git-scm.com/docs/git-bundle)  and aims to make repository synchronization easier (even a tad!) .

## Features

* Automated bundle output according to json configurations
* Automated bundle merge/push <br> Note: To use this feature, employ GitBundleManager for both bundle output and bundle merge
* Multiple repository/branch support


## Using GitBundleManager

1. Configure gitbundle_config.json 
2. Run make_bat.bat
3. Bundle files for specified repositories and branches will be generated to the specified directory
4. Bundle files in the specified directory will be automatically merged to your repository.

## Notes

* Current implementation supports one branch per json configuration.
* The toolkit is currently implemented for Windows environments

* Environment

| tool name | version |
| :--- | :--- |
| Git | version 2.30.1.windows.1 |
| Python | version 3.9.2 |
| GitPython | version 3.1.14 |

## Upcoming features

* Wildcard support for branch name, e.g. feature/*.  <version 0.0.3>
* Branch synchronization (add/delete). <version 0.0.3>

## History

### Version 0.0.2

* Added bundle merge support.
* Added --tags to bundle output option example.

### Version 0.0.1

* First release.

