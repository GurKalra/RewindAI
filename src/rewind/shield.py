import shutil
import os
from pathlib import Path

class Shield:
    def __init__(self, vault_path, shadow_path):
        self.vault = Path(vault_path)
        self.shadow = Path(shadow_path)
        self.shadow.mkdir(parents=True, exist_ok=True)

    def create_baseline(self):
        """Creates the initial 'safe' copy of all files."""
        print(f"Shield: Protecting {self.vault}...")
        for file_path in self.vault.glob('*'):
            if file_path.is_file():
                shutil.copy2(file_path, self.shadow / file_path.name)
        print("Baseline Secure. Ready for 'Rewind'.")

    def restore_file(self, filename):
        """Restores a single corrupted file from the shadow vault."""
        source = self.shadow / filename
        target = self.vault / filename
        if source.exists():
            shutil.copy2(source, target)
            print(f"Rewound: {filename} restored to healthy state.")

# Quick Test
if __name__ == "__main__":
    # Update these paths to your actual folders
    S = Shield(vault_path="data/vault", shadow_path="data/shadow_root")
    S.create_baseline()