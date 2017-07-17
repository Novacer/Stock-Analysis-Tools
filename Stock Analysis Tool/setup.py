from cx_Freeze import setup, Executable
import os
import scipy

os.environ['TCL_LIBRARY'] = r"C:\Users\MARY\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\MARY\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6"

includes      = ['numpy.core._methods', 'numpy.lib.format', 'matplotlib.backends.backend_tkagg', 'tkinter.filedialog', 'numpy.matlib']
include_files = [r"C:\Users\MARY\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll", \
                 r"C:\Users\MARY\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]
scipy_path = os.path.dirname(scipy.__file__)
include_files.append(scipy_path)

				 
setup(name='Tool',
	  version='1.0',
	  description='Collection of stock tools',
	  options= {"build_exe": {"includes": includes, "include_files": include_files}},
	  executables = [Executable('Tool.py', base='win32GUI')])