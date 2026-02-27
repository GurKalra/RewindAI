# RewindAI: Autonomous Zero-Loss Ransomware Defense
*An AI-powered ransomware detection and recovery tool.*

<img width="1831" height="787" alt="Screenshot_20260227_210606" src="https://github.com/user-attachments/assets/9e6e95df-94eb-45f4-b1cd-07aac5b4fd04" />

* **"Don't just detect the breach. Rewind the damage."**

## The Issue: Why Are We Solving This?
Ransomware operates at machine speed, often encrypting thousands of files in seconds. Traditional antivirus and Endpoint Detection and Response (EDR) systems rely on known malware signatures and focus purely on *blocking* the execution. 

The critical flaw? **By the time traditional EDR detects a zero-day behavioral anomaly, the damage is already done.** The files are encrypted, the process is killed too late, and the user is forced to pay the ransom or lose their data. We are solving the gap between *detection* and *resilience*.

## The Solution: What Are We Solving?
RewindAI bridges the gap by shifting the paradigm from purely "preventative" to "autonomous self-healing." 

We built a system that assumes a breach will happen and focuses on **Zero-Loss Data Recovery**. If a malicious process bypasses traditional defenses and begins rapid encryption, RewindAI detects the behavioral anomaly in real-time, instantly suspends the attack, and autonomously rewinds the corrupted files to their exact pre-attack state using a secure micro-journal.

![Streamlit Dashboard Live Demo]()

## How Are We Solving It? (System Architecture)
RewindAI operates on a 4-layer autonomous defense architecture:

1. **Layer 1: Real-Time Telemetry (The Eyes)**
   - Monitors the file system (`data/vault/`) for instantaneous I/O operations.
   - Calculates dynamic file metrics: Shannon Entropy, Modification Frequency, and Historical State Deltas.
2. **Layer 2: AI Threat Intelligence (The Brain)**
   - A Random Forest Machine Learning model continuously analyzes the telemetry data.
   - It distinguishes between normal human file edits and aggressive, automated encryption bursts.
3. **Layer 3: Instant Containment & Recovery (The Shield)**
   - If the AI Threat Score breaches 70%, the system triggers the Shield Protocol.
   - The malicious process is instantly contained using `psutil`.
   - The corrupted files are silently overwritten with their clean counterparts from an isolated `shadow_root`.
4. **Layer 4: Continuous Adaptive Learning (The Loop)**
   - Post-recovery, the system dynamically recalibrates the file's baseline entropy and ingests the attack signature into its continuous learning dataset to prevent recurring attacks.

## Hardware Acceleration (AMD Ryzen™ AI)
To provide enterprise-grade protection without slowing down the user's operating system, RewindAI leverages the **AMD Ryzen™ AI NPU**. 
* **Zero CPU Bottleneck:** The computationally heavy tasks—calculating Shannon entropy and running continuous Random Forest ML inferences—are offloaded entirely to the NPU.
* **Millisecond Response Time:** The hardware acceleration allows the system to evaluate file behaviors and predict zero-day threats in under 100 milliseconds, ensuring the attack is caught before significant damage occurs.


## 📂 Project Structure
```text
RewindAI/
├── data/                   
│   ├── vault/              # Live user directory being monitored
│   ├── shadow_root/        # Secure micro-journal for instant recovery
│   └── status.txt          # Live state log for the UI
├── src/
│   └── rewind/
│       ├── monitor.py      # Watchdog Event Monitor & Feature Extractor
│       ├── brain.py        # ML Classifier Engine
│       ├── shield.py       # Containment and Recovery Logic
│       └── app.py          # Streamlit UI Dashboard
├── scripts/
│   └── generate_dataset.py # Synthetic ransomware behavior generator
├── tests/
│   └── mock_attacks/       # Scripts to simulate Stealth, Burst, and Safe edits
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```
## Tech Stack
* **Language:** Python 3.12
* **Machine Learning:** Scikit-Learn, NumPy, Pandas
* **System APIs:** Watchdog (File I/O), Psutil (Process Containment)
* **Frontend:** Streamlit, Plotly Graph Objects

## Getting Started (Local Setup)
1. Prerequisites
   Ensure you have Python 3.12+ installed.
   ```bash
   git clone https://github.com/GurKalra/RewindAI.git
   cd RewindAI
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize the Defense Engine
   ```bash
   python src/rewind/monitor.py
   ```
3. Launch the Dashboard
   ```bash
   streamlit run src/rewind/app.py
   ```
4. Run Mock Attacks
   To test the Ai, open third terminal and run the provided simulation scripts:
   * Safe Edit: ```text python tests/mock_attacks/user_edit.py ```
   * Burst Edit: ```text python tests/mock_attacks/burst.py ```
   * Stealth Edit: ```text python tests/mock_attacks/stealth.py ```
   Watch the dashboard instantly detect the anomaly, restore the file, and recalibrate!

_Developed for the AMD Slingshot Hackathon 2026._
