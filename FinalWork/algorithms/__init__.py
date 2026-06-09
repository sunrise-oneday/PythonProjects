# 导入所有算法模块（触发 @register 装饰器）
from . import grayscale
from . import filtering
from . import frequency
from . import edge_detection
from . import morphology
from . import segmentation
from . import hough
from . import restoration
from . import matting

# 暴露注册字典
from .registry import ALGORITHMS
