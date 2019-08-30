def getTerminalSize():
    """ getTerminalSize()
     - get width and height of console
    """
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        return 0, 0
    return int(cr[1]), int(cr[0])

if __name__ == "__main__":
    sizex,sizey=getTerminalSize()
    print('width =',sizex,'height =',sizey)
