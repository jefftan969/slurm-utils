# Slurm Utilities

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

## Show queued jobs (sorted by priority) and running jobs (sorted by node name)

Run `./slurm_jobs.py`. Example result:

```
======== Queued Jobs: ========
JobID     Priority    TimeQueued     PlanStart      PlanEnd        Duration    User                 GPUs
30479540  5115841     250416-142444  250420-093638  250425-093638  5-00:00:00  cis200000p/jefftan   GPUs=h100:4   	Notes=Resources
30284220  145884      250407-154526  250425-014856  250427-014856  2-00:00:00  cis200000p/jefftan   GPUs=h100-80:8 	Notes=ReqNodeNotAvail,_UnavailableNodes:w[001-002]
JobID     Priority    TimeQueued     PlanStart      PlanEnd        Duration    User                 GPUs
======== Running Jobs: ========
JobID     Node        TimeQueued     TimeStart      TimeEnd        Duration    User                 GPUs
30647173  v001        250419-102948  250419-103308  250419-223308  12:00:00    cis200000p/jefftan   GPUs=v100-16:1   
30542305  v003        250418-000901  250418-011152  250423-011152  5-00:00:00  cis200000p/jefftan   GPUs=v100-32:3
JobID     Node        TimeQueued     TimeStart      TimeEnd        Duration    User                 GPUs
```

Filter the result by partition, GPU type, or node type:
```
./slurm_jobs.py -p GPU-shared
./slurm_jobs.py -g h100-80
./slurm_jobs.py -n w
```

Pass `-q` to show only queued jobs, or `-r` to show only running jobs.
