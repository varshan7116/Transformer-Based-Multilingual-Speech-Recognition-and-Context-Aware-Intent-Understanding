from app.main import safe_path
import pytest

def test_safe_path_accepts_nested_source():
    assert safe_path("src/components/App.jsx") == "src/components/App.jsx"

@pytest.mark.parametrize("path", ["../secret.txt", "/etc/passwd", r"src\\..\\secret", ".env", ".env.production", "node_modules/pkg/a.js"])
def test_safe_path_rejects_unsafe_paths(path):
    with pytest.raises(ValueError):
        safe_path(path)
