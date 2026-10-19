from . import catch22 as _catch22
from .catch22 import catch22_all, feature_table

# one function per feature (e.g., DN_HistogramMode_5), and deprecated aliases for the
# names before v1.0 (e.g., CO_f1ecac)
globals().update(_catch22.FEATURE_FUNCTIONS)
globals().update(_catch22._LEGACY_FUNCTIONS)

__all__ = ['catch22_all', 'feature_table', *_catch22.FEATURE_FUNCTIONS]
