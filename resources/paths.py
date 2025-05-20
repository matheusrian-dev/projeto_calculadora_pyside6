from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES_DIR = Path(__file__).parent
FILES_DIR = RESOURCES_DIR / 'files'
WINDOW_ICON_PATH = FILES_DIR / 'icon-calculator.png'
# Passar o path diretamente no PySide6 gerará um TypeError
# que o VS Code não acusa, converta o path para str para
# resolver.
WINDOW_ICON_PATH_STR = str(WINDOW_ICON_PATH)
