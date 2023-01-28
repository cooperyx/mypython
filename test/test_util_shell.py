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

    def test_remote_cp_file(self):
        user = "yanxu"
        ip = "192.168.0.228"
        passwd = "xxxx"
        src_path = __file__
        tar_path = "/home/yanxu/tmp_scripts/a.sh"
        remote_scp_file(ip, user, passwd, src_path, tar_path)

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


    def test_start_basecall_gpu(self):
        data_name = "20211109193132__WT02__5K_PC28_B16_HD42_AD3_Ecoli_j4_wangshengwen"
        ip, gpu, jobs = "192.168.0.228", 7, 3
        _ = delete_basecall_res(data_name)
        # local_basecll(ip, gpu, data_name, jobs)

    def test_start_basecall_gpu_all(self):
        data_name = "20211010_LAB256_5K_test_yx"
        local_basecll("192.168.0.228", 4, data_name, 3)
        # data_name = "20211119084655_WTseqV1_5K_PC28_28_B16_HD25_J4_A_AD3_Ecoli_ChenWei"
        # local_basecll("192.168.0.228", 1, data_name, 3)
        # data_name = "20211119141645_WTseqV1_5K_PC28_28_B16_HD25_J4_A_AD3_Ecoli_ChenWei"
        # local_basecll("192.168.0.228", 2, data_name, 3)


    def test_start_basecall_inspur(self):
        ip, gpu, jobs = "172.16.18.16", 0, 10
        data_name = "20211109193132__WT02__5K_PC28_B16_HD42_AD3_Ecoli_j4_wangshengwen"
        cp_folders_from_output_data(data_name, ip)
        # _ = delete_basecall_res(data_name)
        # local_basecll(ip, gpu, data_name, jobs)
