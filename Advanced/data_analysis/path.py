'''
Created in order to define path when files are being used in executable. 

Returns different path if file is run as script or through .exe. 

Requires `os` and `sys` libraries. 
'''

import sys
import os

def resolve_path(path):
    '''
    Given path returns either itself or the one required if run in executable. 

    Parameters
    ---------- 
    path: pathname
        Path to be resolved 
    
    Returns
    -------
    pathname 
        Correct path
    '''

    if getattr(sys, "frozen", False):
        # If the 'frozen' flag is set, we are in bundled-app mode!
        resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
    else:
        resolved_path = path

    return resolved_path