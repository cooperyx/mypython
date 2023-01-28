#!/bin/bash

run_name=$1
sample_id=$2
proj_dir=/home/alpha_test/deploy_projects/web9082

nohup  $proj_dir/deploy/venv/bin/python3 \
    -u $proj_dir/util_copy_args.py   \
    --run_name $run_name  \
    --sample_id $sample_id  \
    >  /home/alpha_test/gen_report.log  2>&1  &
