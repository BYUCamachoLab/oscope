from subprocess import run as shell

# git remote update
# I think this updates the tracking?

# git status -uno
# This will tell you if you're up to date with the branch or not.
# ---------- OUTPUT ----------
# On branch updater-git
# Your branch is up to date with 'origin/updater-git'.
# 
# nothing to commit (use -u to show untracked files)
# 
# ---------- END OUTPUT ----------

def update(branch = "master"):
    shell(["git", "fetch"]) # Get changes.
    shell(["git", "reset", "--hard", f"origin/{branch}"]) # Forcibly update local repository with branch.

def check_for_updates():
    shell(["git", "remote", "update"])
    output = shell("git", "status", "-uno").stdout