# flake report, week ending 2026-09-01

25 confirmed flakes in 7 signatures this week.

## 15x  `(no log / no marker)`
jobs: Validate source code changes, int remote rootless fedora-current, macos machine applehv, macos machine libkrun, sys local root fedora-rawhide, sys local rootless debian-sid, sys local rootless fedora-prior, sys remote root fedora-prior, upgrade v5.6.2 root fedora-current, windows installer hyperv, windows installer wsl, windows machine hyperv
- https://github.com/podman-container-tools/podman/actions/runs/33024691199/job/98365766041
- https://github.com/podman-container-tools/podman/actions/runs/32874965888/job/97895039501
- https://github.com/podman-container-tools/podman/actions/runs/33064206102/job/98493018358

## 3x  `[FAIL] podman machine init [It] machine init with cpus, disk size, memory, timezone`
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

