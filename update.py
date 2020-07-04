""" Updater script using git.

This script calls git through the shell to do updates.
This script is only meant to be used in actual deployments as
it will overwrite any local changes to repository.

"""

from subprocess import run as shell

def update(branch = "master"):
    # Git commands to clean.
    shell(["git", "clean", "-f", "-x", "-d", "-e", "settings.py", "-e", "DATA/"])
    shell(["git", "submodule", "foreach", "git", "clean", "-f", "-x", "-d"])
    # Git commands to update.
    shell(["git", "fetch"]) # Get changes.
    shell(["git", "reset", "--hard", f"origin/{branch}"]) # Forcibly update local repository with branch.
    shell(["git", "submodule", "foreach", "--recursive", "git", "reset", "--hard"]) # Reset submodules as well.

def matches_repo(branch = "master"):
    shell(["git", "remote", "update"])
    repo_hash = shell(["git", "ls-remote", "origin", f"refs/heads/{branch}"], capture_output=True).stdout.split()[0]
    local_hash = shell(["git", "rev-parse", "HEAD"], capture_output=True).stdout.strip()
    print(f"Repo  Hash: {repo_hash}")
    print(f"Local Hash: {local_hash}")
    return (repo_hash == local_hash)

if __name__ == "__main__":
    # Run update when called directly.
    branch = "development"
    no_changes = matches_repo(branch)
    if not no_changes:
        update(branch)