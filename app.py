"""
SECURECOM Advanced
Secure Military-Style Message Simulator
Educational local-only desktop prototype.
"""
import base64
import csv
import json
import secrets
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

APP_NAME = "SECURECOM"
AUTHOR = "Abdul Samad"
UNIVERSITY = "Aror University of Art, Architecture, Design & Heritage, Sukkur"

BG = "#07110D"
PANEL = "#101F18"
PANEL2 = "#172B21"
GREEN = "#8BFFB0"
GREEN_DARK = "#1F6A43"
TEXT = "#E5F5EA"
MUTED = "#A4B9AA"
AMBER = "#FFC66D"
RED = "#FF7D86"
CYAN = "#78E8E2"


def encrypt_message(message: str, key: bytes, sender: str, receiver: str) -> str:
    """Encrypt text with AES-256-GCM; sender/receiver metadata is authenticated."""
    if not message.strip():
        raise ValueError("Please enter a message before encrypting.")
    if len(key) != 32:
        raise ValueError("The session key is invalid.")
    sender = sender.strip().upper() or "ALPHA"
    receiver = receiver.strip().upper() or "BRAVO"
    nonce = secrets.token_bytes(12)
    aad = f"SECURECOM|1|{sender}|{receiver}".encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, message.encode("utf-8"), aad)
    envelope = {
        "app": APP_NAME,
        "version": 1,
        "algorithm": "AES-256-GCM",
        "sender": sender,
        "receiver": receiver,
        "created_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
    }
    return json.dumps(envelope, indent=2)


def decrypt_message(packet: str, key: bytes) -> tuple[str, dict]:
    """Authenticate and decrypt an SECURECOM JSON envelope."""
    try:
        envelope = json.loads(packet)
        if envelope.get("app") != APP_NAME or envelope.get("version") != 1:
            raise ValueError("This is not a supported SECURECOM packet.")
        sender = str(envelope["sender"])
        receiver = str(envelope["receiver"])
        nonce = base64.b64decode(envelope["nonce_b64"], validate=True)
        ciphertext = base64.b64decode(envelope["ciphertext_b64"], validate=True)
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("Packet format is invalid or incomplete.") from exc
    if len(nonce) != 12:
        raise ValueError("Packet nonce has an invalid length.")
    aad = f"SECURECOM|1|{sender}|{receiver}".encode("utf-8")
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad).decode("utf-8")
    return plaintext, envelope


class SecureComApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SECURECOM | Advanced Secure Message Simulator")
        self.root.geometry("1380x900")
        self.root.minsize(1080, 740)
        self.root.configure(bg=BG)
        self.key = AESGCM.generate_key(bit_length=256)
        self.events = []
        self.last_packet = ""
        self._style()
        self._build_ui()
        self._update_key_status()
        self.log("SYSTEM INITIALIZED | Temporary AES-256-GCM session key created.")
        self.log("SIMULATION MODE | Messages are processed locally; no network transmission.")

    def _style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL2, foreground=TEXT,
                        padding=(18, 9), font=("Consolas", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", GREEN_DARK)],
                  foreground=[("selected", "#FFFFFF")])
        style.configure("Treeview", background=PANEL, foreground=TEXT,
                        fieldbackground=PANEL, rowheight=26, borderwidth=0,
                        font=("Consolas", 9))
        style.configure("Treeview.Heading", background=PANEL2, foreground=GREEN,
                        font=("Consolas", 9, "bold"))
        style.map("Treeview", background=[("selected", GREEN_DARK)])

    def _label(self, parent, text, size=10, color=TEXT, bold=False, bg=None):
        return tk.Label(parent, text=text, bg=bg or parent["bg"], fg=color,
                        font=("Consolas", size, "bold" if bold else "normal"),
                        anchor="w", justify="left")

    def _button(self, parent, text, command, color=GREEN, fg=BG):
        return tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground="#B7FFCA", activeforeground=BG,
                         relief="flat", padx=13, pady=9,
                         font=("Consolas", 9, "bold"), cursor="hand2",
                         borderwidth=0)

    def _card(self, parent, padx=14, pady=12):
        return tk.Frame(parent, bg=PANEL, padx=padx, pady=pady,
                        highlightbackground="#254332", highlightthickness=1)

    def _build_ui(self):
        # Premium dashboard header
        header = tk.Frame(self.root, bg=BG, padx=26, pady=16)
        header.pack(fill="x")
        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left", fill="x", expand=True)
        self._label(brand, "◈  SECURECOM", 27, GREEN, True).pack(anchor="w")
        self._label(brand, "SECURE MESSAGE OPERATIONS  /  ENCRYPTION LAB", 10, MUTED, True).pack(anchor="w", pady=(4, 0))
        right_head = tk.Frame(header, bg=BG)
        right_head.pack(side="right", anchor="e")
        self._label(right_head, "LOCAL SIMULATION", 9, AMBER, True).pack(anchor="e")
        self.clock_label = self._label(right_head, "--:--:--", 17, CYAN, True)
        self.clock_label.pack(anchor="e", pady=(4, 0))

        # System strip
        statusbar = tk.Frame(self.root, bg=PANEL2, padx=18, pady=10,
                             highlightbackground="#254332", highlightthickness=1)
        statusbar.pack(fill="x", padx=26, pady=(0, 13))
        self.status_label = self._label(statusbar, "● SYSTEM ONLINE", 10, GREEN, True, PANEL2)
        self.status_label.pack(side="left")
        self.key_label = self._label(statusbar, "KEY: ACTIVE", 9, CYAN, True, PANEL2)
        self.key_label.pack(side="left", padx=(24, 0))
        self._label(statusbar, "AES-256-GCM  •  AUTHENTICATED ENCRYPTION", 9, MUTED, True, PANEL2).pack(side="right")

        # Live metrics cards
        metrics = tk.Frame(self.root, bg=BG, padx=26)
        metrics.pack(fill="x", pady=(0, 13))
        self.metric_encrypted = tk.StringVar(value="0")
        self.metric_verified = tk.StringVar(value="0")
        self.metric_alerts = tk.StringVar(value="0")
        self.metric_events = tk.StringVar(value="0")
        self._metric_card(metrics, "PACKETS ENCRYPTED", self.metric_encrypted, GREEN, 0)
        self._metric_card(metrics, "MESSAGES VERIFIED", self.metric_verified, CYAN, 1)
        self._metric_card(metrics, "SECURITY ALERTS", self.metric_alerts, RED, 2)
        self._metric_card(metrics, "AUDIT EVENTS", self.metric_events, AMBER, 3)
        for col in range(4):
            metrics.grid_columnconfigure(col, weight=1, uniform="metric")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=26, pady=(0, 10))
        self.command_tab = tk.Frame(self.tabs, bg=BG)
        self.audit_tab = tk.Frame(self.tabs, bg=BG)
        self.about_tab = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(self.command_tab, text="  COMMAND CENTER  ")
        self.tabs.add(self.audit_tab, text="  SECURITY AUDIT  ")
        self.tabs.add(self.about_tab, text="  PROJECT DETAILS  ")
        self._build_command_center()
        self._build_audit()
        self._build_about()

        footer = tk.Frame(self.root, bg=BG, padx=26, pady=8)
        footer.pack(fill="x")
        self._label(footer, f"DEVELOPED BY {AUTHOR.upper()}  |  {UNIVERSITY.upper()}", 8, MUTED).pack(side="left")
        self._label(footer, "EDUCATIONAL PROTOTYPE • NOT FOR REAL MILITARY USE", 8, AMBER, True).pack(side="right")
        self._tick_clock()

    def _metric_card(self, parent, title, variable, accent, column):
        card = tk.Frame(parent, bg=PANEL, padx=16, pady=10,
                        highlightbackground="#254332", highlightthickness=1)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 7, 0 if column == 3 else 7))
        self._label(card, title, 8, MUTED, True, PANEL).pack(anchor="w")
        tk.Label(card, textvariable=variable, bg=PANEL, fg=accent,
                 font=("Consolas", 22, "bold"), anchor="w").pack(anchor="w", pady=(4, 0))

    def _tick_clock(self):
        if hasattr(self, "clock_label"):
            self.clock_label.config(text=datetime.now().strftime("%H:%M:%S  |  %d %b %Y"))
            self.root.after(1000, self._tick_clock)

    def _build_command_center(self):
        top = tk.Frame(self.command_tab, bg=BG)
        top.pack(fill="x", pady=(12, 10))
        card = self._card(top, 14, 10)
        card.pack(fill="x")
        self._label(card, "MISSION CONFIGURATION", 10, GREEN, True).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 9))
        self._label(card, "SENDER TERMINAL", 9, MUTED, True).grid(row=1, column=0, sticky="w")
        self.sender_var = tk.StringVar(value="ALPHA")
        self.sender_box = ttk.Combobox(card, textvariable=self.sender_var, values=["ALPHA", "CHARLIE", "DELTA", "ECHO"], width=15, state="readonly")
        self.sender_box.grid(row=2, column=0, padx=(0, 16), sticky="w")
        self._label(card, "RECEIVER TERMINAL", 9, MUTED, True).grid(row=1, column=1, sticky="w")
        self.receiver_var = tk.StringVar(value="BRAVO")
        self.receiver_box = ttk.Combobox(card, textvariable=self.receiver_var, values=["BRAVO", "ALPHA", "CHARLIE", "DELTA", "ECHO"], width=15, state="readonly")
        self.receiver_box.grid(row=2, column=1, padx=(0, 16), sticky="w")
        self._label(card, "SESSION KEY FINGERPRINT", 9, MUTED, True).grid(row=1, column=2, sticky="w")
        self.fingerprint_var = tk.StringVar()
        self.fingerprint_entry = tk.Entry(card, textvariable=self.fingerprint_var, state="readonly", readonlybackground=BG, fg=CYAN, relief="flat", width=28, font=("Consolas", 10))
        self.fingerprint_entry.grid(row=2, column=2, padx=(0, 16), sticky="w")
        self._button(card, "ROTATE SESSION KEY", self.new_key, color=AMBER).grid(row=2, column=3, sticky="e")
        card.grid_columnconfigure(4, weight=1)

        body = tk.Frame(self.command_tab, bg=BG)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        left = self._card(body)
        right = self._card(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        right.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        self._label(left, "01  /  ALPHA — COMPOSE", 12, GREEN, True).pack(anchor="w")
        self._label(left, "Message body (kept local in this demo)", 9, MUTED).pack(anchor="w", pady=(5, 7))
        self.message = scrolledtext.ScrolledText(left, height=7, bg=BG, fg=TEXT, insertbackground=GREEN, wrap="word", font=("Consolas", 10), relief="flat", padx=9, pady=8)
        self.message.pack(fill="both", expand=True)
        self.message.insert("1.0", "SECURECOM communication test.")
        actions = tk.Frame(left, bg=PANEL)
        actions.pack(fill="x", pady=(10, 9))
        self._button(actions, "ENCRYPT & TRANSMIT  →", self.send).pack(side="left")
        self._button(actions, "CLEAR", self.clear_message, color=PANEL2, fg=TEXT).pack(side="left", padx=(8, 0))
        self._label(left, "ENCRYPTED PACKET  /  JSON ENVELOPE", 9, GREEN, True).pack(anchor="w")
        self.packet = scrolledtext.ScrolledText(left, height=10, bg=BG, fg=CYAN, insertbackground=GREEN, wrap="word", font=("Consolas", 9), relief="flat", padx=9, pady=8)
        self.packet.pack(fill="both", expand=True, pady=(6, 8))
        packet_actions = tk.Frame(left, bg=PANEL)
        packet_actions.pack(fill="x")
        self._button(packet_actions, "SAVE PACKET", self.save_packet, color=PANEL2, fg=TEXT).pack(side="left")
        self._button(packet_actions, "COPY PACKET", self.copy_packet, color=PANEL2, fg=TEXT).pack(side="left", padx=(8, 0))

        self._label(right, "02  /  BRAVO — RECEIVE & VERIFY", 12, CYAN, True).pack(anchor="w")
        self._label(right, "Paste or load a packet to simulate reception", 9, MUTED).pack(anchor="w", pady=(5, 7))
        self.received = scrolledtext.ScrolledText(right, height=12, bg=BG, fg=CYAN, insertbackground=GREEN, wrap="word", font=("Consolas", 9), relief="flat", padx=9, pady=8)
        self.received.pack(fill="both", expand=True)
        receive_actions = tk.Frame(right, bg=PANEL)
        receive_actions.pack(fill="x", pady=(10, 9))
        self._button(receive_actions, "LOAD PACKET", self.load_packet, color=PANEL2, fg=TEXT).pack(side="left")
        self._button(receive_actions, "VERIFY & DECRYPT", self.receive).pack(side="left", padx=(8, 0))
        self._label(right, "AUTHENTICATED PLAINTEXT", 9, GREEN, True).pack(anchor="w")
        self.plaintext = scrolledtext.ScrolledText(right, height=6, bg=BG, fg=TEXT, insertbackground=GREEN, wrap="word", font=("Consolas", 10), relief="flat", padx=9, pady=8)
        self.plaintext.pack(fill="both", expand=True, pady=(6, 0))

    def _build_audit(self):
        frame = self._card(self.audit_tab, 18, 16)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        top = tk.Frame(frame, bg=PANEL)
        top.pack(fill="x")
        self._label(top, "SECURITY EVENT MONITOR", 14, GREEN, True, PANEL).pack(side="left")
        self._label(top, "LIVE SESSION LOG", 9, MUTED, True, PANEL).pack(side="right")
        self._label(frame, "Filter events by keyword or status. Events remain local until exported.", 9, MUTED).pack(anchor="w", pady=(6, 10))
        tools = tk.Frame(frame, bg=PANEL)
        tools.pack(fill="x", pady=(0, 10))
        self.audit_filter = tk.StringVar()
        filter_entry = tk.Entry(tools, textvariable=self.audit_filter, bg=BG, fg=TEXT,
                                insertbackground=GREEN, relief="flat", font=("Consolas", 10))
        filter_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        filter_entry.insert(0, "")
        self._button(tools, "FILTER", self.refresh_audit, color=GREEN).pack(side="left", padx=(0, 8))
        self._button(tools, "RESET", self.reset_audit_filter, color=PANEL2, fg=TEXT).pack(side="left")
        columns = ("time", "event", "status")
        self.audit_tree = ttk.Treeview(frame, columns=columns, show="headings", height=17)
        self.audit_tree.heading("time", text="TIMESTAMP")
        self.audit_tree.heading("event", text="EVENT DESCRIPTION")
        self.audit_tree.heading("status", text="RESULT")
        self.audit_tree.column("time", width=175, anchor="center", stretch=False)
        self.audit_tree.column("event", width=760, stretch=True)
        self.audit_tree.column("status", width=125, anchor="center", stretch=False)
        self.audit_tree.tag_configure("ALERT", foreground=RED)
        self.audit_tree.tag_configure("SUCCESS", foreground=GREEN)
        self.audit_tree.tag_configure("INFO", foreground=CYAN)
        self.audit_tree.pack(fill="both", expand=True)
        buttons = tk.Frame(frame, bg=PANEL)
        buttons.pack(fill="x", pady=(12, 0))
        self._button(buttons, "EXPORT AUDIT CSV", self.export_audit).pack(side="left")
        self._button(buttons, "CLEAR AUDIT", self.clear_audit, color=PANEL2, fg=TEXT).pack(side="left", padx=(8, 0))

    def refresh_audit(self):
        if not hasattr(self, "audit_tree"):
            return
        term = self.audit_filter.get().strip().lower()
        for item in self.audit_tree.get_children():
            self.audit_tree.delete(item)
        for event in self.events:
            row_text = f"{event['time']} {event['event']} {event['status']}".lower()
            if not term or term in row_text:
                self.audit_tree.insert("", "end", values=(event["time"], event["event"], event["status"]), tags=(event["status"],))

    def reset_audit_filter(self):
        self.audit_filter.set("")
        self.refresh_audit()

    def _build_about(self):
        frame = self._card(self.about_tab, 24, 22)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        self._label(frame, "SECURECOM", 25, GREEN, True).pack(anchor="w")
        self._label(frame, "Secure Military-Style Message Simulator", 14, TEXT, True).pack(anchor="w", pady=(5, 14))
        self._label(frame, f"Developer: {AUTHOR}", 12, CYAN, True).pack(anchor="w", pady=3)
        self._label(frame, f"University: {UNIVERSITY}", 11, TEXT).pack(anchor="w", pady=3)
        self._label(frame, "CORE SECURITY FEATURES", 11, GREEN, True).pack(anchor="w", pady=(20, 8))
        bullets = [
            "AES-256-GCM authenticated encryption for message confidentiality and integrity",
            "Authenticated sender/receiver metadata using Additional Authenticated Data (AAD)",
            "Random 96-bit nonce per encrypted message",
            "Temporary session key rotation with a visible fingerprint (key itself is never displayed)",
            "Packet save/load, clipboard copy, and CSV activity-audit export",
            "Tamper detection: altered ciphertext or authenticated metadata should fail verification",
        ]
        for bullet in bullets:
            self._label(frame, "• " + bullet, 10, TEXT).pack(anchor="w", pady=3)
        self._label(frame, "LIMITATIONS", 11, AMBER, True).pack(anchor="w", pady=(20, 8))
        self._label(frame, "This is a local educational simulator. It does not transmit over a network, manage real identities, or provide operational military-grade communications.", 10, MUTED).pack(anchor="w")
        self._label(frame, "Tagline: ENCRYPT. TRANSMIT. DECRYPT. SECURE.", 10, GREEN, True).pack(anchor="w", pady=(22, 0))

    def _fingerprint(self):
        import hashlib
        return hashlib.sha256(self.key).hexdigest()[:16].upper()

    def _update_key_status(self):
        self.fingerprint_var.set(self._fingerprint())
        self.key_label.config(text=f"KEY: ACTIVE • {self._fingerprint()[:8]}")

    def log(self, event, status="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.events.append({"time": timestamp, "event": event, "status": status})
        if "Packet encrypted" in event:
            self.metric_encrypted.set(str(int(self.metric_encrypted.get()) + 1))
        if "Authentication successful" in event:
            self.metric_verified.set(str(int(self.metric_verified.get()) + 1))
        if status == "ALERT":
            self.metric_alerts.set(str(int(self.metric_alerts.get()) + 1))
        if hasattr(self, "metric_events"):
            self.metric_events.set(str(len(self.events)))
        if hasattr(self, "audit_tree"):
            self.refresh_audit()
        if hasattr(self, "status_label"):
            color = RED if status == "ALERT" else GREEN
            self.status_label.config(text=f"● SYSTEM ONLINE  |  LAST EVENT: {status}", fg=color)

    def new_key(self):
        if not messagebox.askyesno("Rotate session key", "Generate a new temporary key? Packets encrypted with the old key will no longer decrypt in this session."):
            return
        self.key = AESGCM.generate_key(bit_length=256)
        self._update_key_status()
        self.packet.delete("1.0", "end")
        self.received.delete("1.0", "end")
        self.plaintext.delete("1.0", "end")
        self.log("SESSION KEY ROTATED | Previous packets require the old key.", "INFO")
        messagebox.showinfo("Session key rotated", "A fresh temporary AES-256-GCM key was created.")

    def send(self):
        sender = self.sender_var.get()
        receiver = self.receiver_var.get()
        if sender == receiver:
            messagebox.showwarning("Terminal selection", "Choose different sender and receiver terminals.")
            return
        try:
            envelope = encrypt_message(self.message.get("1.0", "end").strip(), self.key, sender, receiver)
        except ValueError as exc:
            messagebox.showwarning("Cannot encrypt", str(exc))
            return
        self.last_packet = envelope
        self.packet.delete("1.0", "end")
        self.packet.insert("1.0", envelope)
        self.received.delete("1.0", "end")
        self.received.insert("1.0", envelope)
        self.plaintext.delete("1.0", "end")
        self.log(f"{sender} → {receiver} | Packet encrypted and delivered to local receiver panel.", "SUCCESS")

    def receive(self):
        packet = self.received.get("1.0", "end").strip()
        if not packet:
            messagebox.showwarning("No packet", "Paste or load a packet, or encrypt a message first.")
            return
        try:
            plaintext, envelope = decrypt_message(packet, self.key)
        except (InvalidTag, ValueError, UnicodeDecodeError, TypeError) as exc:
            self.plaintext.delete("1.0", "end")
            self.log("PACKET AUTHENTICATION FAILED | Packet invalid, altered, or wrong session key.", "ALERT")
            messagebox.showerror("Verification failed", "The packet could not be authenticated/decrypted. It may be altered, malformed, or encrypted with a different session key.")
            return
        self.plaintext.delete("1.0", "end")
        self.plaintext.insert("1.0", plaintext)
        self.log(f"{envelope['receiver']} | Authentication successful; message decrypted.", "SUCCESS")

    def save_packet(self):
        packet = self.packet.get("1.0", "end").strip()
        if not packet:
            messagebox.showwarning("No packet", "Encrypt a message first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON packet", "*.json"), ("Text files", "*.txt")], title="Save encrypted packet")
        if path:
            Path(path).write_text(packet, encoding="utf-8")
            self.log(f"Encrypted packet saved to {Path(path).name}.", "INFO")
            messagebox.showinfo("Packet saved", "Encrypted packet saved. Keep session keys separate from packets.")

    def load_packet(self):
        path = filedialog.askopenfilename(filetypes=[("JSON packet", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")], title="Load encrypted packet")
        if not path:
            return
        try:
            packet = Path(path).read_text(encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Load failed", str(exc))
            return
        self.received.delete("1.0", "end")
        self.received.insert("1.0", packet)
        self.log(f"Packet loaded from {Path(path).name}; verify before trusting.", "INFO")

    def copy_packet(self):
        packet = self.packet.get("1.0", "end").strip()
        if not packet:
            messagebox.showwarning("No packet", "Encrypt a message first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(packet)
        self.log("Encrypted packet copied to clipboard.", "INFO")
        messagebox.showinfo("Copied", "Encrypted packet copied to clipboard.")

    def clear_message(self):
        self.message.delete("1.0", "end")
        self.log("Composer cleared.", "INFO")

    def export_audit(self):
        if not self.events:
            messagebox.showinfo("No events", "There are no audit events to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV audit", "*.csv")], title="Export security audit")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["time", "event", "status"])
            writer.writeheader()
            writer.writerows(self.events)
        messagebox.showinfo("Audit exported", "Current-session audit exported as CSV.")

    def clear_audit(self):
        if not messagebox.askyesno("Clear audit", "Clear current-session audit events from the window?"):
            return
        self.events.clear()
        self.metric_events.set("0")
        for item in self.audit_tree.get_children():
            self.audit_tree.delete(item)
        self.log("Audit cleared by user.", "INFO")


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureComApp(root)
    root.mainloop()
