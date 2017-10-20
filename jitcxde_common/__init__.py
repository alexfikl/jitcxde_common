from .strings import remove_suffix, ensure_suffix, count_up
from .numerical import random_direction, orthonormalise, rel_dist
from .collect_arguments import collect_arguments
from .input_handling import sort_helpers, sympify_helpers, copy_helpers, filter_helpers
from .module_handling import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
from ._jitcxde import jitcxde, DEFAULT_COMPILE_ARGS, DEFAULT_LINK_ARGS, MSVC_COMPILE_ARGS,MSVC_LINK_ARGS

try:
	from .version import version as __version__
except ImportError:
	from warnings import warn
	warn('Failed to find (autogenerated) version.py. Do not worry about this unless you really need to know the version.')
