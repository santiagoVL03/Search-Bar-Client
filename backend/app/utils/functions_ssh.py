from collections import OrderedDict
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
            'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && '
            'export HIVE_HOME=/home/hduser/hive && '
            'export HIVE_CONF_DIR=$HIVE_HOME/conf && '
            'export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$HIVE_HOME/bin:$PATH && '
            'export SPARK_HOME=/home/hduser/spark-3.5.6-bin-hadoop3 && '
            'export PYSPARK_PYTHON=/usr/bin/python3 && '
            'export PATH=$SPARK_HOME/bin:$PATH '
        )
        full_command = export_env + ' && ' + command
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
    data_raw = {}

    lines = hdfs_output_str.strip().split('\n')

    for line in lines:
        if not line.strip():
            continue

        parts = line.split('\t')
        if len(parts) != 3:
            continue  # línea mal formada

        video_file, obj, count_str = parts
        video_file = f"{video_file}.mpg"

        try:
            count = int(count_str)
        except ValueError:
            continue  # si count no es entero, ignoramos

        if video_file not in data_raw:
            data_raw[video_file] = {
                "views": 0,
                "objects": []
            }

        data_raw[video_file]["objects"].append({
            "object": obj,
            "count": count
        })

    data_sorted = OrderedDict(
        sorted(
            (
                (video, {
                    "views": info["views"],
                    "objects": sorted(info["objects"], key=lambda o: o["count"], reverse=True)
                })
                for video, info in data_raw.items()
            ),
            key=lambda x: sum(obj["count"] for obj in x[1]["objects"]),
            reverse=True
        )
    )

    return data_sorted

def parse_spark_output_to_json(spark_output_str, output_hive_str):
    
    data_raw = {}
    views_map = {}

    # Parse Hive output (vistas por video)
    for line in output_hive_str.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        video_file, views_str = parts
        video_file = f"{video_file}.mpg"

        try:
            views = int(views_str)
        except ValueError:
            views = 0

        views_map[video_file] = views

    # Parse Spark output (objetos por video)
    for line in spark_output_str.strip().split('\n'):
        if not line.strip():
            continue

        parts = line.strip().split(',')
        if len(parts) != 3:
            continue  # línea mal formada

        video_file, obj, count_str = parts
        video_file = f"{video_file}.mpg"

        try:
            count = int(count_str)
        except ValueError:
            continue  # si count no es entero, ignoramos

        if video_file not in data_raw:
            data_raw[video_file] = {
                "views": views_map.get(video_file, 0),
                "objects": []
            }

        data_raw[video_file]["objects"].append({
            "object": obj,
            "count": count
        })

    data_sorted = OrderedDict(
        sorted(
            (
                (video, {
                    "views": info["views"],
                    "objects": sorted(info["objects"], key=lambda o: o["count"], reverse=True)
                })
                for video, info in data_raw.items()
            ),
            key=lambda x: x[1]["views"],
            reverse=True
        )
    )

    return data_sorted
