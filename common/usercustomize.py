import sys
import inspect
import pathlib
stack = inspect.stack()
importerpath = pathlib.Path(stack[0].filename).parent
sys.path.append(importerpath.parent.joinpath("common").as_posix())
