#!/usr/bin/python3
# SLURM utility to print queued+running jobs (Author: Jeff Tan, jefftan@andrew.cmu.edu)
import argparse
import os


def print_job_info(ranking_criteria, job_id, job_info):
    """Print a job_info dict from `scontrol show jobs`, according to some
    ranking criteria (e.g. priority or node_name)"""
    alloc_tres = dict(elt.split("=", 1) for elt in job_info["TRES"].split(",") if "=" in elt)
    alloc_count = int(alloc_tres["gres/gpu"]) if "gres/gpu" in alloc_tres else 0
    user_id = job_info["UserId"].split("(")[0]
    group_id = job_info["GroupId"].split("(")[0]
    gpus = job_info["TresPerNode"] if "TresPerNode" in job_info else job_info["TresPerJob"]
    gpus = gpus.replace("gres:gpu:", "")
    dependency = None if job_info["Dependency"] == "(null)" else job_info["Dependency"].replace("afterany:", "after").replace("afterok:", "after").replace("_*", "").replace("(unfulfilled)", "")
    queue_time = dependency or job_info["AccrueTime"].replace("-", "").replace("T", "-").replace(":", "")[2:]
    start_time = job_info["StartTime"].replace("-", "").replace("T", "-").replace(":", "")[2:]
    end_time = job_info["EndTime"].replace("-", "").replace("T", "-").replace(":", "")[2:]
    duration = job_info["TimeLimit"]
    time_limit = job_info["TimeLimit"]
    notes = "" if job_info["Reason"] in ("None", "Priority", "Dependency") else "\tNotes=" + job_info["Reason"]
    print(f"{job_id:<8}  {ranking_criteria:<10}  {queue_time:<13}  {start_time:<13}  {end_time:<13}  {duration:<10}  {group_id}/{user_id:<8}  GPUs={gpus:<9}{notes}")


def main(part_type=None, gpu_type=None, node_type=None, print_running=True, print_queued=True):
    # Keys to limit results to a given partition, gpu type, or node type
    part_key = "" if part_type is None else part_type
    gpu_key = "gres:gpu" if gpu_type is None else f"gres:gpu:{gpu_type}"
    node_key = "" if node_type is None else node_type

    jobs = os.popen("scontrol show jobs").read().strip().split("\n\n")
    queued_jobs = []
    running_jobs = []
    for job_str in jobs:
        job_info = dict(line.strip().split("=", 1) for line in job_str.split() if "=" in line)
        if part_key not in job_info["Partition"] or gpu_key not in job_str or node_key not in job_info["NodeList"]:
            # Restrict results to the specified partition/GPU/node type
            continue

        job_id = int(job_info["JobId"])
        priority = int(job_info["Priority"])
        job_state = job_info["JobState"]
        node_list = job_info["NodeList"]

        if job_state == "PENDING":
            queued_jobs.append((priority, job_id, job_info))
        elif job_state == "RUNNING":
            running_jobs.append((node_list, job_id, job_info))
        # Other job state: CANCELLED, COMPLETED, COMPLETING, FAILED, OUT_OF_MEMORY, TIMEOUT

    if print_queued:
        print("======== Queued Jobs: ========")
        header_queued = "JobID     Priority    TimeQueued     PlanStart      PlanEnd        Duration    User                 GPUs"
        print(header_queued)
        for priority, job_id, job_info in sorted(queued_jobs, key=lambda x: (-x[0], x[1])):
            # Print queued jobs sorted by priority (descending) and job_id (low2high)
            print_job_info(priority, job_id, job_info)
        print(header_queued)

    if print_running:
        print("======== Running Jobs: ========")
        header_running = "JobID     Node        TimeQueued     TimeStart      TimeEnd        Duration    User                 GPUs"
        print(header_running)
        for node_list, job_id, job_info in sorted(running_jobs):
            # Print runnings jobs sorted by node_name (ascending) and job_id (ascending)
            print_job_info(node_list, job_id, job_info)
        print(header_running)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", type=str, default=None, help="Limit search to a partition (e.g. 'ROBO')")
    parser.add_argument("-g", "--gpu", type=str, default=None, help="Limit search to a GPU type (e.g. 'h100')")
    parser.add_argument("-n", "--node", type=str, default=None, help="Limit search to a node type (e.g. 'w')")
    parser.add_argument("-q", "--queued", default=False, action="store_true", help="Only print queued jobs")
    parser.add_argument("-r", "--running", default=False, action="store_true", help="Only print running jobs")
    args = parser.parse_args()

    main(
        part_type=args.part, gpu_type=args.gpu, node_type=args.node,
        print_running=not args.queued, print_queued=not args.running,
    )
