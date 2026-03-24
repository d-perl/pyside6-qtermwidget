def test_import_wheel():
    import pyside6_qtermwidget


def test_module_has_class():
    import pyside6_qtermwidget

    assert hasattr(pyside6_qtermwidget, "QTermWidget")


def test_instantiate_class():
    import sys

    import pyside6_qtermwidget
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = QTermWidget()
