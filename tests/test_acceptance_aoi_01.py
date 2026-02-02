from mapgen.cli import main
from pathlib import Path

def test_acceptance_aoi_01(tmp_path):
    # Run acceptance for aoi_01
    # Use a temporary directory for artifacts to avoid polluting current dir
    artifacts_dir = tmp_path / "artifacts"
    
    exit_code = main(["acceptance", "run", "--aoi", "aoi_01", "--artifacts", str(artifacts_dir)])
    
    assert exit_code == 0
    
    # Check if artifacts are produced
    result_json = artifacts_dir / "aoi_01" / "result.json"
    assert result_json.exists()
    
    import json
    with open(result_json, "r") as f:
        result = json.load(f)
        
    assert result["aoi"] == "aoi_01"
    assert result["score"] >= result["threshold"]
    assert result["pass"] is True
    assert Path(result["artifacts"]["candidate"]).exists()
    assert Path(result["artifacts"]["diff"]).exists()

def test_acceptance_run_all(tmp_path):
    artifacts_dir = tmp_path / "artifacts"
    
    # run-all should process both aoi_01 and any other folders in tests/golden
    exit_code = main(["acceptance", "run-all", "--artifacts", str(artifacts_dir)])
    
    assert exit_code == 0
    
    # Check if aoi_01 result exists
    assert (artifacts_dir / "aoi_01" / "result.json").exists()
