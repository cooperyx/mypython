"""
先实现host上执行shell -- 通过local_run_cmd
再实现远程执行shell -- 通过remote_run_cmd
"""


from unittest import TestCase
from utils.util_shell import *


class UtilTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_local_run_cmd(self):
        cmd = "ls -l /home/yanxu/"
        # cmd = "sshpass -p xxxx ssh yanxu@192.168.0.228 'echo xxxx | sudo -S chmod -R 777 tmp_scripts'"
        # cmd = "sshpass -p xxxx ssh -t yanxu@192.168.0.228 'sudo -S pwd'"
        # cmd = "ssh yanxu@192.168.0.228 'echo xxxx | sudo -S chmod -R 777 tmp_scripts'"
        # cmd = "echo xxxx | ssh -tt yanxu@192.168.0.228 'sudo chmod -R 777 tmp_scripts'"
        local_run_cmd(cmd)

    def test_local_run_sudo_cmd(self):
        user = "yanxu"
        passwd = "xxxx"
        # cmd = "chown -R yanxu:yanxu /home/yanxu/test_folder"
        cmd = "chmod -R 777  /home/yanxu/test_folder"
        local_sudo_run_cmd(user, passwd, cmd)

    def test_remote_run_cmd(self):
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        sub_cmd = "ls -l tmp_scripts"
        # sub_cmd = "pwd"
        remote_run_cmd(ip, user, passwd, sub_cmd)

    def test_remote_sudo_run_cmd(self):
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        cmd = "chmod -R 777 /home/yanxu/tmp_scripts"
        remote_sudo_run_cmd(ip, user, passwd, cmd)

    def test_remote_cp_file(self):
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        src_path = __file__
        tar_path = "/home/yanxu/tmp_scripts/a.sh"
        remote_scp_file(ip, user, passwd, src_path, tar_path)

    def test_remote_nohup(self):
        """
        实现远程多任务并行
        :return:
        """
        # 1. 复制nohup脚本到远程主机, 其中nohup脚本写成传参形式
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        src_path = "./nohup.sh"
        tar_path = "/home/yanxu/tmp_scripts/a.sh"
        remote_scp_file(ip, user, passwd, src_path, tar_path)
        # 2. 远程执行shell脚本
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        sub_cmd = "bash nohup.sh --run_id {}  --name {}"
        # sub_cmd = "pwd"
        remote_run_cmd(ip, user, passwd, sub_cmd)




