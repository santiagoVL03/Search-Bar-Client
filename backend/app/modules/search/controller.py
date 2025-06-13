import paramiko
import json
from backend.app.utils.functions_ssh import _ssh_execute, parse_hdfs_output_to_json
class SearchController:
    def __init__(self):
        self.name = 'SearchController'
        self.description = 'Controller for search operations'
        self.ssh_host = 'worker5'
        self.ssh_user = 'hduser'
        self.ssh_password = 'kali'
        self.hdfs_output_path = '/inverted_index'
        self.input_path = '/metadata'
        self.jar_path = '$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar'
        self.mapper = "python3 map.py"
        self.reducer = "python3 reduce.py"
        self.map = '/home/hduser/BASIC-SEARCH-BAR-IN-CLUSTER/Index/map.py'
        self.reduce = '/home/hduser/BASIC-SEARCH-BAR-IN-CLUSTER/Index/reduce.py'

    def index(self, word = None):
        # Paso 1: Eliminar salida previa en HDFS
        cleanup_cmd = f'hadoop fs -rm -r {self.hdfs_output_path}'
        cleanup_result = _ssh_execute(cleanup_cmd, self.ssh_host, self.ssh_user, self.ssh_password)
        if cleanup_result['status'] == 'error':
            print(f"Error cleaning up HDFS output: {cleanup_result['output']} THIS ERROR IS NOT BLOCKING")

        # Paso 2: Ejecutar job MapReduce
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

        # Paso 3: Leer resultados de HDFS
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
        # Paso 4: Devolver resultados
        if word:
            # Filtrar resultados por la palabra clave
            filtered_output = {k: v for k, v in output_json.items() if word.lower() in k.lower()}
            return {
                'status': 'success',
                'output': filtered_output
            }
        # Si no se proporciona una palabra clave, devolver todos los resultados
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