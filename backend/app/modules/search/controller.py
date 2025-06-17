import paramiko
import json
from app.utils.functions_ssh import _ssh_execute, parse_hdfs_output_to_json
import os
class SearchController:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        config_path = os.path.abspath(os.path.join(base_dir, '../../config/config.json'))
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.name = 'SearchController'
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

    def index(self, word = None):
        cleanup_cmd = f'hadoop fs -rm -r {self.hdfs_output_path}'
        cleanup_result = _ssh_execute(cleanup_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        
        if cleanup_result['status'] == 'error':
            print(f"Error cleaning up HDFS output: {cleanup_result['output']} THIS ERROR IS NOT BLOCKING")
        
        # create_directory_cmd = f'hadoop fs -mkdir -p {self.hdfs_output_path}'
        # create_directory_result = _ssh_execute(create_directory_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        
        # if create_directory_result['status'] == 'error':
        #     print(f"Error creating HDFS output directory: {create_directory_result['output']} THIS ERROR IS NOT BLOCKING")
            
        job_cmd = (
            f"hadoop jar {self.jar_path} "
            f"-input {self.input_path} "
            f"-output {self.hdfs_output_path} "
            f"-mapper \"{self.mapper}\" "
            f"-reducer \"{self.reducer}\" "
            f"-file {self.map} "
            f"-file {self.reduce} "
        )

        job_result = _ssh_execute(job_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if job_result['status'] == 'error':
            print(f"Error executing MapReduce job: {job_result['output']} THIS ERROR IS NOT BLOCKING")

        read_cmd = f'hdfs dfs -cat {self.hdfs_output_path}/part-*'
        read_result = _ssh_execute(read_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if read_result['status'] == 'error':
            return {
                'step': 'read_output',
                'error': 'Error reading output from HDFS',
                'details': read_result['output']
            }
            
        print(read_result['output'])
        output = read_result['output']
        output_json = parse_hdfs_output_to_json(output)
        json_str = json.dumps(output_json, indent=4)
        print(json_str)
        if word:
            filtered_output = {k: v for k, v in output_json.items() if word.lower() in k.lower()}
            return {
                'status': 'success',
                'output': filtered_output
            }
        if not output_json:
            return {
                'status': 'success',
                'output': {}
            }
        else:
            return {
                'status': 'success',
                'output': output_json
            }