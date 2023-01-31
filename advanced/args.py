import sys
sys.path.append("/home/cyclone_public/basecall_api")

import time
import argparse
import requests
from util import processing_data, logger
import os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_type", type=str, help="")
    parser.add_argument("--data_name", type=str, help="")
    parser.add_argument("--model_name", type=str, help="")
    parser.add_argument("--auto_trim_adaptor", type=str, help="", default="0")
    return parser


def update_task_info(args, key, value):
    params = {
        "data_name": args.data_name,
        "task_type": args.task_type,
        "info": {key: value}
    }
    r = requests.post("http://192.168.0.106:9083/update_running_task", json=params)
    if not r.status_code == 200:
        # TODO add log
        pass


def done_recorder(args,error):
    params = {
        "data_name": args.data_name,
        "task_type": args.task_type,
        "error": error
    }
    r = requests.post("http://192.168.0.106:9083/done_recorder", json=params)
    if not r.status_code == 200:
        # TODO add log
        pass


def local_time():
    time_now = int(time.time())
    # 转换成localtime
    time_local = time.localtime(time_now)
    # 转换成新的时间格式(2022-02-17 15:11:20)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def main():
    # 1. get params
    args = get_parser().parse_args()
    # 2. update task info
    update_task_info(args, "task_status", "start running ...")
    update_task_info(args, "pid", os.getpid())
    # 3. start process data
    start_time = time.time()

    try:
        processing_data(args.data_name, args.model_name, args.auto_trim_adaptor)
        task_status = "end and succeed"
        update_task_info(args, "tooktime", time.time()-start_time)
        update_task_info(args, "endtime", local_time())
        update_task_info(args, "task_status", task_status)
    except Exception as err:
        logger.error("ERROR: {}: {}".format(args.data_name, str(err)))
        task_status = "end but failed"
        update_task_info(args, "tooktime", time.time()-start_time)
        update_task_info(args, "error", str(err))

    # 4. delete task
    done_recorder(args, task_status)


if __name__=="__main__":
    main()





