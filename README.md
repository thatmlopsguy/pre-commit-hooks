# Pre-commit git hooks

Git hooks to integrate with pre-commit.

## Hooks available

### `helm-pluto-chart-check`

Prevent deprecated kubernetes APIs on helm charts using [pluto](https://github.com/FairwindsOps/pluto).

This pre-commit hook can be added into the `.pre-commit-config.yaml` file like this:

```
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.3
    hooks:
      - id: helm-pluto-chart-check
        args: ["--charts", "tests/example-charts"]
```

The hook uses `helm template` internally and passes its output to the `pluto`

```sh
usage: helm-pluto.py [-h] [--charts CHARTS]

Check Helm charts with Pluto

options:
  -h, --help       show this help message and exit
  --charts CHARTS  Path to the directory containing Helm charts
```

### `kubectl-score-chart-check`

Runs [kube-score](https://kube-score.com/) against a Helm charts directory.

This pre-commit hook can be added into the `.pre-commit-config.yaml` file like this:

```
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.3
    hooks:
      - id: kubectl-score-chart-check
        args: ["--charts", "tests/example-charts"]
```

The hook uses `helm template` internally and passes its output to the `kube-score`

```sh
usage: kube-score.py [-h] [--charts CHARTS]

Check Helm charts with kube-score

options:
  -h, --help       show this help message and exit
  --charts CHARTS  Path to the directory containing Helm charts
```

## License

MIT

## Author

[@thatmlopsguy](https://github.com/thatmlopsguy)
