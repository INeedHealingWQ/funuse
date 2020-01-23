'''
***
Modified generic daemon class
***

Author:         http://www.jejik.com/articles/2007/02/
                        a_simple_unix_linux_daemon_in_python/www.boxedice.com

License:        http://creativecommons.org/licenses/by-sa/3.0/

Changes:        23rd Jan 2009 (David Mytton <david@boxedice.com>)
                - Replaced hard coded '/dev/null in __init__ with os.devnull
                - Added OS check to conditionally remove code that doesn't
                  work on OS X
                - Added output to console on completion
                - Tidied up formatting
                11th Mar 2009 (David Mytton <david@boxedice.com>)
                - Fixed problem with daemon exiting on Python 2.4
                  (before SystemExit was part of the Exception base)
                13th Aug 2010 (David Mytton <david@boxedice.com>
                - Fixed unhandled exception if PID file is empty
'''

# Core modules
import atexit
import errno
import os
import sys
import time
import signal
import datetime
from pathlib import Path

class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, logfile, statefile,  stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, use_eventlet=False):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.logfile = logfile
        self.statefile = statefile
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True
        self.use_gevent = use_gevent
        self.use_eventlet = use_eventlet
        self.write_state('inited\n')

    def log(self, *args):
        with open(self.logfile, 'a') as f:
            for a in args:
                tm = str(datetime.datetime.today().time())
                line = ' '.join([tm, a])
                f.write(line)

    def write_pid(self, *args):
        with open(self.pidfile, 'w') as f:
            for l in args:
                f.write(l)

    def write_state(self, *args):
        with open(self.statefile, 'w') as f:
            for a in args:
                f.write(a)

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        self.log('in daemonize\n')
        if self.use_eventlet:
            import eventlet.tpool
            eventlet.tpool.killall()
        try:
            self.log('start first forking\n')
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as e:
            self.log('OSError occurred while fork: %s\n' %(e.strerror))
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment
        self.log('Decouple from parent environment\n')
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        # Do second fork
        try:
            self.log('start second forking\n')
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError as e:
            self.log('OSError occurred while fork: %s\n' %(e.strerror))
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        if sys.platform != 'darwin':  # This block breaks on OS X
            self.log('platform is not drawin\n')
            # Redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = open(self.stdin, 'r')
            so = open(self.stdout, 'a+')
            if self.stderr:
                try:
                    se = open(self.stderr, 'a+', 0)
                except ValueError:
                    # Python 3 can't have unbuffered text I/O
                    se = open(self.stderr, 'a+', 1)
            else:
                se = so
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())
            self.log('all duping down\n')

        def sigtermhandler(signum, frame):
            self.daemon_alive = False
            sys.exit()

        if self.use_gevent:
            import gevent
            gevent.reinit()
            gevent.signal(signal.SIGTERM, sigtermhandler, signal.SIGTERM, None)
            gevent.signal(signal.SIGINT, sigtermhandler, signal.SIGINT, None)
        else:
            signal.signal(signal.SIGTERM, sigtermhandler)
            signal.signal(signal.SIGINT, sigtermhandler)

        self.log("Started\n")

        # Write pidfile
        atexit.register(self.delpid)  # Make sure pid file is removed if we quit
        pid = str(os.getpid())
        pid += '\n'
        self.write_pid(pid)

    def dellog(self):
        os.remove(self.logfile)

    def delpid(self):
        self.write_state('exited\n')
        try:
            # the process may fork itself again
            pid = int(open(self.pidfile, 'r').read().strip())
            if pid == os.getpid():
                os.remove(self.pidfile)
                self.log('exited\n')
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise

    def start(self, *args, **kwargs):
        """
        Start the daemon
        """

        if self.verbose >= 1:
            self.log("Starting...\n")

        # Check for a pidfile to see if the daemon already runs

        pt = Path(self.pidfile)
        if pt.exists() is True:
            with open(pt, 'r') as f:
                l = f.readlines()
                if len(l) != 0 and l[0] != '' and l[0].isspace() is False:
                    if self.verbose >= 1:
                        self.log('Daemon is already running with pid: %s' %l[0])
                    sys.exit(1)

        # Start the daemon
#        print('start to daemonize')
        self.log('start up daemonize\n')
        self.daemonize()
        self.log('Daemonized down. Start to run\n')
        self.write_state('running\n')
        self.run(*args, **kwargs)

    def stop(self):
        """
        Stop the daemon
        """

        if self.verbose >= 1:
            self.log("Stopping...\n")

        # Get the pid from the pidfile
        pid = self.get_pid()

        if not pid:
            message = "pidfile %s does not exist. Not running?\n"
            sys.stderr.write(message % self.pidfile)

            # Just to be sure. A ValueError might occur if the PID file is
            # empty but does actually exist
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

            return  # Not an error in a restart

        # Try killing the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            if err.errno == errno.ESRCH:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.exit(1)

        self.write_state('Stopped\n')
        self.log("Stopped\n")

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def is_running(self):
        pid = self.get_pid()

        if pid is None:
            self.log('Process is stopped\n')
            return False
        elif os.path.exists('/proc/%d' % pid):
            self.log('Process (pid %d) is running...\n' % pid)
            return True
        else:
            self.log('Process (pid %d) is killed\n' % pid)
            return False

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplementedError
