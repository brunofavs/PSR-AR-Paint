#!/usr/bin/env python3

# -----------
# Conventions
# -----------

# ! camelCase for functions and methods
# ! snake_case for variables

# -----------
# Imports
# -----------
import argparse
import cv2
import numpy as np
from functools import partial
import json
from copy import deepcopy

# -----------
# Functions
# -----------

def buildPuzzle(res):



    blank_1D = np.zeros([res[0], res[1]],dtype = np.uint8)
    return