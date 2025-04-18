#!/usr/bin/python3
# SLURM utility to print pending jobs (Author: Jeff Tan, jefftan@andrew.cmu.edu)
import argparse
import os

def main(part_type=None, gpu_type=None, node_type=None):
    part_key = "" if part_type is None else part_type + " "
    gpu_key = "gres:gpu" if gpu_type is None else f"gres:gpu:{gpu_type}"
    node_key = "" if node_type is None else node_type

    jobs = os.popen("scontrol show jobs").read().strip().split("\n\n")
    pending_jobs = []
    for job_str in jobs:
        job_info = dict(line.strip().split("=", 1) for line in job_str.split("\n") if len(line.strip()) > 0)
        if part_key not in job_info["Partition"] or gpu_key not in job_str or node_key not in job_info["NodeList"]:
            # No allocated GPUs of the specified partition/GPU/node type
            continue

        job_id = int(job_info["JobId"].split(" ")[0])
        priority = int(job_info["Priority"].split(" ")[0])
        job_state = job_info["JobState"].split(" ")[0]
        node_list = job_info["NodeList"]

        if job_state == "PENDING":
            pending_jobs.append((priority, job_id, job_info))
        # Other job state: RUNNING, CANCELLED, COMPLETED, COMPLETING, FAILED, OUT_OF_MEMORY, TIMEOUT

    print("Pending Jobs:")
    for priority, job_id, job_info in sorted(pending_jobs, key=lambda x: (-x[0], x[1])):
        alloc_tres = dict(elt.split("=", 1) for elt in job_info["TRES"].split(",") if len(elt) > 0)
        alloc_count = int(alloc_tres["gres/gpu"]) if "gres/gpu" in alloc_tres else 0
        user_id = job_info["UserId"].split("(")[0]
        group_id = job_info["UserId"].split("GroupId=")[1].split("(")[0]
        gpus = job_info["TresPerNode"] if "TresPerNode" in job_info else job_info["TresPerJob"]
        gpus = gpus.replace("gres:gpu:", "")
        queue_time = job_info["AccrueTime"]
        job_state = job_info["JobState"]
        notes = "" if job_state == "PENDING Reason=Priority Dependency=(null)" else f"\tNotes={job_state}"
        print(f"Priority={priority}\tJob={job_id}\tQueued={queue_time}\tUser={group_id}/{user_id}\tGPUs={gpus}{notes}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=str, default=None, help="Limit search to a given partition")
    parser.add_argument("--gpu", type=str, default=None, help="Limit search to a given GPU type")
    parser.add_argument("--node", type=str, default=None, help="Limit search to a given node type")
    args = parser.parse_args()

    main(part_type=args.part, gpu_type=args.gpu, node_type=args.node)
