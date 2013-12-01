import os
import sys

if os.name == 'posix':
    libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
    if libpath not in sys.path:
        sys.path.insert(0, libpath)
        
else:
    libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib'))
    if libpath not in sys.path:
        sys.path.insert(0, libpath)