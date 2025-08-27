import streamlit as st
import hashlib
import random
import time

# -------------------------
# Block Class
# -------------------------
class Block:
    def __init__(self, block_no, data, prev_hash="0"):
        self.block_no = block_no
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = str(self.block_no) + self.data + self.prev_hash
        return hashlib.sha256(content.encode()).hexdigest()[:6]

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(1, "Genesis Block", "0")
        self.chain.append(genesis)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain)+1, data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.prev_hash != prev.hash:
                return False
        return True

# -------------------------
# Init game state
# -------------------------
if "blockchain" not in st.session_state:
    bc = Blockchain()
    bc.add_block("A → B : 5 coins")
    bc.add_block("B → C : 2 coins")
    bc.add_block("C → D : 10 coins")

    # break one random block
    idx = random.randint(1, len(bc.chain)-1)
    bc.chain[idx].data = "💀 Tampered Data!"
    bc.chain[idx].hash = "XXXXX"

    st.session_state.blockchain = bc

bc = st.session_state.blockchain

# -------------------------
# Page title
# -------------------------
st.set_page_config(page_title="Chain Keeper Game", page_icon="🔗", layout="centered")
st.title("🧩 Chain Keeper – Blockchain Puzzle Game")

# 🎶 Background music (judas.mp3)
st.markdown(
    """
    <audio autoplay loop id="bg-audio">
        <source src="https://githubusercontent.com/charrr-star/blockyyyyy/main/judas.mp3" type="audio/mp3">
    </audio>
    """,
    unsafe_allow_html=True
)

# Volume slider
volume = st.slider("🔊 Volume", 0, 100, 50)

# Inject JS to control volume
st.markdown(f"""
<script>
  var audio = document.getElementById("bg-audio");
  if (audio) {{
    audio.volume = {volume}/100;
  }}
</script>
""", unsafe_allow_html=True)

# -------------------------
# CSS animations
# -------------------------
st.markdown("""
<style>
.flip-card {
  background-color: transparent;
  width: 280px;
  height: 160px;
  perspective: 1000px;
  display: inline-block;
  margin: 10px;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}
.flip-card.fixed .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
  padding: 15px;
}
.flip-card-front {
  background-color: #FF7F7F;
  color: white;
}
.flip-card-back {
  background-color: #90EE90;
  color: black;
  transform: rotateY(180deg);
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Display blocks
# -------------------------
valid_blocks = 0
for i, block in enumerate(bc.chain):
    valid = (block.hash == block.calculate_hash()) and (i == 0 or block.prev_hash == bc.chain[i-1].hash)
    if valid:
        valid_blocks += 1

    st.markdown(
        f"""
        <div class="flip-card {'fixed' if valid else ''}">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <h4>🔗 Block {block.block_no}</h4>
              🚨 Tampered!<br>
              Data: {block.data}<br>
              Hash: {block.hash}<br>
              Prev: {block.prev_hash}
            </div>
            <div class="flip-card-back">
              <h4>🔗 Block {block.block_no}</h4>
              ✅ Valid<br>
              Data: {block.data}<br>
              Hash: {block.calculate_hash()}<br>
              Prev: {block.prev_hash}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True
    )

# -------------------------
# Progress bar
# -------------------------
progress = int((valid_blocks / len(bc.chain)) * 100)
st.progress(progress)

# -------------------------
# Controls
# -------------------------
st.write("### 🔧 Repair a Block")
choice = st.number_input("Enter block number to repair:", min_value=1, max_value=len(bc.chain), step=1)

if st.button("✨ Repair"):
    with st.spinner(f"Fixing Block {choice}... 🔨"):
        time.sleep(1.5)
    bc.chain[choice-1].hash = bc.chain[choice-1].calculate_hash()
    if choice > 1:
        bc.chain[choice-1].prev_hash = bc.chain[choice-2].hash
    st.success(f"Block {choice} repaired!")

# -------------------------
# Win animation
# -------------------------
if bc.is_chain_valid():
    st.balloons()
    st.success("🎆 Woohoo! Blockchain integrity restored!")










