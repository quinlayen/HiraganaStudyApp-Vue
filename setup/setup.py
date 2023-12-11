#!/bin/bash python3

import toml
import os
import logging
import requests
import re

import sqlite3

from pathlib import Path
from bs4 import BeautifulSoup

from hiragana_data import hiragana_data

##############################


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

#######
# The following functions deal with downloading mp3 files for pronunciation
#######
def create_audio_directory(parent_dir):
    audio_dir = parent_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    return audio_dir

def download_file(url, dest):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(response.content)
        logging.info(f"Downloaded and saved: {dest}")
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")


def get_audio():
    setup_logging()
    parent_dir = Path(__file__).resolve().parents[1]
    audio_dir = create_audio_directory(parent_dir)
    
    url = url
    headers = {{headers}}
    try:
        req = requests.get(url, headers=headers)
        req.raise_for_status()
        soup = BeautifulSoup(req.content, 'html.parser')

        for a in soup.find_all('a', href=True):
            if a['href'].endswith('.mp3'):
                filename = Path(a['href']).name
                file_path = audio_dir / filename
                download_file(a['href'], file_path)
    except requests.RequestException as e:
        logging.error(f"Error fetching the page: {e}")

#######
# The following functions deal with creating and populating a database of hiragana characters
#######
def sqlite_connect(host):
    conn = sqlite3.connect(f"{host}")
    return conn


def create_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS hiragana
                 (id INTEGER PRIMARY KEY, character TEXT, romaji TEXT)"""
    )

    conn.executemany(
        "INSERT INTO hiragana (id, character, romaji) VALUES (?,?,?)", hiragana_data
    )

    conn.commit()
    conn.close()
