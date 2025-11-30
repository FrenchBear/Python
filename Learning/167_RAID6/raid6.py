# raid6.py
# Simulation of RAID 6 storage
#
# 2025-11-30    PV      First version

# I understand how RAID 5 works on n drives, computing a checksum from n-1 drives using for instance XOR function.
# If drive n is unavailable, no problem, disks 0..n-1 still contain data, and if a drive in 0..n-1 is missing, computing
# the XOR of available volumes including the one containing checksum will return the value of the unavailable disk.
# 
# But I don't really understand which function can be used for RAID 6, so that even in the case of 2 volumes not available,
# information can be reconstructed.  Can you explain me, for instance, using 5 drives, if any two are unavailable, I still
# can get the data from the 3 remaining drives?
# 
# Furthermore, can you illustrate RAID 6 calculations with a simple python example, let's say we have 5 drives holding the
# data, and for this exercise, data is simply represented by an array of 64 bytes, so I have three arrays of 64 bytes
# to store.  What will the 5 arrays of 64 bytes stored on disk?  Can you show me that with the data of any 3 disks among 5,
# I can rebuild my three initial 64 bytes arrays?


# To understand RAID 6, you have to move from simple arithmetic (XOR) to Algebra.
# 
# In RAID 5 (XOR), you essentially have one equation with n variables. If you lose one variable, you can solve for it.
# In RAID 6, because you want to survive two simultaneous failures, you need a system of two independent equations.
# 
# The Logic: Two Equations for Two Unknowns
# 
# Imagine you have data chunks D1​,D2​,D3​. You want to create two parity blocks, P and Q.
# 
#     Parity P (The RAID 5 approach): This is the simple sum (XOR).
#     P=D1​⊕D2​⊕D3​
# 
#     Parity Q (The Reed-Solomon approach): If we just made another XOR checksum, it would be identical to P, that doesn't
# 	help. We need a second equation that is mathematically "distinct" from the first. We do this by applying coefficients
# 	(weights) to the data.
#     Q=(A⋅D1​)⊕(B⋅D2​)⊕(C⋅D3​)
# 
# The Algebra of Recovery: If drives 1 and 2 fail (D1​ and D2​ are missing), you are left with two unknowns. Because you have
# two equations (P and Q) and the remaining values (D3​), you can solve the system to find D1​ and D2​.
# 
# The Solution: Galois Field Arithmetic
# 
# You might ask: "If I multiply bytes by coefficients, won't the numbers get huge?"
# 
# If a byte is 255 and we multiply it by 2, we get 510, which doesn't fit in a byte. To solve this, RAID 6 uses Galois
# Field (GF) arithmetic, specifically GF(28):
# - Addition in this field is simply XOR, so is subtraction.
# - Multiplication is a special polynomial operation that wraps around so the result always fits inside 8 bits (0-255).
# - Division is multiplication by the inverse.
	

import os
# import random

# --- PART 1: The Math Engine (Galois Field GF(2^8)) ---
# This ensures that Math on bytes stays within 0-255.
# In a real driver, this is done via lookup tables for speed.

class GF256:
    # The "reduction polynomial" for AES/Rijndael (standard for storage)
    IRREDUCIBLE_POLY = 0x11b

    @staticmethod
    def add(a, b):
        return a ^ b  # Addition is just XOR

    @staticmethod
    def mul(a, b):
        # "Russian Peasant" multiplication algorithm for GF(2^8)
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            high_bit_set = a & 0x80
            a <<= 1
            if high_bit_set:
                a ^= GF256.IRREDUCIBLE_POLY
            b >>= 1
        return p & 0xFF

    @staticmethod
    def div(a, b):
        # Division is multiplication by inverse.
        # For this demo, we brute-force find the inverse to keep code simple.
        if b == 0:
            raise ZeroDivisionError()
        for candidate in range(256):
            if GF256.mul(b, candidate) == 1:
                return GF256.mul(a, candidate)
        return 0

# --- PART 2: The RAID 6 Implementation ---

def calculate_parity(d1, d2, d3):
    """
    Returns two arrays: P (XOR) and Q (Weighted).
    Equation P: D1 + D2 + D3
    Equation Q: 1*D1 + 2*D2 + 3*D3  (Weights are arbitrary but must be unique)
    """
    p_drive = bytearray(len(d1))
    q_drive = bytearray(len(d1))

    for i in range(len(d1)):
        # Calculate P: Simple XOR
        p_val = GF256.add(d1[i], GF256.add(d2[i], d3[i]))

        # Calculate Q: Weighted Sum in Galois Field
        # We use weights 1, 2, and 3 for drives 1, 2, and 3
        term1 = GF256.mul(d1[i], 1)
        term2 = GF256.mul(d2[i], 2)
        term3 = GF256.mul(d3[i], 3)
        q_val = GF256.add(term1, GF256.add(term2, term3))

        p_drive[i] = p_val
        q_drive[i] = q_val

    return p_drive, q_drive

def reconstruct_d1_d2(d3, p, q):
    """
    Scenario: We lost D1 and D2. We have D3, P, and Q.
    We need to solve the system of linear equations for every byte.

    System:
    1) D1 + D2 = P + D3           (Call this Target_P)
    2) D1 + 2*D2 = Q + 3*D3       (Call this Target_Q)
    
    Add (XOR) the two equations:
    (D1 + D1) + (D2 + 2*D2) = Target_P + Target_Q
    0 + (1 ^ 2)*D2 = Target_P + Target_Q
    3 * D2 = Target_P + Target_Q
    
    Therefore:
    D2 = (Target_P + Target_Q) / 3
    D1 = Target_P + D2
    """
    rec_d1 = bytearray(len(d3))
    rec_d2 = bytearray(len(d3))

    for i in range(len(d3)):
        # The values we currently have on disk
        val_d3 = d3[i]
        val_p = p[i]
        val_q = q[i]

        # 1. Calculate the 'constants' side of the equations
        # Target_P = P - D3 (which is P XOR D3)
        target_p = GF256.add(val_p, val_d3)

        # Target_Q = Q - 3*D3
        val_3_d3 = GF256.mul(val_d3, 3)
        target_q = GF256.add(val_q, val_3_d3)

        # 2. Solve for D2
        # Algebraic derivation: D2 = Target_Q - Target_P
        # Acknowledging that (1 XOR 2) == 3
        sum_targets = GF256.add(target_p, target_q)
        recovered_d2 = GF256.div(sum_targets, 3)

        # 3. Solve for D1
        # Algebraic derivation: D1 = Target_P - D2
        recovered_d1 = GF256.add(target_p, recovered_d2)

        rec_d1[i] = recovered_d1
        rec_d2[i] = recovered_d2

    return rec_d1, rec_d2


def reconstruct_d1_from_q_only(d2, d3, q):
    """
    Scenario: D1 is lost. P is lost (or we just want to use Q).
    We have D2, D3, and Q.
    Equation: 1*D1 + 2*D2 + 3*D3 = Q
    Solved:   D1 = (Q + 2*D2 + 3*D3) / 1
    """
    rec_d1 = bytearray(len(d2))
    
    # The weight used for D1 in our original calculation
    weight_d1 = 1 
    
    for i in range(len(d2)):
        val_d2 = d2[i]
        val_d3 = d3[i]
        val_q  = q[i]
        
        # 1. Re-calculate the parts of Q we know (from D2 and D3)
        term2 = GF256.mul(val_d2, 2)
        term3 = GF256.mul(val_d3, 3)
        
        # 2. Combine them (sum of knowns)
        known_part = GF256.add(term2, term3)
        
        # 3. Isolate the D1 term
        # (1 * D1) = Q - (2*D2 + 3*D3)
        term1 = GF256.add(val_q, known_part)
        
        # 4. Solve for D1 by dividing by its weight
        # In this specific case, weight is 1, so it changes nothing.
        # But if we were recovering D2, we would divide by 2 here.
        rec_d1[i] = GF256.div(term1, weight_d1)
        
    return rec_d1


# --- PART 3: The Simulation ---


# 1. Create Data (3 arrays of 64 bytes)
print("--- Creating Data ---")
size = 64
disk1 = bytearray(os.urandom(size))
disk2 = bytearray(os.urandom(size))
disk3 = bytearray(os.urandom(size))

print(f"Disk 1 (first 5 bytes): {[hex(b) for b in disk1[:5]]}")
print(f"Disk 2 (first 5 bytes): {[hex(b) for b in disk2[:5]]}")
print(f"Disk 3 (first 5 bytes): {[hex(b) for b in disk3[:5]]}")

# 2. Calculate Parity
print("\n--- Calculating RAID 6 Parity (P and Q) ---")
diskP, diskQ = calculate_parity(disk1, disk2, disk3)
print(f"Disk P (first 5 bytes): {[hex(b) for b in diskP[:5]]}")
print(f"Disk Q (first 5 bytes): {[hex(b) for b in diskQ[:5]]}")

# 3a. Disaster Strikes!
print("\n--- DISASTER: Losing Disk 1 and Disk 2 ---")
# We pretend disk1 and disk2 are gone.
# We only have disk3, diskP, diskQ.

# 4. Reconstruction
print("--- Attempting Reconstruction ---")
rec_disk1, rec_disk2 = reconstruct_d1_d2(disk3, diskP, diskQ)

print(f"Rec Disk 1 (first 5 bytes): {[hex(b) for b in rec_disk1[:5]]}")
print(f"Rec Disk 2 (first 5 bytes): {[hex(b) for b in rec_disk2[:5]]}")

# 5. Verification
if rec_disk1 == disk1 and rec_disk2 == disk2:
    print("\nSUCCESS: Data completely restored from remaining 3 drives!")
else:
    print("\nFAILURE: Data corruption detected.")



print("\n--- Testing Single Drive Recovery using Q ---")
# Let's say we lost Disk 1 and Disk P. We recover Disk 1 using Q.
recovered_d1_q = reconstruct_d1_from_q_only(disk2, disk3, diskQ)

print(f"Original D1 (first 5): {[hex(b) for b in disk1[:5]]}")
print(f"Recovered D1 (first 5): {[hex(b) for b in recovered_d1_q[:5]]}")

if recovered_d1_q == disk1:
    print("SUCCESS: Disk 1 recovered using only D2, D3, and Q.")