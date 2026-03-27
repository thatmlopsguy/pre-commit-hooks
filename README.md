# Pre-commit git hooks

Git hooks to integrate with pre-commit.

## Hooks available

### `helm-pluto-chart-check`

Prevent deprecated kubernetes APIs on helm charts using [pluto](https://github.com/FairwindsOps/pluto).

This pre-commit hook can be added into the `.pre-commit-config.yaml` file like this:

```yaml
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.4
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

```yaml
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.4
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

### `promtool-check-rules`

Validate Prometheus rules files using [promtool](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/).

This pre-commit hook can be added into the `.pre-commit-config.yaml` file like this:

```yaml
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.4
    hooks:
      - id: promtool-check-rules
        files: rules\.yml$
```

```sh
usage: promtool.py [-h] [--type {rules,config}] [--fail-fast] [files ...]

Validate Prometheus rules and configuration with promtool

positional arguments:
  files                 Files to check

options:
  -h, --help            show this help message and exit
  --type {rules,config} Type of check to run: 'rules' or 'config' (default: rules)
  --fail-fast           Exit on first failure
```

### `promtool-check-config`

Validate Prometheus configuration files using [promtool](https://prometheus.io/docs/prometheus/latest/configuration/configuration/).

This pre-commit hook can be added into the `.pre-commit-config.yaml` file like this:

```yaml
  - repo: https://github.com/thatmlopsguy/pre-commit-hooks
    rev: v0.0.4
    hooks:
      - id: promtool-check-config
        files: prometheus\.yml$
```

## License

MIT

## Author

[@thatmlopsguy](https://github.com/thatmlopsguy)
