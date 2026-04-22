##ruff and black 
"""ruff is a linter"""
"""Linter -- is a tool to check for errors without actually running the code"""

its extremely fast and used in rust programming lang

primarily used to check for errors,style issues,unused imports, etc

##Black
Its a code formatter 
its only used for style consistency and not for linting
linter--finds the problems 
formatter-- fixes formatting automatically

"""formatter is a tool that automatically rewrites your code to follow a consistent style

installed ruff and black 
pip install ruff
pip install black

##To check the version 
black --version
ruff --version
 

To format a specific file 
#black file.py

#entire folder
black .

TO check for issues 
ruff check .
#To auto fix
ruff check . --fix
#To format
ruff format .
#To check single file
ruff check file.py