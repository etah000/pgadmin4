from os import system
from paramiko import SSHClient as _SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
import logging


class SSHClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, port=22, password=None, pkey=None):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.pkey = pkey

        self.client = None
        self.scp = None

        self._connect()

    def _connect(self, ):
        """Open connection to remote host. """
        try:
            self.client = _SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                pkey=self.pkey,
                look_for_keys=True,
            )

            self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as error:
            logging.error('Authentication failed: did you remember to create an SSH key? {}'.format(error))
            raise error

        return self.client

    def __del__(self, ):
        self.disconnect()

    def disconnect(self):
        """Close ssh connection."""

        # It’s good practice to close your client objects anytime you’re done using them,
        # instead of relying on garbage collection.

        if self.client:
            self.client.close()
            self.client = None

        if self.scp:
            self.scp.close()
            self.scp = None

    def put(self, files, remote_path='.', recursive=False, preserve_times=False):
        """
        Upload files to a remote directory.

        :param files: single or list of paths to local files.
        """

        self.scp.put(files, remote_path=remote_path,
                     recursive=recursive,
                     preserve_times=preserve_times, )

    def putfo(self, fl, remote_path, mode='0644', size=None):
        """
        Transfer file-like object to remote host.

        """

        self.scp.putfo(fl, remote_path, mode=mode, size=size)

    def get(self, remote_path, local_path='', recursive=False, preserve_times=False):
        """Download file from remote host."""

        self.scp.get(remote_path, local_path=local_path,
                     recursive=recursive,
                     preserve_times=preserve_times, )

    def execute_cmds(self, cmds):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        for cmd in cmds:
            self.execute_cmd(cmd)

    def execute_cmd(self, cmd, **kwargs):
        """
        Execute command in succession.

        :param cmd: unix command as string
        :type cmd: str

        """
        stdin, stdout, stderr = self.client.exec_command(cmd, **kwargs)
        exit_status = stdout.channel.recv_exit_status()

        return exit_status, stdout, stderr

    def _execute_cmd(self, cmd):
        """
        Execute single commands in succession.

        :param cmd: unix command as string
        :type cmd: str
        """

        stdin, stdout, stderr = self.client.exec_command(cmd)
        # stdin.write('PASSWORD\n')
        # print(stdout.readlines())

        exit_status = stdout.channel.recv_exit_status()

        stdout_response = stdout.readlines()
        stderr_response = stderr.readlines()

        print('exit_status:', exit_status)
        print('stdout_response:', stdout_response)
        print('stderr_response:', stderr_response)


if __name__ == '__main__':
    client = SSHClient('node151', 'root')
    client.execute_cmd('date')
    client.execute('date')
