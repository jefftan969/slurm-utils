# Slurm Utilities + Dashboards

## Show available GPUs per node

Run `./slurm_open_gpus.py`. Example result:

```
v100-32 available:
  v001: 2/8
  v002: 2/8
  v009: 1/8
  v020: 1/8
v100-16 available:
  v025: 3/8
  v028: 8/8
  v030: 3/8
```

## Show pending jobs, sorted by priority

Run `./slurm_pending_jobs.py`. Example result:

```
Pending Jobs:
Priority=142800	Job=30277396	Queued=2025-04-07T02:27:41	User=cis200000p/jefftan969	GPUs=v100-32:4	Notes=PENDING Reason=Resources Dependency=(null)
Priority=111404	Job=30284220	Queued=2025-04-07T15:45:26	User=cis200000p/jefftan969	GPUs=h100:8	Notes=PENDING Reason=ReqNodeNotAvail,_UnavailableNodes:w[001-009] Dependency=(null)
```

Filter the result by partition, GPU type, or node name:
```
./slurm_pending_jobs.py --part GPU-shared
./slurm_pending_jobs.py --gpu h100-80
./slurm_pending_jobs.py --node w
```

## Show running jobs, sorted by node

Run `./slurm_running_jobs.py`. Example result:

```
Running Jobs:
Node=v016	Job=30565232	Started=2025-04-18T08:28:39	User=cis200000p/jefftan969	GPUs=v100-16:1
Node=v034	Job=30564882	Started=2025-04-18T09:38:22	User=cis200000p/jefftan969	GPUs=v100-32:4
```

Filter the result by partition, GPU type, or node name:
```
./slurm_running_jobs.py --part GPU-shared
./slurm_running_jobs.py --gpu h100-80
./slurm_running_jobs.py --node w
```
