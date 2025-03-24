# Vigenère Cipher Analysis & Attack

A Python project implementing both the **Vigenère Cipher** and its **cryptanalysis** using statistical methods like **Index of Coincidence** and **Frequency Analysis**. The program is designed to break encrypted messages encoded with the Vigenère cipher without knowing the key.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [License](#license)

## Overview
The program performs cryptanalysis of the Vigenère cipher by exploiting statistical properties of the English language and the ciphertext itself. It estimates the key length using **Index of Coincidence (IC)** and deduces the key using **Frequency Analysis**.

## Features
- Encrypts and Decrypts messages using the Vigenère cipher.
- Analyzes ciphertext to estimate key length using **Index of Coincidence**.
- Uses **Frequency Analysis** to determine the most likely key.
- Supports plaintexts of arbitrary length.
- Provides detailed feedback during the decryption process.

## Requirements
- Python 3.x
- `numpy` (Install via `pip install numpy`)

## Usage
1. Clone this repository.
2. Install the required library with:
```bash
pip install numpy
```
3. Run the script:
```bash
python vigenere.py
```
4. Enter the ciphertext (multiline input supported) and type `fine` to finish.

## How It Works
- **Index of Coincidence (IC):**
  - Measures how likely two randomly selected letters from the text are identical.
  - High IC indicates the text is written in natural language.
  - By segmenting the text and analyzing each segment’s IC, the key length can be estimated.

- **Frequency Analysis:**
  - Once the key length is determined, the ciphertext is split into separate streams.
  - The program compares the frequency distribution of each stream with typical English letter frequencies to deduce the key.

- **Decryption:**
  - The key obtained is used to decrypt the ciphertext by reversing the Vigenère cipher formula.

## Limitations
- Assumes the ciphertext is in English.
- Efficiency decreases with shorter ciphertexts.
- Probabilistic approach: results may vary slightly for different ciphertexts.

