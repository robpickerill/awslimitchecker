"""
awslimitchecker/version.py

The latest version of this package is available at:
<https://github.com/jantman/awslimitchecker>

################################################################################
Copyright 2015-2018 Jason Antman <jason@jasonantman.com>

    This file is part of awslimitchecker, also known as awslimitchecker.

    awslimitchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    awslimitchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with awslimitchecker.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/awslimitchecker> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import os

import logging
logger = logging.getLogger(__name__)

try:
    from versionfinder import find_version
except ImportError:
    logger.error("Unable to import versionfinder", exc_info=True)

_VERSION_TUP = (11, 0, 0)
_VERSION = '.'.join([str(x) for x in _VERSION_TUP])
_PROJECT_URL = 'https://github.com/jantman/awslimitchecker'


class AWSLimitCheckerVersion(object):

    def __init__(self, release, url, commit=None, tag=None):
        self.release = release
        self.url = url
        self.commit = commit
        self.tag = tag

    @property
    def version_str(self):
        """
        The version string for the currently-running awslimitchecker;
        includes git branch and tag information.

        :rtype: str
        """
        vs = str(self.release)
        if self.tag is not None:
            vs += '@{t}'.format(t=self.tag)
        elif self.commit is not None:
            vs += '@{c}'.format(c=self.commit)
        return vs

    def __str__(self):
        """
        Human-readable string representation of this version object, in the
        format: "version_str <url>"

        :rtype: str
        """
        return '{s} <{u}>'.format(
            s=self.version_str,
            u=self.url
        )

    def __repr__(self):
        """
        Return a representation of this object that is valid Python and will
        create an idential AWSLimitCheckerVersion object.

        :rtype: str
        """
        return 'AWSLimitCheckerVersion({r}, {u}, tag={t}, commit={c})'.format(
            r=repr(self.release),
            u=repr(self.url),
            t=repr(self.tag),
            c=repr(self.commit),
        )


def _get_version_info():
    """
    Returns the currently-installed awslimitchecker version, and a best-effort
    attempt at finding the origin URL and commit/tag if installed from an
    editable git clone.

    :returns: awslimitchecker version
    :rtype: str
    """
    if os.environ.get('VERSIONCHECK_DEBUG', '') != 'true':
        for lname in ['versionfinder', 'pip', 'git']:
            l = logging.getLogger(lname)
            l.setLevel(logging.CRITICAL)
            l.propagate = True
    try:
        vinfo = find_version('awslimitchecker')
        dirty = ''
        if vinfo.git_is_dirty:
            dirty = '*'
        tag = vinfo.git_tag
        if tag is not None:
            tag += dirty
        commit = vinfo.git_commit
        if commit is not None:
            if len(commit) > 7:
                commit = commit[:8]
            commit += dirty
        return AWSLimitCheckerVersion(
            vinfo.version,
            vinfo.url,
            tag=tag,
            commit=commit
        )
    except Exception:
        logger.exception("Error checking installed version; this installation "
                         "may not be in compliance with the AGPLv3 license:")
    # fall back to returning just the hard-coded release information
    return AWSLimitCheckerVersion(_VERSION, _PROJECT_URL)
