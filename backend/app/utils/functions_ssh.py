import paramiko
def _ssh_execute(command, host, user, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=host,
            username=user,
            password=password,
        )
        export_env = (
            'export HADOOP_HOME=/home/hduser/hadoop-3.3.2 && '
            'export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH && '
            'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64'
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