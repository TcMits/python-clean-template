import os

from config import get_settings
from internal import app

PROJECT_ROOT = os.path.dirname(__file__)

if __name__ == "__main__":
    settings = get_settings()
    app.run(PROJECT_ROOT, settings)
