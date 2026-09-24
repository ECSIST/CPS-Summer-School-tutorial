# CPS tutorial: Concrete in GitHub Codespaces

A Python 3.12 / Linux x86_64 environment for `cps-tutorial-2.ipynb`, including the supplied ONNX model and test data.

## Start as a student

1. Extract the ZIP. Create a GitHub repository and upload **the contents** of `cps-tutorial-codespaces`, including the hidden `.devcontainer` directory. The notebook, requirements, and `.devcontainer` must be at the repository root. A Git client is useful if your file picker hides dotfiles.
2. On GitHub, choose **Code → Codespaces → Create codespace**. The configuration requests at least 4 cores and 16 GB RAM. Availability depends on your account or organization.
3. Wait for the container setup to finish. It installs dependencies, registers a kernel, checks the model/data, and runs a small encrypted calculation. First setup can take several minutes.
4. Open `cps-tutorial-2.ipynb`. In **Select Kernel**, choose **CPS Tutorial (Python 3.12)**. If necessary choose **Python Environments → .venv/bin/python** or reload the window.
5. Run cells in order. Exercise cells are intentionally incomplete for students to fill in.

Codespaces usage is subject to your GitHub account's quota/billing. Stop the codespace when finished. This archive does not create or publish a GitHub repository for you.

## Environment

The container image is `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm` (Python minor version pinned to 3.12; image patch releases may change). Packages are installed in `.venv`.

Core versions: Concrete ML **1.9.0**, Concrete Python **2.10.0**, NumPy **1.26.4**, scikit-learn **1.5.0**, ONNX **1.17.0**, ONNX Runtime **1.18.0**, and CPU-only PyTorch **2.3.1+cpu**. Notebook support uses ipykernel **6.29.5**. `time` is part of Python's standard library.

Concrete ML 1.9.0 explicitly requires Concrete Python 2.10.0. Do not independently upgrade Concrete Python to 2.11.0. The CPU PyTorch wheel satisfies Concrete ML's 2.3.1 dependency without installing CUDA packages. Direct requirements are pinned; this is not a complete transitive lockfile.

References: [Concrete ML 1.9.0](https://pypi.org/project/concrete-ml/1.9.0/), [Concrete Python 2.10.0](https://pypi.org/project/concrete-python/2.10.0/), [development container configuration](https://containers.dev/implementors/json_reference/).

## Files and notebook changes

- `cps-tutorial-2.ipynb`: runnable tutorial with cleared saved outputs and Python 3.12 kernel metadata.
- `pruned_model_35_percent_acc_9629.onnx`, `test_X.npy`, `test_Y.npy`: original assets, unchanged.
- `.devcontainer/devcontainer.json` and `setup.sh`: container and automatic setup.
- `requirements.txt`: compatible pinned direct dependencies.
- `scripts/check_environment.py`: imports, ONNX validation, data checks, and a small encrypted calculation.
- `reference/cps-tutorial-1.ipynb`: extra notebook found in the supplied ZIP, preserved as received. It uses **pi-heaan**, which is not installed or supported by this Concrete environment. Do not run its installation cell as part of tutorial 2.

The original notebook referred to an absent `anomaly_detection` directory, lowercase `test_y.npy`, and a different 50%-pruned model. Those paths now point to the supplied files at the repository root. Reported model results may differ from the original saved outputs because the supplied model is the 35%-pruned variant.

Unpinned pip installation cells were replaced with version checks. The arithmetic example now creates a seeded input set with explicit range endpoints instead of relying on `fhe.inputset`. Teaching exercises and the original encrypted execution settings remain intact.

## Runtime and troubleshooting

The logistic regression cell runs encrypted inference on 20 examples; the anomaly detection cell runs it on 30. Compilation, key generation, and inference can be slow and use substantial memory. For an initial anomaly-model pass, set `run_fhe = 0`; this skips encrypted inference but still compiles the model. To try one encrypted example, change **both** `items = 30` and the random selection's `size=30` to `1`.

Run from the repository root. A missing module usually means the wrong kernel is selected or setup has not finished. In the terminal, rerun setup with:

```bash
bash .devcontainer/setup.sh
```

To rerun the checks only:

```bash
.venv/bin/python -m pip check
.venv/bin/python scripts/check_environment.py
```

If compilation is killed, select a larger Codespaces machine and reopen it. This setup targets Linux x86_64 Codespaces; native Windows is not the target environment.

## Validation scope

During packaging, all executable tutorial cells were parsed, notebook/config JSON was checked, dataset dimensions and numeric values were inspected, asset copies were checked by SHA-256, and the ZIP contents were verified. Published dependency metadata confirms Python 3.12 support and the required Concrete version pair. The datasets have shapes `(6355, 32)` and `(6355,)`; the ONNX header declares 32 float inputs, one float output, and standard opset 14. A cross-platform dependency dry run was stopped during the large PyTorch download and did not complete. A Linux Codespaces runtime was not available during packaging, so full package installation and end-to-end tutorial execution have not been verified. The automatic setup runs the environment smoke test on first creation; it does not execute the full anomaly-detection tutorial.
