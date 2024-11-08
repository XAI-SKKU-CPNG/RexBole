import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to app.libs.rexbole
rexbole_path = os.path.join(current_dir, '..', '..', 'libs', 'rexbole')

# Add rexbole_path to sys.path
sys.path.append(rexbole_path)
