def gui_fname(dir=None):
    """
    Select a file via a dialog and return the file name.
    """
    try:
        from PyQt5.QtWidgets import QApplication, QFileDialog
    except ImportError:
        try:
            from PyQt4.QtGui import QApplication, QFileDialog
        except ImportError:
            from PySide.QtGui import QApplication, QFileDialog

    if dir is None:
        dir = './'

    app = QApplication([dir])
    fname = QFileDialog.getOpenFileName(None, "Select a file...",
                                        dir, filter="All files (*)")

    if isinstance(fname, tuple):
        return fname[0]
    else:
        return str(fname) 