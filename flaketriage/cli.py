"""usage:
  python3 -m flaketriage scan <owner/repo> <workflow-file> [--limit N] [--created A..B]
  python3 -m flaketriage extract
  python3 -m flaketriage corroborate [--limit N] [--created A..B] [--min-runs N]
                                            second oracle: known flakes in runs nobody re-ran
  python3 -m flaketriage report [--no-issues]
  python3 -m flaketriage weekly
  python3 -m flaketriage propose            draft issue comments, never posts
  python3 -m flaketriage journal <job-id>   fetch the systemd journal artifact
  python3 -m flaketriage diff <job-id>      lines only in the failing attempt
  python3 -m flaketriage analyze [--limit N]  model verdicts (needs a model endpoint)
  python3 -m flaketriage eval               measure the model against hand labels
  python3 -m flaketriage check "<test name>"  is this a known flake? (REVIEWING.md)

scan is incremental - run it daily and it only touches new runs.
"""
import sys

from . import analyze as analyzecmd
from . import artifacts, attemptdiff, check as checkcmd, corroborate as corroboratecmd
from . import evalcmd, extract, ingest, propose, report


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    cmd = args[0]
    if cmd == "scan":
        pos = [a for a in args[1:] if not a.startswith("--")]
        if len(pos) < 2:
            print(__doc__)
            return 1
        limit = created = None
        if "--limit" in args and args.index("--limit") + 1 < len(args):
            limit = int(args[args.index("--limit") + 1])
        if "--created" in args and args.index("--created") + 1 < len(args):
            created = args[args.index("--created") + 1]
        ingest.scan(pos[0], pos[1], limit=limit, created=created)
    elif cmd == "extract":
        extract.extract_all()
    elif cmd == "corroborate":
        limit = created = None
        min_runs = 1
        if "--limit" in args and args.index("--limit") + 1 < len(args):
            limit = int(args[args.index("--limit") + 1])
        if "--created" in args and args.index("--created") + 1 < len(args):
            created = args[args.index("--created") + 1]
        if "--min-runs" in args and args.index("--min-runs") + 1 < len(args):
            min_runs = int(args[args.index("--min-runs") + 1])
        corroboratecmd.corroborate(limit=limit, created=created, min_runs=min_runs)
    elif cmd == "report":
        report.full_report(with_issues="--no-issues" not in args)
    elif cmd == "weekly":
        report.weekly()
    elif cmd == "propose":
        propose.proposals()
    elif cmd == "journal":
        if len(args) < 2:
            print(__doc__)
            return 1
        if artifacts.fetch(args[1]) is None:
            return 1
    elif cmd == "diff":
        if len(args) < 2:
            print(__doc__)
            return 1
        if attemptdiff.render(args[1]) is None:
            return 1
    elif cmd == "analyze":
        limit = None
        if "--limit" in args and args.index("--limit") + 1 < len(args):
            limit = int(args[args.index("--limit") + 1])
        analyzecmd.analyze(limit=limit)
    elif cmd == "check":
        if len(args) < 2:
            print('usage: check "<test name>"')
            return 1
        return checkcmd.check(" ".join(args[1:]))
    elif cmd == "eval":
        evalcmd.run()
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
