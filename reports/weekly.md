# flake report, week ending 2026-08-17

90 confirmed flakes in 21 signatures this week.

## 33x  `(no log / no marker)`
jobs: Validate source code changes, bud local root fedora-current, compose_v2  root fedora-current, compose_v2  rootless fedora-current, int local root debian-sid, int local root fedora-rawhide, int local rootless debian-sid, int local rootless fedora-prior, int remote root fedora-prior, int remote rootless fedora-current, macos machine libkrun, sys local root debian-sid, sys local root fedora-current, sys local root fedora-rawhide, sys local rootless debian-sid, sys local rootless fedora-current, sys remote root fedora-prior, sys remote root fedora-rawhide, unit  root fedora-current, windows machine hyperv, windows machine wsl
- https://github.com/podman-container-tools/podman/actions/runs/31635164657/job/94259259703
- https://github.com/podman-container-tools/podman/actions/runs/31839624435/job/94893455317
- https://github.com/podman-container-tools/podman/actions/runs/31804911176/job/94787335666

## 31x  `(no log / no marker)`
jobs: Validate source code changes, apiv2  root fedora-current, apiv2  rootless fedora-current, bindings  root fedora-current, bud local root fedora-current, build debian-sid, build fedora-current, build fedora-rawhide, compose_v2  root fedora-current, int local root fedora-current, int local root fedora-prior, int local root fedora-rawhide, int local rootless fedora-current, int remote root debian-sid, int remote rootless fedora-current, machine linux amd64, sys local root fedora-rawhide, sys local rootless debian-sid, sys local rootless fedora-prior, unit  root fedora-current, windows installer hyperv, windows installer wsl
- https://github.com/podman-container-tools/podman/actions/runs/31508241936/job/93835206236
- https://github.com/podman-container-tools/podman/actions/runs/31409432964/job/93527219424
- https://github.com/podman-container-tools/podman/actions/runs/31673722979/job/94410956845

## 4x  `make: *** [TARGET] Error 1`
jobs: Validate source code changes
- https://github.com/podman-container-tools/podman/actions/runs/31594925821/job/94108049621
- https://github.com/podman-container-tools/podman/actions/runs/31714125771/job/94494366085
- https://github.com/podman-container-tools/podman/actions/runs/31709559909/job/94479022625

## 3x  `[FAIL] Podman run networking [It] podman run bridge multiple containers same network different ports`
jobs: int local rootless debian-sid, int local rootless fedora-rawhide, int remote rootless fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31535365546/job/94053002455
- https://github.com/podman-container-tools/podman/actions/runs/31535365546/job/94053002734
- https://github.com/podman-container-tools/podman/actions/runs/31388391879/job/93457200219

## 3x  `[FAIL] Podman build [It] podman build --build-context: URL source`
jobs: int local root fedora-prior, int local rootless fedora-current, int remote root fedora-prior
- https://github.com/podman-container-tools/podman/actions/runs/31635164657/job/94259260188
- https://github.com/podman-container-tools/podman/actions/runs/31620875719/job/94204768736
- https://github.com/podman-container-tools/podman/actions/runs/31620875719/job/94204768944

## 1x  `[FAIL] podman machine set [It] set rootful with docker sock change`
jobs: macos machine libkrun
- https://github.com/podman-container-tools/podman/actions/runs/31609473874/job/94161435950

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

## 1x  `[FAIL] Podman pod stop [It] podman pod start/stop single pod via --pod-id-file`
jobs: int local root debian-sid
- https://github.com/podman-container-tools/podman/actions/runs/31730666358/job/94554132184

## 1x  `not ok \|N\| podman autoupdate local`
jobs: sys local root fedora-rawhide
- https://github.com/podman-container-tools/podman/actions/runs/31728021211/job/94566503128

## 1x  `[FAIL] run basic podman commands [It] Basic ops`
jobs: windows machine wsl
- https://github.com/podman-container-tools/podman/actions/runs/31723951112/job/94531471286

## 1x  `not ok \|N\| podman healthcheck`
jobs: sys remote root fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31707172259/job/94475153937

## 1x  `[FAIL] Podman run with volumes [It] podman named volume copyup`
jobs: int local root debian-sid
- https://github.com/podman-container-tools/podman/actions/runs/31679740179/job/94385285864

## 1x  `[FAIL] podman machine proxy settings propagation [It] ssh to running machine and check proxy setting`
jobs: macos machine applehv
- https://github.com/podman-container-tools/podman/actions/runs/31635164657/job/94423262642

## 1x  `not ok \|N\| podman run docker-archive`
jobs: sys local root fedora-current
- https://github.com/podman-container-tools/podman/actions/runs/31635164657/job/94259260278

