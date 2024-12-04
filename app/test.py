import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models.validators import get_validators
from app.settings.config import ROOT_DIR

print(get_validators(f"{ROOT_DIR}/settings/validators.json"))
