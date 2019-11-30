__version__ = '0.4'
__author__ = "Shengmei Zou"
__email__ = "21818662@zju.edu.cn"

import warnings
warnings.simplefilter("ignore")
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
import numpy as np
import  pandas as pd
import matplotlib.pylab  as plt
from .Detection import Detection
from .Detection2 import Detection2
from .Detection3 import Detection3
from .Preprocessed_data import Preprocessed_data
#from  .outbreak_prediction import outbreak_prediction
from  .PredictionDetection import PredictionDetection
from  .Prediction import *
from .PAD import PAD
