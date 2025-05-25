import paramiko

class SearchController:
    def __init__(self):
        self.name = 'SearchController'
        self.description = 'Controller for search operations'
        self.ssh_host = 'master'
        self.ssh_user = 'hduser'
        self.ssh_password = 'kali'
        self.hdfs_output_path = '/output/inverted_index'
        self.input_path = '/input/docs'
        self.jar_path = '/home/kali/inverted.jar'

    def index(self):
        # Paso 1: Eliminar salida previa en HDFS
        cleanup_cmd = f'hdfs dfs -rm -r -f {self.hdfs_output_path}'
        cleanup_result = self._ssh_execute(cleanup_cmd)
        if cleanup_result['status'] == 'error':
            return {
                'step': 'cleanup',
                'error': 'Error cleaning HDFS output path',
                'details': cleanup_result['output']
            }

        # Paso 2: Ejecutar job MapReduce
        job_cmd = f'hadoop jar {self.jar_path} {self.input_path} {self.hdfs_output_path}'
        job_result = self._ssh_execute(job_cmd)
        if job_result['status'] == 'error':
            return {
                'step': 'mapreduce',
                'error': 'Error running MapReduce job',
                'details': job_result['output']
            }

        # Paso 3: Leer resultados de HDFS
        read_cmd = f'hdfs dfs -cat {self.hdfs_output_path}/part-*'
        read_result = self._ssh_execute(read_cmd)
        if read_result['status'] == 'error':
            return {
                'step': 'read_output',
                'error': 'Error reading output from HDFS',
                'details': read_result['output']
            }

        return {
            'status': 'success',
            'output': read_result['output']
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

            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            ssh.close()
            if error.strip():
                return {'status': 'error', 'output': error}
            return {'status': 'success', 'output': output}
        except Exception as e:
            return {'status': 'error', 'output': str(e)}
