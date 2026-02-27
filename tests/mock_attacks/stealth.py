import os, time
target = "data/vault/evidence.txt"
print("SIMULATING STEALTHY ENCRYPTION...")
for i in range(3):
    with open(target, "wb") as f:
        f.write(os.urandom(4096))
    print(f"  > Sleeping to evade detection...")
    time.sleep(2.5) # Low frequency, trying to hide