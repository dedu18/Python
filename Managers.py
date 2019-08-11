import cv2
import numpy
import time


class CaptureManger(object):

    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):
        # 单下划线保护变量（子类可访问），双下划线私有变量（子类不可访问）
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
