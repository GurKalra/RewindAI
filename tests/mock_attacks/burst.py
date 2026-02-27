import os, time
target = "data/vault/evidence.txt"
print("!!!!SIMULATING RAPID ENCRYPTION!!!!")
for i in range(15):
    with open(target, "wb") as f:
        f.write(os.urandom(2048)) # High entropy noise
    print(f"  > Packet {i+1} injected.")
    time.sleep(0.05) # High frequency burst