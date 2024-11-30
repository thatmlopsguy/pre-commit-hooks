# Pre-commit git hooks

Git hooks to integrate with pre-commit.

## Hooks available

### `helm-pluto-chart-check`

Prevent deprecated kubernetes APIs on helm charts using [pluto](https://github.com/FairwindsOps/pluto).

The hook uses `helm template` internally and passes its output to the `pluto`

```sh
usage: helm-pluto.py [-h] [--charts CHARTS]

Check Helm charts with Pluto

options:
  -h, --help       show this help message and exit
  --charts CHARTS  Path to the directory containing Helm charts
```

## License

MIT

## Author

[@thatmlopsguy](https://github.com/thatmlopsguy)
