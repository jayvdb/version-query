"""Git repository version query tools."""

import datetime
import logging
import pathlib
import typing as t

import git
#import packaging

from .version import VersionComponent, Version

_LOG = logging.getLogger(__name__)


def _all_git_tag_versions(repo: git.Repo) -> t.Mapping[git.Tag, Version]:
    versions = {}
    for tag in repo.tags:
        tag_str = str(tag)
        if tag_str.startswith('v'):
            tag_str = tag_str[1:]
        else:
            continue
        try:
            versions[tag] = Version.from_str(tag_str)
        except ValueError:
        #except packaging.version.InvalidVersion:
            _LOG.warning('failed to convert %s to version', tag_str)
            continue
    return versions


def _latest_git_tag_version(repo: git.Repo) -> t.Tuple[git.Tag, Version]:
    versions = sorted(_all_git_tag_versions(repo).items(), key=lambda _: _[1])
    if not versions:
        raise ValueError('no versions in this repository')
    return versions[-1]


def _upcoming_git_tag_version(repo: git.Repo) -> Version:
    latest_version_tag, version = _latest_git_tag_version(repo)
    repo_is_dirty = repo.is_dirty(untracked_files=True)
    repo_has_new_commits = repo.head.commit != latest_version_tag.commit

    if not repo_has_new_commits and not repo_is_dirty:
        return version

    pre_patch_increment = 0
    if repo_has_new_commits:
        for commit in repo.iter_commits():
            _LOG.log(logging.NOTSET, 'iterating over commit %s', commit)
            if commit == latest_version_tag.commit:
                break
            pre_patch_increment += 1
        _LOG.debug('there are %i new commits since %s', pre_patch_increment, version)

    if version._pre_release:
        if repo_has_new_commits:
            version.increment(VersionComponent.PrePatch, pre_patch_increment)
        #if True: raise NotImplementedError()
        #return version
    else:
        version.increment(VersionComponent.Patch)
        if repo_has_new_commits:
            version._pre_release = [('.', 'dev', pre_patch_increment)]

    if repo_has_new_commits:
        commit_sha = repo.head.commit.hexsha[:8]
        version._local = (commit_sha,)

    if repo_is_dirty:
        version._local = version._local + ('.', 'dirty{}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')))

    #if not repo_is_dirty and get_caller_module_name(-1) == 'setup' \
    #        and any(_ in sys.argv for _ in ('bdist', 'bdist_wheel', 'sdist')):
    #    commit_sha = None

    return version


def query_git_repo(
        repo_path: pathlib.Path, search_parent_directories: bool = True) -> Version:
    """Determine version from tags of a git repository."""
    _LOG.debug('looking for git repository in "%s"', repo_path)
    repo = git.Repo(str(repo_path), search_parent_directories=search_parent_directories)
    _LOG.debug('found git repository in "%s"', repo.working_dir)
    return _latest_git_tag_version(repo)[1]

def predict_git_repo(repo_path: pathlib.Path, search_parent_directories: bool = True) -> Version:
    repo = git.Repo(str(repo_path), search_parent_directories=search_parent_directories)
    return _upcoming_git_tag_version(repo)
