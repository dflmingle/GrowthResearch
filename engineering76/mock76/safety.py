"""Python-level fail-closed transport guard;not an OS sandbox claim."""
import sys

def install(*,allow_child=False):
    def guard(event,args):
        if event.startswith(('socket.','http.client.','urllib.')):
            raise PermissionError('Round76 forbids all sockets and external transports')
        if event in ['os.system','os.exec','os.posix_spawn']:
            raise PermissionError('Shell/exec is disabled')
        if event=='subprocess.Popen' and not allow_child:
            raise PermissionError('App/service/auditor cannot spawn children')
    sys.addaudithook(guard)

def mock_key(value):
    if not isinstance(value,str) or not value.startswith('mock-') or len(value)>80 or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in value):
        raise ValueError('Only fixture mock-* keys permitted;no actual identifiers')
    return value
