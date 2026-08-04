import os

def load_sample(sample_name: str, base_dir: str = "data"):
    """
    Loads the training sample and its corresponding reference summary.
    Returns a dictionary with paths and contents.
    """
    train_path = os.path.join(base_dir, "train", f"{sample_name}.txt")
    ref_path = os.path.join(base_dir, "references", f"{sample_name}.txt")
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training sample not found: {train_path}")
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f"Reference sample not found: {ref_path}")
        
    with open(train_path, "r", encoding="utf-8") as f:
        train_content = f.read().strip()
        
    with open(ref_path, "r", encoding="utf-8") as f:
        ref_content = f.read().strip()
        
    return {
        "sample_name": sample_name,
        "train_path": train_path,
        "ref_path": ref_path,
        "train_content": train_content,
        "ref_content": ref_content
    }

if __name__ == "__main__":
    # Test loading the minimal sample we created in Phase 1
    # Resolves the absolute path to the data directory based on this script's location
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    try:
        sample_data = load_sample("sample_1", base_dir=data_dir)
        print(f"Loaded Sample: {sample_data['sample_name']}")
        print(f"Train Path: {sample_data['train_path']}")
        print(f"Ref Path:   {sample_data['ref_path']}")
        print("\n--- Train Content ---")
        print(sample_data["train_content"])
        print("\n--- Reference Content ---")
        print(sample_data["ref_content"])
    except FileNotFoundError as e:
        print(e)
