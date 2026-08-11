#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import io
import json
from dataclasses import dataclass
import os
import time
from typing import Tuple

import numpy as np
import requests
from PIL import Image
import torch
import torch.nn as nn

# Define MNIST normalization constants
MNIST_MEAN = 0.1307 # average pixel intensity of MNIST images scaled to [0,1]
MNIST_STD = 0.3081 # standard deviation of pixel intensities in [0,1]

