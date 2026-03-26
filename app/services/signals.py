from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):
    product_changed = Signal()
    category_changed = Signal()


app_signals = AppSignals()
