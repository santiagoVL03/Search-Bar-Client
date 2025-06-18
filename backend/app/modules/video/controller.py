import os
import json
import paramiko
import subprocess
from flask import send_file
from app.utils.functions_ssh import _ssh_execute

class VideoController:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        config_path = os.path.abspath(os.path.join(base_dir, '../../config/config.json'))
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.name = 'VideoController'
        self.description = 'Controller for showing a video from the cluster'
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

    def getvideo(self, video_file):
        command_create_video_dir = f"mkdir -p {self.local_video_dir}"
        result_create_dir = _ssh_execute(command_create_video_dir, self.ssh_host, self.ssh_user, self.ssh_password)
        if result_create_dir['status'] == 'error':
            print(f"Error creating local video directory: {result_create_dir['output']} THIS ERROR IS NOT BLOCKING")
        command = f"hadoop fs -get /oursystem/input/video/{video_file} {self.local_video_dir}/{video_file}"
        result = _ssh_execute(command, self.ssh_host, self.ssh_user, self.ssh_password)
        if result['status'] == 'error':
            print(f"Error downloading video: {result['output']} THIS ERROR IS NOT BLOCKING")

        os.makedirs("/tmp/video", exist_ok=True)
        remote_path = f"{self.local_video_dir}/{video_file}"
        local_path_mpg = f"/tmp/video/{video_file}"
        
        if os.path.exists(local_path_mpg):
            os.remove(local_path_mpg)
        
        sftp_result = download_file_via_sftp(
            host=self.ssh_host,
            user=self.ssh_user,
            password=self.ssh_password,
            remote_path=remote_path,
            local_path=local_path_mpg
        )
        if sftp_result['status'] == 'error':
            print(f"Error downloading video via SFTP: {sftp_result['message']} THIS ERROR IS NOT BLOCKING")

        webm_path = local_path_mpg.replace(".mpg", ".webm")
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", local_path_mpg,
                "-c:v", "libvpx", "-b:v", "1M",
                "-c:a", "libvorbis", webm_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'message': f'Error converting video: {e}'}

        return {
            'status': 'success',
            'message': 'Video downloaded and converted successfully.',
            'path': webm_path
        }

    def index(self, video_file=None):
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

def download_file_via_sftp(host, user, password, remote_path, local_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=password)
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        ssh.close()
        return {'status': 'success', 'message': f'Archivo descargado: {remote_path} → {local_path}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
