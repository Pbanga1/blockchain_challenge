# Pychain Ledger

# Imports

import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from datetime import datetime
import pandas as pd
import hashlib


# Creating a Record Data Class

# 1. Defining a new class named `Record`.
# 2. Adding the `@dataclass` decorator immediately before the `Record` class
# definition.
# 3. Adding an attribute named `sender` of type `str`.
# 4. Adding an attribute named `receiver` of type `str`.
# 5. Adding an attribute named `amount` of type `float`.

@dataclass
class Record:
    sender: str
    receiver: str
    amount: float



# Modifying the Existing Block Data Class to Store Record Data

# 1. In the `Block` class, renaming the `data` attribute to `record`.
# 2. Setting the data type of the `record` attribute to `Record`.
    
@dataclass
class Block:

    # @TODO
    # Rename the `data` attribute to `record`, and set the data type to `Record`
    record: Record

    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adding the cache decorator for Streamlit

@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()


################################################################################

# Adding Relevant User Inputs to the Streamlit Interface

# Coding additional input areas for the user interface of your Streamlit
# application. Creating these input areas to capture the sender, receiver, and
# amount for each transaction that you’ll store in the `Block` record.

# 1. Deleting the `input_data` variable from the Streamlit interface.
# 2. Adding an input area where you can get a value for `sender` from the user.
# 3. Adding an input area where you can get a value for `receiver` from the user.
# 4. Adding an input area where you can get a value for `amount` from the user.
# 5. As part of the Add Block button functionality, updating `new_block` so that `Block` consists of an attribute named `record`, which is set equal to a `Record` that contains the `sender`, `receiver`, and `amount` values. The updated `Block`should also include the attributes for `creator_id` and `prev_hash`.

# Adding an input area where you can get a value for `sender` from the user.

input_sender = st.text_input("Sender")


# Adding an input area where you can get a value for `receiver` from the user.

input_receiver = st.text_input("Receiver")


# Adding an input area where you can get a value for `amount` from the user.

input_amount = st.number_input("Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # @TODO
    # Updating `new_block` so that `Block` consists of an attribute named `record`
    # which is set equal to a `Record` that contains the `sender`, `receiver`,
    # and `amount` values
    new_block = Block(
        record = Record,
        creator_id = 42,
        prev_hash = prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()


################################################################################

# Rest of Streamlit Code

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())


################################################################################

# Testing the PyChain Ledger by Storing Records

# Using the terminal, running the Streamlit application by
# `streamlit run pychain.py`.

