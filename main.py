import sys
import logging
import traceback

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox

from app.core.config import APP_NAME, DATA_DIR
from app.core.logging_config import setup_logging
from app.database.init_db import init_db
from app.database.seed import ensure_default_business
from app.ui.design_system.theme import load_app_stylesheet
from app.ui.app_window import AppWindow


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    # Initialize database
    try:
        logger.info("=" * 60)
        logger.info(f"Application starting - Database location: {DATA_DIR}")
        logger.info("=" * 60)
        
        logger.info("Step 1: Initializing database tables...")
        init_db()
        logger.info("✓ Database initialization complete")
        
        logger.info("Step 2: Ensuring default business exists...")
        ensure_default_business()
        logger.info("✓ Default business ready")
        
    except Exception as e:
        logger.exception("Database initialization failed - application cannot start")
        
        # Show error dialog to user
        app = QApplication(sys.argv)
        error_message = (
            f"Failed to initialize the application database.\n\n"
            f"Error Details:\n{str(e)}\n\n"
            f"Please ensure:\n"
            f"1. The application has write permissions to: {DATA_DIR}\n"
            f"2. The drive has sufficient free space\n"
            f"3. Your antivirus is not blocking file access\n\n"
            f"Check the logs in {DATA_DIR / 'logs'} for more details."
        )
        QMessageBox.critical(None, "Database Initialization Error", error_message)
        logger.critical("Application terminated due to database initialization failure")
        sys.exit(1)

    # Start the application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(load_app_stylesheet())

    def excepthook(exc_type, exc, tb):
        logger.critical("Unhandled exception in application", exc_info=(exc_type, exc, tb))
        msg = "".join(traceback.format_exception(exc_type, exc, tb))
        try:
            QMessageBox.critical(None, "Unexpected Error", msg)
        except Exception:
            # If Qt isn't available, fall back to stderr
            sys.__stderr__.write(msg + "\n")

    sys.excepthook = excepthook

    logger.info("Application UI starting...")
    window = AppWindow()
    window.show()
    logger.info("✓ Application ready")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()