# SECURECOM — Secure Military-Style Message Simulator

**Developer:** Abdul Samad  
**University:** Aror University of Art, Architecture, Design & Heritage, Sukkur  
**Tagline:** *Encrypt. Transmit. Decrypt. Secure.*

SECURECOM is an educational Python desktop application that simulates secure message exchange between fictional terminals. It demonstrates authenticated encryption and message-tampering detection in a local environment.

> **Disclaimer:** This is a local educational prototype, not a real military communication system. It does not transmit messages over a network or provide operational security guarantees.

## Features

- Tkinter desktop GUI with a dark military-inspired theme
- AES-256-GCM authenticated encryption
- Authenticated sender/receiver metadata
- Random nonce per encrypted message
- Temporary session-key rotation and fingerprint display (the key itself is never shown)
- Simulated ALPHA/BRAVO-style terminals
- Save/load encrypted JSON packets and copy packets to clipboard
- Tamper/wrong-key detection during authentication
- Session audit log with CSV export
- Jupyter Notebook cryptography demonstration

## Files

```text
SECURECOM_Advanced/
├── app.py
├── SECURECOM_Cryptography_Demo.ipynb
├── requirements.txt
├── Run_SECURECOM.bat
└── README.md
```

## Requirements

- Windows 10/11 (GUI)
- Python 3.10+ recommended
- Internet access only for installing the dependency

## Run on Windows

1. Extract the ZIP.
2. Open a terminal in the extracted folder.
3. Install dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python app.py
   ```

If `python` is not recognized, use your Python environment's full path, for example:

```cmd
"C:\Users\YOUR-WINDOWS-USER\.conda\envs\YOUR-ENV\python.exe" -m pip install -r requirements.txt
"C:\Users\YOUR-WINDOWS-USER\.conda\envs\YOUR-ENV\python.exe" app.py
```

Or double-click `Run_SECURECOM.bat` after reviewing the Python path in that file.

## Jupyter Notebook

Run:

```bash
jupyter notebook
```

Open `SECURECOM_Cryptography_Demo.ipynb` and run its cells in order.

## Test checklist

1. Enter a sample message and click **ENCRYPT & TRANSMIT**.
2. Check that a JSON packet appears.
3. Click **VERIFY & DECRYPT**; the original text should appear.
4. Change one character in the received packet and verify again; authentication should fail.
5. Rotate the session key and try the previous packet; decryption should fail.
6. Export the session audit to CSV.

## Security notes and limitations

- AES-GCM provides confidentiality and authentication when keys are managed properly.
- The key is temporary and generated in memory at app launch; it is not persisted or exchanged between separate app installations.
- A packet saved on disk cannot be decrypted after restarting the app unless the original key is still available (this prototype intentionally does not export keys).
- This application has no user account system, network transport, key distribution, secure key storage, or live identity verification.
- Audit events are kept in memory until exported or the application closes.
- The app is a teaching aid, not a substitute for reviewed production cryptographic software.

## Technology stack

- Python
- Tkinter / ttk
- `cryptography` (AESGCM)
- Jupyter Notebook
- GitHub

## License

For educational and demonstration use.
