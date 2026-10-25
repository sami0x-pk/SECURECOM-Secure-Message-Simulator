# 🛡️ SECURECOM
### Advanced Secure Message Simulator

**SECURECOM** is a Python-based desktop application that demonstrates secure communication using **AES-256-GCM authenticated encryption**.

It features a military-inspired graphical interface designed to help students understand encryption, decryption, message integrity, and cybersecurity concepts.

> 🔐 **ENCRYPT. TRANSMIT. DECRYPT. SECURE.**

---

## 🚀 Key Features

- 🔐 **AES-256-GCM Encryption** — Protects message confidentiality and integrity.
- 🖥️ **Advanced GUI** — Military-inspired dark-themed interface.
- 📊 **Security Dashboard** — Displays session activity and security information.
- 📤 **Message Encryption** — Converts plaintext messages into encrypted packets.
- 📥 **Message Decryption** — Verifies and decrypts authenticated packets.
- 🔑 **Session Key Rotation** — Generates new temporary encryption keys.
- 🛡️ **Tamper Detection** — Detects modified or invalid encrypted messages.
- 📋 **Security Audit Logs** — Records security events.
- 💾 **Packet Management** — Save, load, and copy encrypted packets.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Desktop GUI development |
| Cryptography | AES-256-GCM encryption |
| JSON | Encrypted packet representation |
| CSV | Security audit export |
| Jupyter Notebook | Cryptography demonstration |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sami0x-pk/SECURECOM-Secure-Message-Simulator.git
```

### 2. Open the project directory

```bash
cd SECURECOM-Secure-Message-Simulator
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Windows users can also launch the application using `Run_SECURECOM.bat`.

---

## 🔄 How SECURECOM Works

**Step 1 — Compose Message**

The sender enters a message into the application.

**Step 2 — Encrypt Message**

SECURECOM encrypts the message using AES-256-GCM.

**Step 3 — Simulate Transmission**

The encrypted packet is delivered to the local receiver panel.

**Step 4 — Verify and Decrypt**

The receiver verifies the encrypted packet and decrypts the message using the active session key.

**Step 5 — Security Audit**

The application records relevant security events for monitoring and analysis.

---

## 🔒 Security Concepts Demonstrated

- Confidentiality
- Data Integrity
- Authenticated Encryption
- Cryptographic Nonces
- Session Key Management
- Message Authentication
- Tamper Detection

---

## ⚠️ Project Limitations

SECURECOM is an **educational cybersecurity simulator**.

- It does not transmit messages over a real network.
- It does not implement real military communication protocols.
- Session keys are temporary and stored in application memory.
- Previously saved packets cannot be decrypted after the original session key is lost.

The project is intended for learning and demonstration purposes only.

---

## 👨‍💻 Developer

**Abdul Samad**

🎓 **Aror University of Art, Architecture, Design & Heritage, Sukkur**

💻 **Field:** Cybersecurity & Information Technology

🔗 **GitHub:** [sami0x-pk](https://github.com/sami0x-pk)

---

## 🎯 Future Improvements

- Secure network-based communication
- User authentication
- Multi-user messaging
- Encrypted message history
- Additional security monitoring features
- Improved desktop interface

---

## 📜 Disclaimer

This application is developed for educational purposes and cybersecurity awareness. It is not intended for operational military communication.

---

### ⭐ SECURECOM — Secure Communication Through Cryptography

**Developed by Abdul Samad | Aror University, Sukkur**
