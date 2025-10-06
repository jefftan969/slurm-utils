# Slurm Utilities

## Show available GPUs per node

Run `./slurm_open_gpus.py`. Example result:

```
v100-32 available:
  v001: 2/8  (Mem   63G/250G  | CPU  12/32  )
  v002: 2/8  (Mem   63G/250G  | CPU  12/32  )
  v009: 1/8  (Mem    3G/250G  | CPU   4/32  )
  v020: 1/8  (Mem  145G/250G  | CPU   8/32  )
v100-16 available:
  v025: 3/8  (Mem 1015G/2015G | CPU  71/104 )
  v028: 8/8  (Mem 2015G/2015G | CPU 104/104 )
  v030: 3/8  (Mem 1014G/2015G | CPU  72/104 )
```

## Show queued jobs (sorted by priority) and running jobs (sorted by node name)

Run `./slurm_jobs.py`. Example result:

```
======== Queued Jobs: ========
JobID     Priority    TimeQueued     PlanStart      PlanEnd        Duration    User                 GPU       Mem      CPU
30479540  5115841     250416-142444  250420-093638  250425-093638  5-00:00:00  cis200000p/jefftan   h100:4    97250M   16   Notes=Resources
30284220  145884      250407-154526  250425-014856  250427-014856  2-00:00:00  cis200000p/jefftan   h100-80:8 960G     96   Notes=ReqNodeNotAvail,_UnavailableNodes:w[001-002]
JobID     Priority    TimeQueued     PlanStart      PlanEnd        Duration    User                 GPUs
======== Running Jobs: ========
JobID     Node        TimeQueued     TimeStart      TimeEnd        Duration    User                 GPUs
30647173  v001        250419-102948  250419-103308  250419-223308  12:00:00    cis200000p/jefftan   v100-16:1 250G     4
30542305  v003        250418-000901  250418-011152  250423-011152  5-00:00:00  cis200000p/jefftan   v100-32:3 500G     8
JobID     Node        TimeQueued     TimeStart      TimeEnd        Duration    User                 GPUs
```

Filter the result by partition, GPU type, node type, or user:
```
./slurm_jobs.py -p GPU-shared
./slurm_jobs.py -g h100-80
./slurm_jobs.py -n w
./slurm_jobs.py -u jefftan
```

Pass `-q` to show only queued jobs, or `-r` to show only running jobs.
