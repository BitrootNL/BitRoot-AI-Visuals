import importlib
import os


def load_classes():
    """ Load implementation classes from the implementation subdirectory. """
    impl_dir = os.path.join(os.path.dirname(__file__), "implementation")
    for filename in os.listdir(impl_dir):
        if not filename.endswith(".py") or filename in ("__init__.py",):
            continue
        try:
            module = importlib.import_module(f'CCPlots.implementation.{filename[:-3]}')
        except Exception:
            continue
        for name, cls in module.__dict__.items():
            if isinstance(cls, type) and getattr(cls, '__module__', '') == module.__name__:
                globals()[name] = cls


load_classes()
