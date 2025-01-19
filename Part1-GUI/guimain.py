import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import time
from hashlib import sha256
import randomname
import random
from threading import Thread, Event
from oldBlock import Block

# Configuration
PREFIX_ZEROS = 5
MAX_BLOCK_SIZE = 4
block_chain = []

# Generate random transactions
def gen_transactions(max_block_size):
    transaction_list = []
    for _ in range(max_block_size):
        sender = randomname.get_name()
        recipient = randomname.get_name()
        amount = random.randint(0, 10000)
        transaction = [sender, recipient, amount]
        transaction_list.append(transaction)
    return transaction_list

# GUI Application
class BlockchainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blockchain Miner")
        self.geometry("800x600")

        style = Style(theme="darkly")
        style.configure("Treeview", rowheight=25)

        # Mining control
        self.mining_thread = None
        self.stop_event = Event()
        self.paused_event = Event()  # Event to handle pause/resume
        self.paused_event.set()      # Initially set, meaning mining is allowed

        # Mining Frame
        self.mining_frame = ttk.LabelFrame(self, text="Mining", padding=10)
        self.mining_frame.pack(fill="x", padx=10, pady=5)

        self.start_button = ttk.Button(
            self.mining_frame, text="Start Mining", command=self.start_mining
        )
        self.start_button.pack(side="left", padx=5)

        self.pause_button = ttk.Button(
            self.mining_frame, text="Pause Mining", command=self.pause_or_resume, state="disabled"
        )
        self.pause_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(
            self.mining_frame, text="Stop Mining", command=self.stop_mining, state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(self.mining_frame, text="Status: Ready")
        self.status_label.pack(side="left", padx=10)

        # Transactions Frame
        self.transactions_frame = ttk.LabelFrame(self, text="Transactions", padding=10)
        self.transactions_frame.pack(fill="x", padx=10, pady=5)

        self.transactions_table = ttk.Treeview(
            self.transactions_frame,
            columns=("Sender", "Recipient", "Amount"),
            show="headings",
        )
        self.transactions_table.heading("Sender", text="Sender")
        self.transactions_table.heading("Recipient", text="Recipient")
        self.transactions_table.heading("Amount", text="Amount")
        self.transactions_table.pack(fill="x", padx=5, pady=5)

        # Blockchain Frame
        self.blockchain_frame = ttk.LabelFrame(self, text="Blockchain", padding=10)
        self.blockchain_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.blockchain_list = tk.Text(
            self.blockchain_frame, wrap="word", state="disabled", height=15
        )
        self.blockchain_list.pack(fill="both", padx=5, pady=5, expand=True)

    def start_mining(self):
        self.status_label.config(text="Status: Mining...")
        self.start_button.config(state="disabled")   # Disable Start button
        self.pause_button.config(state="normal")    # Enable Pause button
        self.stop_button.config(state="normal")     # Enable Stop button
        self.stop_event.clear()  # Reset stop event

        # Start a new thread for mining
        self.mining_thread = Thread(target=self.mine_blocks, daemon=True)
        self.mining_thread.start()

    def pause_or_resume(self):
        if self.paused_event.is_set():
            # Pause mining
            self.paused_event.clear()  # Block the mining loop
            self.status_label.config(text="Status: Paused")
            self.pause_button.config(text="Resume Mining")
        else:
            # Resume mining
            self.paused_event.set()    # Allow the mining loop to continue
            self.status_label.config(text="Status: Mining...")
            self.pause_button.config(text="Pause Mining")

    def stop_mining(self):
        self.stop_event.set()  # Signal the thread to stop
        self.status_label.config(text="Status: Stopping...")
        self.start_button.config(state="normal")  # Enable Start button
        self.pause_button.config(state="disabled", text="Pause Mining")  # Reset Pause button
        self.stop_button.config(state="disabled")  # Disable Stop button
        self.status_label.config(text="Status: Stopped")

    def mine_blocks(self):
        block_number = len(block_chain)
        previous_hash = block_chain[-1].mine(PREFIX_ZEROS) if block_chain else "0"

        while not self.stop_event.is_set():
            # Pause if the paused_event is not set
            if not self.paused_event.is_set():
                time.sleep(0.1)  # Wait for a short time before checking again
                continue

            # Generate random transactions
            transaction_list = gen_transactions(MAX_BLOCK_SIZE)

            # Create and mine a new block
            new_block = Block(
                previous_hash,
                sha256(repr(transaction_list).encode("utf-8")).hexdigest(),
                PREFIX_ZEROS,
                transaction_list,
            )
            block_hash = new_block.mine()
            new_block.timestamp = time.time()
            block_chain.append(new_block)

            # Update the GUI
            self.after(0, self.update_transactions_table, transaction_list)
            self.after(0, self.update_blockchain_list, block_number, block_hash)

            # Prepare for the next block
            block_number += 1
            previous_hash = block_hash

        self.status_label.config(text="Status: Stopped")  # Update status when loop ends

    def update_transactions_table(self, transaction_list):
        # Clear previous transactions
        for row in self.transactions_table.get_children():
            self.transactions_table.delete(row)

        # Insert new transactions
        for transaction in transaction_list:
            self.transactions_table.insert(
                "", "end", values=(transaction[0], transaction[1], transaction[2])
            )

    def update_blockchain_list(self, block_number, block_hash):
        self.blockchain_list.config(state="normal")
        self.blockchain_list.insert(
            "end",
            f"Block {block_number}:\nHash: {block_hash}\n{'-' * 40}\n",
        )
        self.blockchain_list.config(state="disabled")


if __name__ == "__main__":
    app = BlockchainApp()
    app.mainloop()