"""Check imports, supplied assets, and a tiny real encrypted computation."""
from pathlib import Path
import sys
from importlib.metadata import version
import numpy as np
import onnx
from concrete import fhe
from concrete.ml.sklearn import LogisticRegression
from concrete.ml.torch.compile import compile_onnx_model

assert sys.version_info[:2] == (3, 12), sys.version
for name, expected in {"concrete-ml":"1.9.0", "concrete-python":"2.10.0"}.items():
    assert version(name) == expected, (name, version(name))
    print(name, version(name))
root = Path(__file__).resolve().parents[1]
x = np.load(root / "test_X.npy", allow_pickle=False)
y = np.load(root / "test_Y.npy", allow_pickle=False)
assert x.shape[0] == y.shape[0] and x.shape[0] >= 30, (x.shape, y.shape)
assert np.isfinite(x).all() and np.isfinite(y).all()
model = onnx.load(root / "pruned_model_35_percent_acc_9629.onnx")
onnx.checker.check_model(model)
print("Dataset shapes:", x.shape, y.shape)
print("ONNX opsets:", [(op.domain, op.version) for op in model.opset_import])
@fhe.compiler({"x": "encrypted"})
def increment(x):
    return x + 1
circuit = increment.compile(range(4))
assert circuit.encrypt_run_decrypt(2) == 3
print("Environment and encrypted smoke test passed.")
