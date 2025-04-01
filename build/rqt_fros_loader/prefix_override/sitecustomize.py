import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/himaj/rqt_fros_loader/install/rqt_fros_loader'
