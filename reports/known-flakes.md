# known flakes - podman-container-tools/podman

Generated 2026-08-23 from the rerun history. 1615 completed runs (2026-06-01 to 2026-08-23), 462 re-run by hand, 672 confirmed flakes - 428 of them in 166 signatures, the rest with no marker or no log.

A confirmed flake failed on one attempt and passed on a later attempt of the same run, so the commit never changed. Issue matches below are candidates, not verdicts - in the study this tool grew out of, 6 of 16 name-based matches moved once the logs were opened (docs/verification.md). Anything marked needs-check requires a human before it is used.

## test failures (393 flakes, 163 signatures)

| n | signature | window | issue candidate |
|---|---|---|---|
| 30 | `not ok \|N\| podman healthcheck` | 2026-06-02 to 2026-08-13 | #23871 needs-check |
| 14 | `[FAIL] Podman prune [It] podman system prune --build clean up after terminated build` | 2026-06-02 to 2026-07-21 | #28868 needs-check |
| 12 | `[FAIL] run cp commands [DeferCleanup (Each)] podman cp` | 2026-06-16 to 2026-07-22 |  |
| 9 | `[FAIL] Podman rmi [It] podman image rm - concurrent with shared layers` | 2026-06-08 to 2026-08-12 |  |
| 9 | `not ok \|N\| quadlet - image tag` | 2026-06-02 to 2026-08-07 | #24598 needs-check |
| 9 | `[FAIL] Podman run networking [It] podman run container with two static IPs one per subnet` | 2026-06-04 to 2026-06-29 |  |
| 8 | `not ok \|N\| podman update - set ulimits` | 2026-06-10 to 2026-07-13 |  |
| 8 | `not ok \|N\| podman kube play --wait with siginterrupt` | 2026-06-04 to 2026-07-07 | #21560 needs-check |
| 7 | `[FAIL] Podman run memory [It] podman run memory test on oomkilled container` | 2026-06-08 to 2026-07-28 |  |
| 7 | `not ok \|N\| check Go template formatting` | 2026-06-04 to 2026-07-21 |  |
| 7 | `[FAIL] run basic podman commands [It] Basic ops` | 2026-06-04 to 2026-08-13 | #26547 needs-check |
| 6 | `[FAIL] podman machine init [It] machine init with cpus, disk size, memory, timezone` | 2026-06-02 to 2026-08-01 |  |
| 6 | `not ok \|N\| podman run --timeout - basic test` | 2026-06-04 to 2026-07-22 | #26547 needs-check |
| 6 | `[FAIL] Podman run [It] podman run with cgroups=split` | 2026-06-04 to 2026-07-20 |  |
| 6 | `not ok \|N\| podman container rm doesn't affect stopping containers` | 2026-06-02 to 2026-06-19 |  |
| 5 | `not ok \|N\| podman mount - basic test` | 2026-06-11 to 2026-07-14 | #24223 needs-check |
| 5 | `not ok [N] podman run - default_host_ips from containers.conf` | 2026-06-11 to 2026-06-28 |  |
| 5 | `not ok \|N\| podman stop - can trap signal` | 2026-06-01 to 2026-06-02 |  |
| 4 | `[FAIL] podman machine init [It] simple init with start` | 2026-06-15 to 2026-08-11 | #26547 needs-check |
| 4 | `not ok [N] podman network reload` | 2026-06-05 to 2026-08-10 | #17288 needs-check |
| 4 | `[FAIL] run basic podman commands [It] podman build contexts` | 2026-06-08 to 2026-07-27 |  |
| 4 | `[FAIL] run basic podman commands [It] Podman ops with port forwarding and gvproxy` | 2026-06-04 to 2026-07-16 |  |
| 4 | `not ok \|N\| TCP port range forwarding, IPv4, loopback` | 2026-06-04 to 2026-07-13 |  |
| 4 | `not ok [N] podman checkpoint/restore - publish with default_host_ips` | 2026-06-07 to 2026-07-07 | #24571 needs-check |
| 4 | `not ok [N] podman networking: port with --userns=keep-id for rootless or --uidmap=* for ro` | 2026-06-01 to 2026-07-03 |  |
| 4 | `not ok \|N\| TCP port range forwarding, IPv6, loopback` | 2026-06-01 to 2026-06-24 |  |
| 4 | `[FAIL] Podman build [It] podman build --build-context: URL source` | 2026-06-12 to 2026-08-12 |  |
| 3 | `[FAIL] Podman run networking [It] podman run bridge multiple containers same network diffe` | 2026-08-10 to 2026-08-11 |  |
| 3 | `[FAIL] podman machine start [It] start two machines in parallel` | 2026-07-08 to 2026-08-10 | #22551 needs-check |
| 3 | `[FAIL] podman system reset [It] system reset completely removes container [Serial]` | 2026-06-10 to 2026-08-10 |  |
| 3 | `[FAIL] podman machine start [It] machine init --now with --import-native-ca with mounted d` | 2026-06-09 to 2026-07-28 |  |
| 3 | `not ok \|N\| events - container inspect data - journald` | 2026-07-08 to 2026-07-22 |  |
| 3 | `not ok \|N\| podman commit --pause default` | 2026-06-15 to 2026-07-21 | #24598 needs-check |
| 3 | `[FAIL] run cp commands [It] podman machine cp` | 2026-06-12 to 2026-07-08 | #26547 needs-check |
| 3 | `not ok \|N\| TCP/IPv6 small transfer, loopback` | 2026-06-08 to 2026-07-07 |  |
| 3 | `[FAIL] podman machine set [It] set machine cpus, disk, memory` | 2026-06-19 to 2026-07-06 |  |
| 3 | `not ok \|N\| TCP translated port range forwarding, IPv6, tap` | 2026-06-02 to 2026-07-03 |  |
| 3 | `not ok [N] podman network create` | 2026-06-01 to 2026-06-30 | #17288 needs-check |
| 3 | `not ok \|N\| podman kube play healthcheck should wait initialDelaySeconds before updating st` | 2026-06-02 to 2026-06-29 | #23871 needs-check |
| 3 | `not ok \|N\| quadlet - image files` | 2026-06-26 to 2026-06-29 |  |
| 3 | `not ok \|N\| TCP/IPv4 small transfer, tap` | 2026-06-12 to 2026-06-24 |  |
| 3 | `not ok \|N\| TCP translated port range forwarding, IPv4, loopback` | 2026-06-12 to 2026-06-18 |  |
| 3 | `[FAIL] podman machine start [It] machine start with --update-connection` | 2026-06-02 to 2026-06-15 | #26547 needs-check |
| 3 | `[FAIL] Podman pull [It] podman pull check all tags` | 2026-06-04 |  |
| 2 | `[FAIL] podman machine set [It] set rootful with docker sock change` | 2026-07-20 to 2026-08-12 |  |
| 2 | `[FAIL] podman machine start [It] start simple machine` | 2026-07-08 to 2026-07-27 | #26547 needs-check |
| 2 | `not ok \|N\| podman logs - --since --follow journald` | 2026-06-19 to 2026-07-26 | #23682 needs-check |
| 2 | `[FAIL] podman machine start [It] machine init --now with --update-connection` | 2026-06-24 to 2026-07-20 | #26547 needs-check |
| 2 | `[FAIL] podman machine start [It] start machine already started` | 2026-06-12 to 2026-07-16 | #26547 needs-check |
| 2 | `[FAIL] podman machine start [It] start machine with conflict on SSH port` | 2026-06-24 to 2026-07-13 |  |
| 2 | `[FAIL] podman machine init [It] machine init with rosetta=false` | 2026-06-16 to 2026-07-13 | #26547 needs-check |
| 2 | `[FAIL] podman machine init [It] machine init with volume` | 2026-06-26 to 2026-07-13 | #26547 needs-check |
| 2 | `[FAIL] Podman port [It] podman port multiple ports` | 2026-06-30 to 2026-07-13 | #19048 needs-check |
| 2 | `not ok \|N\| podman images with concurrent removal` | 2026-06-24 to 2026-07-08 | #24800 needs-check |
| 2 | `[FAIL] podman machine init [It] machine init rootful with docker.sock check` | 2026-06-16 to 2026-07-07 | #28873 needs-check |
| 2 | `not ok \|N\| podman network - basic tests` | 2026-06-24 to 2026-07-07 | #17288 needs-check |
| 2 | `[FAIL] podman machine init [It] machine init rootless docker.sock check` | 2026-07-02 to 2026-07-06 | #28873 needs-check |
| 2 | `[FAIL] podman machine start [It] machine init --now with --import-native-ca with SCP file ` | 2026-06-01 to 2026-07-02 |  |
| 2 | `[FAIL] podman machine ssh [It] verify machine rootfulness` | 2026-06-19 to 2026-06-30 |  |
| 2 | `[FAIL] podman machine compose [It] compose test environment variable setup` | 2026-06-12 to 2026-06-29 |  |
| 2 | `not ok \|N\| Interface-bound TCP port forwarding, IPv6, loopback` | 2026-06-23 to 2026-06-29 |  |
| 2 | `not ok \|N\| podman import` | 2026-06-10 to 2026-06-26 | #26547 needs-check |
| 2 | `not ok \|N\| TCP/IPv4 large transfer, tap` | 2026-06-23 to 2026-06-25 |  |
| 2 | `[FAIL] Podman checkpoint [It] podman checkpoint a container started with --rm` | 2026-06-22 to 2026-06-24 |  |
| 2 | `not ok \|N\| TCP translated port range forwarding, IPv6, loopback` | 2026-06-01 to 2026-06-23 |  |
| 2 | `[FAIL] podman machine set [It] no settings should change if no flags` | 2026-06-10 to 2026-06-21 |  |
| 2 | `not ok \|N\| Translated TCP port forwarding, IPv4, tap` | 2026-06-17 to 2026-06-18 |  |
| 2 | `not ok \|N\| TCP port range forwarding, IPv4, tap` | 2026-06-16 |  |
| 2 | `[FAIL] podman machine proxy settings propagation [It] ssh to running machine and check pro` | 2026-06-15 to 2026-08-12 |  |
| 2 | `not ok \|N\| podman play with image volume (automount annotation and OCI VolumeSource)` | 2026-06-02 to 2026-06-12 |  |
| 2 | `[FAIL] Podman port [It] podman port -l nginx` | 2026-06-04 to 2026-06-11 | #19048 needs-check |
| 2 | `not ok \|N\| quadlet - kube build from unavailable image with no tag` | 2026-06-03 to 2026-06-04 |  |
| 1 | `not ok \|N\| podman run --cgroups=disabled keeps the current cgroup` | 2026-08-12 |  |
| 1 | `[FAIL] Podman port [It] podman port nginx by name` | 2026-08-11 | #19048 needs-check |
| 1 | `not ok \|N\| podman mount no-dereference` | 2026-08-09 | #24223 needs-check |
| 1 | `not ok \|N\| podman cp file from container to container` | 2026-08-04 | #10927 needs-check |
| 1 | `[FAIL] podman machine restart [It] should restart a running machine` | 2026-07-29 | #26547 needs-check |
| 1 | `not ok [N] podman system check - container data modified` | 2026-07-27 |  |
| 1 | `[FAIL] Podman healthcheck run [It] podman healthcheck --ignore-result exits 0 on failing h` | 2026-07-22 |  |
| 1 | `[FAIL] run podman API test calls [It] client connect to machine named pipe` | 2026-07-21 |  |
| 1 | `[FAIL] Verify podman containers.conf usage base_hosts_file in containers.conf base_hosts_f` | 2026-07-20 |  |
| 1 | `[FAIL] Podman run networking [It] podman run bridge source IP pasta IPv6 explicit HostIP` | 2026-07-20 |  |
| 1 | `[FAIL] Podman checkpoint [It] podman checkpoint and run exec in restored container` | 2026-07-19 | #10927 needs-check |
| 1 | `[FAIL] podman machine init [It] machine init with swap` | 2026-07-17 | #26547 needs-check |
| 1 | `[FAIL] podman machine init [DeferCleanup (Each)] simple init with start` | 2026-07-13 |  |
| 1 | `[FAIL] podman machine init [DeferCleanup (Each)] machine init rootful with docker.sock che` | 2026-07-13 |  |
| 1 | `[FAIL] run basic podman commands [DeferCleanup (Each)] podman build contexts` | 2026-07-13 |  |
| 1 | `not ok \|N\| podman detects correct tty size` | 2026-07-10 | #10710 needs-check |
| 1 | `[FAIL] podman machine start [DeferCleanup (Each)] start two machines in parallel` | 2026-07-09 |  |
| 1 | `[FAIL] run basic podman commands [It] Volume ops` | 2026-07-08 | #26547 needs-check |
| 1 | `not ok \|N\| podman run -l passthrough-tty` | 2026-07-08 |  |
| 1 | `[FAIL] podman machine stop [It] Stop running machine` | 2026-07-08 | #26547 needs-check |
| 1 | `not ok \|N\| podman rm - running container, w/o and w/ force` | 2026-07-08 |  |
| 1 | `[FAIL] podman machine set [DeferCleanup (Each)] no settings should change if no flags` | 2026-07-07 |  |
| 1 | `[FAIL] Podman run [It] podman test selinux label resolv.conf` | 2026-07-07 |  |
| 1 | `not ok \|N\| Interface-bound TCP port forwarding, IPv4, loopback` | 2026-07-07 |  |
| 1 | `[FAIL] Podman run [It] podman test selinux --privileged label hostname` | 2026-07-07 |  |
| 1 | `not ok \|N\| Address-bound TCP port forwarding, IPv6, tap` | 2026-07-07 |  |
| 1 | `not ok \|N\| TCP port range forwarding, IPv6, tap` | 2026-07-03 |  |
| 1 | `[FAIL] Podman run with volumes [It] podman run --rm with no transient-store` | 2026-07-02 |  |
| 1 | `[FAIL] run podman API test calls [It] curl connect to machine socket` | 2026-07-01 | #22843 needs-check |
| 1 | `not ok \|N\| Single TCP port forwarding, IPv4, loopback` | 2026-06-30 |  |
| 1 | `not ok \|N\| Translated TCP port forwarding, IPv6, loopback` | 2026-06-30 |  |
| 1 | `[FAIL] Podman checkpoint [It] podman checkpoint and restore container with root file-syste` | 2026-06-30 |  |
| 1 | `not ok \|N\| Translated TCP port forwarding, IPv6, tap` | 2026-06-29 |  |
| 1 | `[FAIL] run cp commands [It] podman cp` | 2026-06-29 | #26547 needs-check |
| 1 | `[FAIL] Podman run [It] podman test selinux label /run/secrets` | 2026-06-29 |  |
| 1 | `not ok [N] quadlet verb - install from URL` | 2026-06-27 |  |
| 1 | `not ok \|N\| TCP/IPv6 small transfer, tap` | 2026-06-27 |  |
| 1 | `[FAIL] Podman port [It] podman port -l port nginx` | 2026-06-26 | #19048 needs-check |
| 1 | `[FAIL] Podman run networking [It] podman run with macvlan network` | 2026-06-24 |  |
| 1 | `[FAIL] TOP-LEVEL [AfterEach] Podman kube play test with reserved Seccomp annotation in yam` | 2026-06-24 | #21560 needs-check |
| 1 | `not ok \|N\| Single TCP port forwarding, IPv4, tap` | 2026-06-24 |  |
| 1 | `[FAIL] Podman build [It] podman build with a secret from file` | 2026-06-24 | #20485 needs-check |
| 1 | `[FAIL] Podman create [It] podman container create --tls-verify` | 2026-06-23 |  |
| 1 | `[FAIL] Podman healthcheck run [It] podman healthcheck - health timeout` | 2026-06-23 |  |
| 1 | `[FAIL] podman machine rm [It] Remove running machine` | 2026-06-23 | #22551 needs-check |
| 1 | `not ok \|N\| UDP/IPv6 large transfer, tap` | 2026-06-23 |  |
| 1 | `not ok \|N\| podman healthcheck - stop container when healthcheck runs` | 2026-06-22 |  |
| 1 | `[FAIL] Podman checkpoint [It] podman checkpoint and restore containers with --print-stats` | 2026-06-21 | #24571 needs-check |
| 1 | `[FAIL] Podman checkpoint [It] podman checkpoint and restore container with different port ` | 2026-06-19 | #24571 needs-check |
| 1 | `[FAIL] Podman port [It] podman port -a nginx` | 2026-06-19 | #19048 needs-check |
| 1 | `not ok \|N\| Address-bound TCP port forwarding, IPv4, loopback` | 2026-06-18 |  |
| 1 | `not ok \|N\| Translated UDP port forwarding, IPv6, tap` | 2026-06-18 |  |
| 1 | `[FAIL] podman machine list [It] list machine: check if running while starting` | 2026-06-17 | #28873 |
| 1 | `[FAIL] run podman API test calls [It] client connect to machine socket` | 2026-06-17 | #22843 needs-check |
| 1 | `[FAIL] podman machine ssh [It] ssh to running machine and check os-type` | 2026-06-17 |  |
| 1 | `not ok \|N\| Translated TCP port forwarding, IPv4, loopback` | 2026-06-17 |  |
| 1 | `[FAIL] Podman build [It] podman-remote send correct path to copier` | 2026-06-16 |  |
| 1 | `not ok \|N\| Use options from containers.conf` | 2026-06-15 |  |
| 1 | `[FAIL] Podman build [It] podman build http proxy test` | 2026-06-15 |  |
| 1 | `not ok \|N\| podman logs - --until --follow journald` | 2026-06-15 | #23682 needs-check |
| 1 | `[FAIL] Podman build [It] podman build relay exit code to process` | 2026-06-14 |  |
| 1 | `[FAIL] Podman build [It] podman build --build-context: local source` | 2026-06-13 |  |
| 1 | `not ok \|N\| TCP/IPv6 large transfer, tap` | 2026-06-13 |  |
| 1 | `[FAIL] Podman build [It] podman build --build-context: Image source` | 2026-06-12 |  |
| 1 | `[FAIL] Podman build [It] podman remote test container/docker file is not at root of contex` | 2026-06-12 |  |
| 1 | `[FAIL] Podman build [It] podman build --build-context: Mixed source` | 2026-06-12 |  |
| 1 | `not ok \|N\| podman cp file from container to host` | 2026-06-11 | #10927 needs-check |
| 1 | `not ok [10-images] pullProgress reports sha256:<HASH> as progressComponentID` | 2026-06-11 |  |
| 1 | `[FAIL] Podman checkpoint [It] podman checkpoint container with export (migration)` | 2026-06-10 |  |
| 1 | `[FAIL] Podman network create [It] podman network create --ip-range sip-eip` | 2026-06-10 |  |
| 1 | `[FAIL] Podman attach [It] podman attach to a container with --sig-proxy set to false` | 2026-06-10 |  |
| 1 | `not ok \|N\| quadlet - named volume dependency` | 2026-06-09 |  |
| 1 | `not ok \|N\| podman stop - basic test` | 2026-06-08 |  |
| 1 | `[FAIL] Podman start [It] podman start container --filter` | 2026-06-05 |  |
| 1 | `[FAIL] run basic podman commands [It] Volume should be disabled by command line` | 2026-06-05 |  |
| 1 | `not ok \|N\| podman checkpoint/restore ip and mac handling` | 2026-06-05 | #24571 needs-check |
| 1 | `[FAIL] Podman run dns [It] podman run add search domain` | 2026-06-05 |  |
| 1 | `not ok bud with --layers and single and two line Dockerfiles` | 2026-06-04 |  |
| 1 | `not ok bud --layers with --mount type bind should burst cache if content is changed - sour` | 2026-06-04 |  |
| 1 | `[FAIL] Podman push [It] podman push to local registry with authorization` | 2026-06-04 |  |
| 1 | `not ok bud: build manifest list and --add-compression with containers.conf` | 2026-06-03 |  |
| 1 | `[FAIL] Podman logs [It] tail two lines: k8s-file` | 2026-06-03 | #23615 needs-check |
| 1 | `not ok bud-multiple-platform-failure` | 2026-06-03 |  |
| 1 | `[FAIL] Podman checkpoint [It] podman restore container with tcp-close` | 2026-06-02 | #24571 needs-check |
| 1 | `[FAIL] Podman commit [It] podman commit container with --squash` | 2026-06-01 | #24598 needs-check |
| 1 | `not ok \|N\| TCP translated port range forwarding, IPv4, tap` | 2026-06-01 |  |
| 1 | `not ok \|N\| quadlet kube - start error` | 2026-06-01 | #21560 needs-check |
| 1 | `[FAIL] Podman pod stop [It] podman pod start/stop single pod via --pod-id-file` | 2026-08-13 |  |
| 1 | `not ok \|N\| podman autoupdate local` | 2026-08-13 |  |
| 1 | `[FAIL] Podman run with volumes [It] podman named volume copyup` | 2026-08-13 |  |
| 1 | `not ok \|N\| podman run docker-archive` | 2026-08-12 | #17802 needs-check |

possible families - similar signatures that MAY share one cause. Kept separate above on purpose: similar names can be different failures, so merging is a human call.
- 6 flakes across 2: `not ok \|N\| podman mount - basic test`; `not ok \|N\| podman stop - basic test`
- 7 flakes across 2: `not ok [N] podman network reload`; `not ok [N] podman network create`
- 10 flakes across 3: `not ok \|N\| TCP port range forwarding, IPv4, loopback`; `not ok \|N\| TCP port range forwarding, IPv6, loopback`; `not ok \|N\| TCP port range forwarding, IPv4, tap`
- 7 flakes across 4: `[FAIL] Podman build [It] podman build --build-context: URL s`; `[FAIL] Podman build [It] podman build --build-context: local`; `[FAIL] Podman build [It] podman build --build-context: Image`; `[FAIL] Podman build [It] podman build --build-context: Mixed`
- 9 flakes across 4: `not ok \|N\| TCP translated port range forwarding, IPv6, tap`; `not ok \|N\| TCP translated port range forwarding, IPv4, loopb`; `not ok \|N\| TCP translated port range forwarding, IPv6, loopb`; `not ok \|N\| TCP translated port range forwarding, IPv4, tap`
- 4 flakes across 2: `not ok \|N\| TCP/IPv4 small transfer, tap`; `not ok \|N\| TCP/IPv6 small transfer, tap`
- 5 flakes across 2: `[FAIL] podman machine start [It] machine start with --update`; `[FAIL] podman machine start [It] machine init --now with --u`
- 3 flakes across 2: `not ok \|N\| podman logs - --since --follow journald`; `not ok \|N\| podman logs - --until --follow journald`
- 3 flakes across 2: `[FAIL] podman machine init [It] machine init with volume`; `[FAIL] podman machine init [It] machine init with swap`
- 4 flakes across 2: `[FAIL] podman machine init [It] machine init rootful with do`; `[FAIL] podman machine init [It] machine init rootless docker`
- 3 flakes across 2: `not ok \|N\| Interface-bound TCP port forwarding, IPv6, loopba`; `not ok \|N\| Interface-bound TCP port forwarding, IPv4, loopba`
- 4 flakes across 3: `not ok \|N\| TCP/IPv4 large transfer, tap`; `not ok \|N\| UDP/IPv6 large transfer, tap`; `not ok \|N\| TCP/IPv6 large transfer, tap`
- 6 flakes across 5: `not ok \|N\| Translated TCP port forwarding, IPv4, tap`; `not ok \|N\| Translated TCP port forwarding, IPv6, tap`; `not ok \|N\| Single TCP port forwarding, IPv4, tap`; `not ok \|N\| Translated UDP port forwarding, IPv6, tap` ...
- 3 flakes across 2: `[FAIL] Podman port [It] podman port -l nginx`; `[FAIL] Podman port [It] podman port -a nginx`
- 2 flakes across 2: `not ok \|N\| podman cp file from container to container`; `not ok \|N\| podman cp file from container to host`
- 2 flakes across 2: `[FAIL] run podman API test calls [It] client connect to mach`; `[FAIL] run podman API test calls [It] client connect to mach`
- 2 flakes across 2: `not ok \|N\| Address-bound TCP port forwarding, IPv6, tap`; `not ok \|N\| Address-bound TCP port forwarding, IPv4, loopback`

top signature occurrences:
- https://github.com/podman-container-tools/podman/actions/runs/30463622001/job/91203565547
- https://github.com/podman-container-tools/podman/actions/runs/29951636314/job/89032377003
- https://github.com/podman-container-tools/podman/actions/runs/29844369873/job/88684738266
- https://github.com/podman-container-tools/podman/actions/runs/29842451991/job/88677981054

## designed failures - not real flakes (35 flakes, 3 signatures)

| n | signature | window | issue candidate |
|---|---|---|---|
| 32 | `make: *** [TARGET] Error 1` | 2026-06-02 to 2026-08-13 | #20332 needs-check |
| 2 | `make: *** [TARGET] Error 56` | 2026-06-08 to 2026-07-07 | #20332 needs-check |
| 1 | `make: *** [TARGET] Error 60` | 2026-08-11 | #20332 needs-check |

possible families - similar signatures that MAY share one cause. Kept separate above on purpose: similar names can be different failures, so merging is a human call.
- 35 flakes across 3: `make: *** [TARGET] Error 1`; `make: *** [TARGET] Error 56`; `make: *** [TARGET] Error 60`

top signature occurrences:
- https://github.com/podman-container-tools/podman/actions/runs/31594925821/job/94108049621
- https://github.com/podman-container-tools/podman/actions/runs/30473552461/job/90649483650
- https://github.com/podman-container-tools/podman/actions/runs/30463622001/job/90615769638
- https://github.com/podman-container-tools/podman/actions/runs/30431783562/job/90632301368

## unmatched - open these by hand (118 flakes)

| n | signature | window | issue candidate |
|---|---|---|---|
| 118 | `(none)` | 2026-06-04 to 2026-08-13 |  |

## no retrievable log (126 flakes)

| n | signature | window | issue candidate |
|---|---|---|---|
| 126 | `(none)` | 2026-06-17 to 2026-08-21 |  |
