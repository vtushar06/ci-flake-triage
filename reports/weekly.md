# flake report, week ending 2026-08-30

27 confirmed flakes in 10 signatures this week.

## 12x  `(no log / no marker)`
jobs: Validate source code changes, build fedora-prior, int remote rootless fedora-current, macos machine applehv, sys local root fedora-current, sys local root fedora-rawhide, sys local rootless debian-sid, sys local rootless fedora-prior, upgrade v5.6.2 root fedora-current, windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/32739675019/job/97474966110
- https://github.com/podman-container-tools/podman/actions/runs/32739675019/job/97474968998
- https://github.com/podman-container-tools/podman/actions/runs/32739675019/job/97474969872

## 5x  `[FAIL] podman machine init [It] machine init with cpus, disk size, memory, timezone`
jobs: macos machine applehv, windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/33065037209/job/98495761852
- https://github.com/podman-container-tools/podman/actions/runs/32867130768/job/97869193925
- https://github.com/podman-container-tools/podman/actions/runs/32867130768/job/97869194115

## 2x  `[FAIL] podman machine set [It] set machine cpus, disk, memory`
jobs: windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/33096793134/job/98610199555
- https://github.com/podman-container-tools/podman/actions/runs/32907273049/job/97996913695

## 2x  `[FAIL] run cp commands [DeferCleanup (Each)] podman cp`
jobs: windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/32948408367/job/98117072846
- https://github.com/podman-container-tools/podman/actions/runs/32875465747/job/97897646841

## 1x  `[FAIL] run cp commands [It] podman machine cp`
jobs: windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/33064912684/job/98495341304

## 1x  `[FAIL] Podman run networking [It] podman run bridge multiple containers same network different ports`
jobs: int local rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/32994320302/job/98264135878

## 1x  `[FAIL] Podman rmi [It] podman image rm - concurrent with shared layers`
jobs: int local rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/32973631956/job/98197170457

## 1x  `[FAIL] podman machine start [It] start machine already started`
jobs: windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/32766359585/job/97560430153

## 1x  `not ok [N] podman network create`
jobs: sys local root fedora-prior
- https://github.com/podman-container-tools/podman/actions/runs/32766359585/job/97560433074

## 1x  `[FAIL] podman machine start [It] start machine with conflict on SSH port`
jobs: macos machine applehv
- https://github.com/podman-container-tools/podman/actions/runs/32721285226/job/97416447518

