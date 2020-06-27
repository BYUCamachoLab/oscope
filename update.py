""" Updater script using git.

This script calls git through the shell to do updates.
This script is only meant to be used in actual deployments as
it will overwrite any local changes to repository.

"""

# git status -uno
# This will tell you if you're up to date with the branch or not.
# ---------- OUTPUT ----------
# On branch updater-git
# Your branch is up to date with 'origin/updater-git'.
# 
# nothing to commit (use -u to show untracked files)
# 
# ---------- END OUTPUT ----------
from subprocess import run as shell

def update(branch = "master"):
    # Use git to update:
    # git fetch
    # git reset --hard origin/{branch}
    # git submodule foreach --recursive git reset --hard
    shell(["git", "fetch"]) # Get changes.
    shell(["git", "reset", "--hard", f"origin/{branch}"]) # Forcibly update local repository with branch.
    shell(["git", "submodule", "foreach", "--recursive", "git", "reset", "--hard"]) # Reset submodules as well.

def check_for_updates():
    shell(["git", "remote", "update"])
