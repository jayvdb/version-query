#!/usr/bin/env bash
set -Eeuxo pipefail

# pyenv installer (for macOS)
# updated: 2019-05-10

# use the following to enable diagnostics
# export PYENV_DIAGNOSE=1

if [[ "${TRAVIS_OS_NAME}" == "osx" ]]; then
  if [ -n "${DIAGNOSE_PYENV-}" ] ; then
    pyenv install --list
  fi
  if ! [[ ${TRAVIS_PYTHON_VERSION} =~ .*-dev$ ]] ; then
    TRAVIS_PYTHON_VERSION="$(pyenv install --list | grep -E " ${TRAVIS_PYTHON_VERSION}(\.[0-9brc]+)+" | tail -n 1 | sed -e 's/^[[:space:]]*//')"
  fi
  pyenv install "${TRAVIS_PYTHON_VERSION}"
  # export PATH="${HOME}/.pyenv/versions/${TRAVIS_PYTHON_VERSION}/bin:${PATH}"
  ln -s "${HOME}/.pyenv/versions/${TRAVIS_PYTHON_VERSION}/bin/python" "${HOME}/.local/bin/python"
  ln -s "${HOME}/.pyenv/versions/${TRAVIS_PYTHON_VERSION}/bin/pip" "${HOME}/.local/bin/pip"
fi
