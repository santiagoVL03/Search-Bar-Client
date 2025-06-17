import os
import json
from app.utils.functions_ssh import _ssh_execute, parse_spark_output_to_json
import os
from collections import OrderedDict

class Spark_searchController:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        config_path = os.path.abspath(os.path.join(base_dir, '../../config/config.json'))
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.name = 'SearchControllerSpark'
        self.description = 'Controller for show an video from the cluster'
        self.ssh_host = config['ssh_host']
        self.ssh_user = config['ssh_user']
        self.ssh_password = config['ssh_password']
        self.spark_output_path = config['spark_output_path']
        self.spark_class = config['spark_class']
        self.jar_path = config['jar_path']
        self.search_motor = config['search_motor']
        self.hive_page_ranking = config['hive_page_ranking']
        self.hive_page_ranking_output = config['hive_page_ranking_output']

    def index(self, word = None):
        cleanup_cmd = f'hadoop fs -rm -r {self.spark_output_path}'
        cleanup_result = _ssh_execute(cleanup_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if cleanup_result['status'] == 'error':
            print(f"Error cleaning up HDFS output: {cleanup_result['output']} THIS ERROR IS NOT BLOCKING")
        job_cmd = (
            f"spark-submit "
            f"--class \"{self.spark_class}\" "
            f"--master yarn "
            f"--deploy-mode cluster "
            f" {self.search_motor} "
        )
        job_result = _ssh_execute(job_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if job_result['status'] == 'error':
            print(f"Error executing Spark job: {job_result['output']} THIS ERROR IS NOT BLOCKING")
            
        job_hive = (
            f"hive -hivevar "
            f"search_class = {word} "
            f"-f \"{self.hive_page_ranking}\" "
        )
        
        job_hive_result = _ssh_execute(job_hive, self.ssh_host, self.ssh_user, self.ssh_password)
        if job_hive_result['status'] == 'error':
            print(f"Error executing Hive job: {job_hive_result['output']} THIS ERROR IS NOT BLOCKING")
        
        read_cmd_hive = f'hdfs dfs -cat {self.hive_page_ranking_output}/{word}/0*'
        read_result_hive = _ssh_execute(read_cmd_hive, self.ssh_host, self.ssh_user, self.ssh_password)
        if read_result_hive['status'] == 'error':
            return {
                'status': 'error',
                'output': {}
            }
        print(read_result_hive['output'])
        
        output_hive = read_result_hive['output']

        read_cmd = f'hdfs dfs -cat {self.spark_output_path}/part-*'
        read_result = _ssh_execute(read_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if read_result['status'] == 'error':
            return {
                'status': 'error',
                'output': {}
            }
        print(read_result['output'])
        output = read_result['output']
        
        parsed_output = parse_spark_output_to_json(output, output_hive)
        if word:
            filtered_output = OrderedDict()
            for filename, info in parsed_output.items():
                filtered_detections = [
                    obj for obj in info["objects"]
                    if word.lower() in obj["object"].lower()
                ]
                if filtered_detections:
                    filtered_output[filename] = {
                        "views": info["views"],
                        "objects": filtered_detections
                    }
                    
            return {
                'status': 'success',
                'output': filtered_output
            }

        if not parsed_output:
            return {
                'status': 'success',
                'output': {}
            }
        else:
            return {
                'status': 'success',
                'output': parsed_output
            }