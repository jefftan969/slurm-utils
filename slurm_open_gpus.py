#!/usr/bin/python3
# SLURM utility to print available GPUs (Author: Jeff Tan, jefftan@andrew.cmu.edu)
import argparse
import os

def main(part_type=None, gpu_type=None, node_type=None):
    part_key = "" if part_type is None else part_type
    gpu_key = "" if gpu_type is None else f"gpu:{gpu_type}:"
    node_key = "" if node_type is None else node_type

    nodes = os.popen("scontrol show nodes").read().strip().split("\n\n")
    avail_gpus = {}
    for node_str in nodes:
        node_info = dict(line.strip().split("=", 1) for line in node_str.split() if "=" in line)
        if node_info["Gres"] == "(null)":
            # Not a GPU node
            continue
        if part_key not in node_info["Partitions"] or gpu_key not in node_info["Gres"] or node_key not in node_info["NodeAddr"]:
            # No available GPUs of the specified partition/GPU/node type
            continue

        gpu_avail = node_info["Gres"].split(":", 2)
        assert len(gpu_avail) == 3 and gpu_avail[0] == "gpu", gpu_avail
        gpu_type = gpu_avail[1]
        gpu_count = int(gpu_avail[2].split("(")[0])

        # Extract number of available and allocated GPUs
        cfg_tres = dict(elt.split("=", 1) for elt in node_info["CfgTRES"].split(",") if len(elt) > 0)
        cfg_gpus = int(cfg_tres["gres/gpu"])
        cfg_mem = round(int(node_info["RealMemory"]) // 1024)
        cfg_cpus = int(cfg_tres["cpu"])
        assert cfg_gpus == gpu_count, (cfg_gpus, gpu_count)
        alloc_tres = dict(elt.split("=", 1) for elt in node_info["AllocTRES"].split(",") if len(elt) > 0)
        alloc_gpus = int(alloc_tres["gres/gpu"]) if "gres/gpu" in alloc_tres else 0
        alloc_mem = round(int(node_info["AllocMem"]) // 1024)
        alloc_cpus = int(alloc_tres["cpu"]) if "cpu" in alloc_tres else 0

        node_name = node_info["NodeName"]
        if gpu_type not in avail_gpus:
            avail_gpus[gpu_type] = []
        if "DOWN" in node_info["State"] or "DRAIN" in node_info["State"]:
            # Node is down or drained
            avail_gpus[gpu_type].append((node_name, node_info["State"], node_str.split("Reason=")[1]))
        else:
            avail_gpus[gpu_type].append((node_name, alloc_gpus, alloc_mem, alloc_cpus, cfg_gpus, cfg_mem, cfg_cpus))

    for gpu_type, avail_list in avail_gpus.items():
        # Print available and allocated GPUs+Memory+CPUs, in total and separately for each node
        total_avail_gpus = 0
        total_count_gpus = 0
        for x in avail_list:
            if len(x) == 7:
                node_name, alloc_gpus, alloc_mem, alloc_cpus, cfg_gpus, cfg_mem, cfg_cpus = x
                total_avail_gpus += cfg_gpus - alloc_gpus
                total_count_gpus += cfg_gpus
        print(f"{gpu_type} available: {total_avail_gpus}/{total_count_gpus}")
        for x in avail_list:
            if len(x) == 7:
                node_name, alloc_gpus, alloc_mem, alloc_cpus, cfg_gpus, cfg_mem, cfg_cpus = x
                if alloc_gpus < cfg_gpus:
                    print(f"  {node_name:<10}: {cfg_gpus - alloc_gpus}/{cfg_gpus}  (Mem {str(cfg_mem - alloc_mem) + 'G':>5}/{str(cfg_mem) + 'G':<5} | CPU {cfg_cpus - alloc_cpus:>3}/{cfg_cpus:<3})")
            elif len(x) == 3:
                node_name, node_state, node_reason = x
                print(f"  {node_name:<10}: {node_state} ({node_reason})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", type=str, default=None, help="Limit search to a partition (e.g. 'ROBO')")
    parser.add_argument("-g", "--gpu", type=str, default=None, help="Limit search to a GPU type (e.g. 'h100')")
    parser.add_argument("-n", "--node", type=str, default=None, help="Limit search to a node type (e.g. 'w')")
    args = parser.parse_args()

    main(part_type=args.part, gpu_type=args.gpu, node_type=args.node)
