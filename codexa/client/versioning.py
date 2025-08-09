import logging
import os

from git import Repo

from codexa.core.errors import CodexaRuntimeError

logger = logging.getLogger(__name__)


def compare_git_diff(remote_ref: str, repo_path: str = os.getcwd()) -> str:
    """
    Get the diff between the current working tree and a remote branch using GitPython.

    Args:
        repo_path (str): Path to the Git repository.
        remote_ref (str): Remote branch to diff against (e.g. 'origin/main').

    Returns:
        Optional[str]: The unified diff output as a string, or None on failure.
    """
    try:
        repo = Repo(repo_path)
        if repo.bare:
            logger.warning(f"No changes detected in the repository: {repo_path}")
            return ""

        repo.remotes.origin.fetch()
        head_commit = repo.head.commit
        remote_commit = repo.commit(remote_ref)

        diff_index = head_commit.diff(remote_commit, create_patch=True)
        return "\n".join(str(d.diff) for d in diff_index if d.diff)
    except Exception as e:
        raise CodexaRuntimeError(f"Failed to get git diff: {e}")
