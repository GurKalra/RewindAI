import time
target = "data/vault/evidence.txt"
print("!!!!SIMULATING NORMAL USER ACTIVITY...")
sentences = ["Updating my project notes.", "Added a new paragraph to the essay.", "Fixing a typo in the conclusion."]
for s in sentences:
    with open(target, "a") as f:
        f.write("\n" + s)
    print(f"  > User saved: {s}")
    time.sleep(1.0)