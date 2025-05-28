import paramiko
import json
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
        cleanup_result = self._ssh_execute(cleanup_cmd)
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

        job_result = self._ssh_execute(job_cmd)
        if job_result['status'] == 'error':
            print(f"Error executing MapReduce job: {job_result['output']} THIS ERROR IS NOT BLOCKING")

        # Paso 3: Leer resultados de HDFS
        read_cmd = f'hdfs dfs -cat {self.hdfs_output_path}/part-*'
        read_result = self._ssh_execute(read_cmd)
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
        # if word:
        #     # Filtrar resultados por la palabra clave
        #     filtered_output = {k: v for k, v in output_json.items() if word.lower() in k.lower()}
        #     return {
        #         'status': 'success',
        #         'output': filtered_output
        #     }
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
        
    def _ssh_execute(self, command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                username=self.ssh_user,
                password=self.ssh_password
            )

            export_env = (
                'export HADOOP_HOME=/home/hduser/hadoop-3.3.2 && '
                'export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH && '
            )
            full_command = export_env + command

            stdin, stdout, stderr = ssh.exec_command(full_command)

            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            ssh.close()

            if error.strip():
                return {'status': 'error', 'output': error}
            return {'status': 'success', 'output': output}
        except Exception as e:
            return {'status': 'error', 'output': str(e)}
        
def parse_hdfs_output_to_json(hdfs_output_str):
    data = {}
    lines = hdfs_output_str.strip().split('\n')

    for line in lines:
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) != 3:
            # Por si alguna línea está mal formada
            continue
        video_file, obj, count_str = parts
        count = int(count_str)

        if video_file not in data:
            data[video_file] = []

        data[video_file].append({
            "object": obj,
            "count": count
        })

    return data
    
