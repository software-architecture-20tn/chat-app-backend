import os
import uuid
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent.parent.parent


def _get_media_path(model_instance, filename):
    """Return a magic filename."""
    components = model_instance._meta.label_lower.split(".")
    components.append(str(model_instance.id))
    components.append(str(uuid.uuid4()))
    components.append(filename)
    return os.path.join(*components)


DEFAULT_MEDIA_FILE_PATH = _get_media_path
