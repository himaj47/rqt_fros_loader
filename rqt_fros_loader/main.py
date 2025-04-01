import sys

from rqt_gui.main import Main


def main():
    main = Main()
    sys.exit(main.main(sys.argv, standalone='rqt_fros_loader.fros_loader_plugin.FrosLoaderPlugin'))


if __name__ == '__main__':
    main()