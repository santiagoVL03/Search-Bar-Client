from backend.app.utils.functions_ssh import _ssh_execute
from flask import send_file
import json
import os

class VideoController:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.name = 'VideoController'
        self.description = 'Controller for show an video from the cluster'
        self.ssh_host = config['ssh_host']
        self.ssh_user = config['ssh_user']
        self.ssh_password = config['ssh_password']
        self.hdfs_output_path = config['hdfs_output_path']
        self.input_path = config['input_path']
        self.jar_path = config['jar_path']
        self.mapper = config['mapper_cmd']
        self.reducer = config['reducer_cmd']
        self.map = config['map_path']
        self.reduce = config['reduce_path']
        self.local_video_dir = config['local_video_dir']

    def getvideo (self, video_file):
        command = f"""
        hadoop fs -get /video/{video_file} {self.local_video_dir}/{video_file}
        """
        
        result = _ssh_execute(command, self.ssh_host, self.ssh_user, self.ssh_password)
        
        if result['status'] == 'error':
            return {'status': 'error', 'message': result['output']}
        
        return {'status': 'success', 'message': f'Video {video_file} downloaded successfully.', 'path': f'/tmp/video/{video_file}'}
    
    def index(self, video_file = None):
        data = self.getvideo(video_file)
        if data['status'] == 'error':
            return {
                'status': 'error',
                'message': data['message']
            }
        return {
            'status': 'success',
            'message': data['message'],
            'path': data['path']
        }
