# flake report, week ending 2026-08-13

18 confirmed flakes in 14 signatures this week.

## 3x  `[FAIL] Podman run networking [It] podman run bridge multiple containers same network different ports`
jobs: int local rootless debian-sid, int local rootless fedora-rawhide, int remote rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31535365546/job/94053002455
- https://github.com/podman-container-tools/podman/actions/runs/31535365546/job/94053002734
- https://github.com/podman-container-tools/podman/actions/runs/31388391879/job/93457200219

## 3x  `(no log / no marker)`
jobs: Validate source code changes, int remote rootless fedora-current, sys local rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31508241936/job/93835206236
- https://github.com/podman-container-tools/podman/actions/runs/31409432964/job/93527219424
- https://github.com/podman-container-tools/podman/actions/runs/31304615246/job/93492863519

## 1x  `[FAIL] podman machine set [It] set rootful with docker sock change`
jobs: macos machine libkrun
- https://github.com/podman-container-tools/podman/actions/runs/31609473874/job/94161435950

## 1x  `make: *** [TARGET] Error 1`
jobs: Validate source code changes
- https://github.com/podman-container-tools/podman/actions/runs/31594925821/job/94108049621

## 1x  `[FAIL] Podman rmi [It] podman image rm - concurrent with shared layers`
jobs: int local root fedora-rawhide
- https://github.com/podman-container-tools/podman/actions/runs/31594925821/job/94130233395

## 1x  `not ok \|N\| podman run --cgroups=disabled keeps the current cgroup`
jobs: sys local root fedora-rawhide
- https://github.com/podman-container-tools/podman/actions/runs/31583231056/job/94082573235

## 1x  `make: *** [TARGET] Error 60`
jobs: macos installer
- https://github.com/podman-container-tools/podman/actions/runs/31535365546/job/93942837789

## 1x  `[FAIL] podman machine init [It] simple init with start`
jobs: macos machine libkrun
- https://github.com/podman-container-tools/podman/actions/runs/31527128471/job/93903188389

## 1x  `[FAIL] Podman port [It] podman port nginx by name`
jobs: int local rootless fedora-prior
- https://github.com/podman-container-tools/podman/actions/runs/31527128471/job/93903189328

## 1x  `[FAIL] podman machine start [It] start two machines in parallel`
jobs: macos machine libkrun
- https://github.com/podman-container-tools/podman/actions/runs/31408636467/job/93527815162

## 1x  `[FAIL] podman system reset [It] system reset completely removes container [Serial]`
jobs: int local root fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31388433472/job/93457337233

## 1x  `not ok [N] podman network reload`
jobs: sys local root fedora-rawhide
- https://github.com/podman-container-tools/podman/actions/runs/31388391879/job/93457200292

## 1x  `not ok \|N\| podman mount no-dereference`
jobs: sys local rootless debian-sid
- https://github.com/podman-container-tools/podman/actions/runs/31304615246/job/93492863484

## 1x  `not ok \|N\| quadlet - image tag`
jobs: sys local rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31171540579/job/92847046566

