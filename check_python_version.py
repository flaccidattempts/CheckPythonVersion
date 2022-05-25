'''Check to see if python is recent enough'''

from __future__ import print_function

import os
import platform
import subprocess
import sys

MIN_PYTHON_VERSION_SOFT = (3, 6)
MIN_PYTHON_VERSION_HARD = (3, 5)

def exec_command(cmd):
  """Execute |cmd| or return None on failure."""
  try:
    if platform.system() == 'Windows':
      ret = subprocess.call(cmd)
      sys.exit(ret)
    else:
      os.execvp(cmd[0], cmd)
  except Exception:
    pass


def check_python_version():
  """Make sure the active Python version is recent enough."""
  def reexec(prog):
    exec_command([prog] + sys.argv)


  ver = sys.version_info
  major = ver.major
  minor = ver.minor

  # Abort on very old Python 2 versions.
  if (major, minor) < (2, 7):
    print('error: Your Python version is too old. ''Please use Python {}.{} or newer instead.'.format(*MIN_PYTHON_VERSION_SOFT), file=sys.stderr)
    sys.exit(1)

  # Try to re-exec the version specific Python 3 if needed.

  if (major, minor) < MIN_PYTHON_VERSION_SOFT:

    # Python makes releases ~once a year, so try our min version +10 to help
    # bridge the gap.  This is the fallback anyways so perf isn't critical.

    min_major, min_minor = MIN_PYTHON_VERSION_SOFT

  for inc in range(0, 10):

    reexec('python{}.{}'.format(min_major, min_minor + inc))

    # Fallback to older versions if possible.

  for inc in range(MIN_PYTHON_VERSION_SOFT[1] - MIN_PYTHON_VERSION_HARD[1], 0, -1):

    # Don't downgrade, and don't reexec ourselves (which would infinite loop).

    if (min_major, min_minor - inc) <= (major, minor):

      break

    reexec('python{}.{}'.format(min_major, min_minor - inc))


  # Try the generic Python 3 wrapper, but only if it's new enough.  If it
  # isn't, we want to just give up below and make the user resolve things.
    
  try:
    proc = subprocess.Popen(['python3', '-c', 'import sys; ''  print(sys.version_info.major, sys.version_info.minor)'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, _) = proc.communicate()
    python3_ver = tuple(int(x) for x in output.decode('utf-8').split())
  
  except (OSError, subprocess.CalledProcessError):
    python3_ver = None

  # If the python3 version looks like it's new enough, give it a try.

  if (python3_ver and python3_ver >= MIN_PYTHON_VERSION_HARD and python3_ver != (major, minor)):
    reexec('python3')

  # We're still here, so diagnose things for the user.

  if major < 3:

    print('[error]: Python 2 is no longer supported; ''Please upgrade to Python {}.{}+.'.format(*MIN_PYTHON_VERSION_HARD),file=sys.stderr)
    sys.exit(1)

  elif (major, minor) < MIN_PYTHON_VERSION_HARD:

    print('[error]: Python 3 version is too old; ''Please use Python {}.{} or newer.'.format(*MIN_PYTHON_VERSION_HARD),file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
  check = check_python_version()
  if check == None:
    print('Python Check Passed')

