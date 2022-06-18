import os
import sys
import subprocess
sys.exit(subprocess.call([
    os.path.join(os.path.dirname(__file__), 'Contents', 'Home', 'bin', 'java'),
    *sys.argv[1:]
]))