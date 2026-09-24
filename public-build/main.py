# ============================================================
# File:        main.py
# Project:     UAV Management Dashboard
# Purpose:     Application Entry point
#
# Description:
#     Initializes the PyQt6 application and launches the dashboard.
#
# Features:
#     Launch point
#
# Author:      Debe Okoye
# Created:     2026-06-02
# ============================================================

import sys

from PyQt6.QtWidgets import (
	QApplication
)
from app.ui.dashboard import DashboardWindow


def main() -> None:
	app = QApplication(sys.argv)
	
	window = DashboardWindow()
	window.show()
	sys.exit(app.exec())


if __name__ == "__main__":
	main()
