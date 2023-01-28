import logging.config
from conf import PROJ_DIR
import subprocess
import re
import os
import paramiko
import logging

LOG_PATH = "{}/logs/util_shell.log".format(PROJ_DIR)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    filename = LOG_PATH,
    # filemode="w"
)


def log_subprocess_output(pipe, log_obj):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        log_obj.info('got line from subprocess: %r', line.decode("utf-8"))


def local_run_cmd(cmd_str):
    logging.info(cmd_str)
    process = subprocess.Popen(
        cmd_str.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    with process.stdout:
        log_subprocess_output(process.stdout, logging)
    exitcode = process.wait()


def remote_scp_file(tar_ip, tar_user, tar_passwd, src_path, tar_path):
    cmd = "sshpass -p {} scp {} {}@{}:{}".format(
        tar_passwd,
        src_path,
        tar_user,
        tar_ip,
        tar_path
    )
    local_run_cmd(cmd)


def remote_scp_folder(tar_ip, tar_user, tar_passwd, src_path, tar_path):
    cmd = "sshpass -p {} scp {} {}@{}:{}".format(
        tar_passwd,
        src_path,
        tar_user,
        tar_ip,
        tar_path
    )
    local_run_cmd(cmd)


def remote_run_cmd(tar_ip, tar_user, tar_passwd, tar_cmd):
    cmd ="sshpass -p {} ssh -o ConnectTimeout=3 {}@{} {}".format(
        tar_passwd,
        tar_user,
        tar_ip,
        tar_cmd
    )
    local_run_cmd(cmd)


class SSH:
    def __init__(self):
        pass

    def get_ssh_connection(self, ssh_machine, ssh_username, ssh_password):
        """
          Establishes a ssh connection to execute command.
            :param ssh_machine: IP of the machine to which SSH connection to be established.
            :param ssh_username: User Name of the machine to which SSH connection to be established..
            :param ssh_password: Password of the machine to which SSH connection to be established..
            returns connection Object
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_machine, username=ssh_username, password=ssh_password, timeout=10)
        logging.info("try to connect")
        return client

    def run_sudo_command(self, ssh_username="root", ssh_password="abc123", ssh_machine="localhost", command="ls",
                         jobid="None"):
        """Executes a command over a established SSH connectio.
        :param ssh_machine: IP of the machine to which SSH connection to be established.
        :param ssh_username: User Name of the machine to which SSH connection to be established..
        :param ssh_password: Password of the machine to which SSH connection to be established..
        returns status of the command executed and Output of the command.
        """
        conn = self.get_ssh_connection(ssh_machine=ssh_machine, ssh_username=ssh_username, ssh_password=ssh_password)
        command = "sudo -S -p '' %s" % command
        logging.info("Job[%s]: Executing: %s" % (jobid, command))
        stdin, stdout, stderr = conn.exec_command(command=command)
        stdin.write(ssh_password + "\n")
        stdin.flush()
        stdoutput = [line for line in stdout]
        stderroutput = [line for line in stderr]
        for output in stdoutput:
            logging.info("Job[%s]: %s" % (jobid, output.strip()))
        # Check exit code.
        logging.info("Job[%s]:stdout: %s" % (jobid, stdoutput))
        logging.info("Job[%s]:stderror: %s" % (jobid, stderroutput))
        logging.info("Job[%s]:Command status: %s" % (jobid, stdout.channel.recv_exit_status()))
        # TEST
        conn.close()
        if not stdout.channel.recv_exit_status():
            logging.info("Job[%s]: Command executed." % jobid)
            conn.close()
            if not stdoutput:
                stdoutput = True
            return True, stdoutput
        else:
            logging.error("Job[%s]: Command failed." % jobid)
            for output in stderroutput:
                logging.error("Job[%s]: %s" % (jobid, output))
            conn.close()

            return False, stderroutput


def remote_sudo_run_cmd(ip, user, passwd, cmd):
    ssh_obj = SSH()
    ssh_obj.get_ssh_connection(ip, user, passwd)
    ssh_obj.run_sudo_command(
        ssh_username=user,
        ssh_password=passwd,
        ssh_machine=ip,
        command=cmd
    )


def local_sudo_run_cmd(user, passwd, cmd):
    ssh_obj = SSH()
    ssh_obj.get_ssh_connection("localhost", user, passwd)
    ssh_obj.run_sudo_command(
        ssh_username=user,
        ssh_password=passwd,
        ssh_machine="localhost",
        command=cmd
    )


def delete_basecall_res(data_name):
    data_dir = "/mnt/seqdata/output_data/{}/data_for_analysing".format(data_name)
    file_path_basename = "/mnt/seqdata/output_data/{}/data_for_analysing/{}".format(data_name, data_name)
    file_path_list = [val.format(file_path_basename) for val in ["{}.fastq",  "{}.sam", "{}.bam"]] + [
        "{}/res_mapping.log".format(data_dir),
        "{}/setting.conf".format(data_dir),
        "{}/basecall.log".format(data_dir),
    ]
    for file_path in file_path_list:
        cmd = "rm -f {}".format(file_path)
        local_sudo_run_cmd("yanxu", "xxxx", cmd)
    return data_dir


def local_basecll(ip, gpu_num, data_name, jobs, block=False):
    # 1. delete old res
    data_dir = delete_basecall_res(data_name)

    # 2. start basecall
    script_path = "/home/yanxu/basecall_data/basecall_to_output.sh"
    if not block:
        cmd = "nohup bash {}  {} {} {} > {}/basecall.log  2>&1  &".format(script_path, data_name, gpu_num, jobs, data_dir)
        remote_run_cmd(ip, "yanxu", "xxxx", cmd)
    else:
        cmd = "bash {}  {} {} {}".format(script_path, data_name, gpu_num, jobs)
        remote_run_cmd(ip, "yanxu", "xxxx", cmd)


def local_basecll_v1(ip, gpu_num, data_name, jobs, block=False):
    # 1. delete old res
    data_dir = delete_basecall_res(data_name)

    # 2. copy fast_5
    # cp_folders(tar_ip, tar_user, tar_passwd, src_path, tar_path)

    # 3. start basecall
    script_path = "/home/yanxu/basecall_data/basecall_to_output.sh"
    if not block:
        cmd = "nohup bash {}  {} {} {} > {}/basecall.log  2>&1  &".format(script_path, data_name, gpu_num, jobs, data_dir)
        remote_run_cmd(ip, "yanxu", "xxxx", cmd)

    else:
        cmd = "bash {}  {} {} {}".format(script_path, data_name, gpu_num, jobs)
        remote_run_cmd(ip, "yanxu", "xxxx", cmd)

    # 4.


def cp_folders_from_output_data(data_name, tar_ip):
    cmd = "cp -r /mnt/seqdata/output_data/{}/data_for_analysing/{}_fast5  /mnt/seqdata/output".format(
        data_name, data_name
    )
    logging.info(cmd)
    remote_run_cmd(tar_ip, "yanxu", "xxxx", cmd)
