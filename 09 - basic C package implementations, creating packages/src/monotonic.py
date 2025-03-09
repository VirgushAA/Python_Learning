import ctypes
import ctypes.util


libc = ctypes.CDLL('/usr/lib/libSystem.dylib', use_errno=True)


if not hasattr(libc, "clock_gettime"):
    raise OSError("clock_gettime is not available on this system")


class Timespec(ctypes.Structure):
    _fields_ = [('tv_sec', ctypes.c_long), ('tv_nsec', ctypes.c_long)]


def monotonic():
    ts = Timespec()
    CLOCK_MONOTONIC = 6

    if libc.clock_gettime(CLOCK_MONOTONIC, ctypes.byref(ts)) != 0:
        raise OSError(ctypes.get_errno(), 'clock_gettime failed')

    return ts.tv_sec + ts.tv_nsec * 1e-9


def main():
    print(monotonic())


if __name__ == '__main__':
    main()
