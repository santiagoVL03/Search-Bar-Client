import unittest
import json

from app.modules.video.controller import VideoController


def test_index():
    video_controller = VideoController()
    result = video_controller.index()
    assert result == {'message': 'Hello, World!'}
