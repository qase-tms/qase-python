from .converters import Converter, UnstructureStrategy
from .modifiers import mod

__all__ = (
    "global_converter",
    "unstructure",
    "structure",
    "structure_dataclass_fromtuple",
    "structure_dataclass_fromdict",
    "UnstructureStrategy",
    "Converter",
    "mod",
)

__author__ = "Parviz Khavari"
__email__ = "me@parviz.pw"


global_converter = Converter()

unstructure = global_converter.unstructure
structure = global_converter.structure
structure_dataclass_fromtuple = global_converter.structure_dataclass_fromtuple
structure_dataclass_fromdict = global_converter.structure_dataclass_fromdict
register_structure_hook = global_converter.register_structure_hook
register_structure_hook_func = global_converter.register_structure_hook_func
register_unstructure_hook = global_converter.register_unstructure_hook
register_unstructure_hook_func = (
    global_converter.register_unstructure_hook_func
)
