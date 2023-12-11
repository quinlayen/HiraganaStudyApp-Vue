# #!/bin/bash python3

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
    audio_dir = parent_dir / Path().absolute() / "audio"
    audio_dir.mkdir(exist_ok=True)
    return audio_dir

def download_file(url, dest):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest, "wb") as f:
            f.write(response.content)
        logging.info(f"Downloaded and saved: {dest}")
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")


def get_audio_main(sound_url):
    parent_dir = Path(__file__).resolve().parents[1]
    audio_dir = create_audio_directory(parent_dir)

    url = sound_url

    try:
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.content, "html.parser")

        for a in soup.find_all("a", href=True):
            if a["href"].endswith(".mp3"):
                filename = Path(a["href"]).name
                file_path = audio_dir / filename
                download_file(a["href"], file_path)
    except requests.RequestException as e:
        logging.error(f"Error fetching the page: {e}")


#######
# The following functions deal with creating and populating a database of hiragana characters
#######


def sqlite_connect(db_name):
    conn = sqlite3.connect(f"{db_name}")
    return conn


def create_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS hiragana
                 (id INTEGER PRIMARY KEY, character TEXT, romaji TEXT)"""
    )


def load_table(conn):
    conn.executemany(
        "INSERT INTO hiragana (id, character, romaji) VALUES (?,?,?)", hiragana_data
    )


def create_db_main(db_name):
    conn = sqlite_connect(f"{db_name}")

    try:
        create_table(conn)

        load_table(conn)

    except sqlite3.Error as e:
        logging.error(e)

    finally:
        conn.commit()
        conn.close()


#########
# Main function calls
#########
if __name__== "__main__":
    setup_logging()
    
    logging.info("Starting main program")
    app_config = toml.load("config.toml")
    logging.info("Configuration variables loaded")

    db_name = app_config["db"]["db_name"]
    sound_url = app_config["api"]["sound_url"]
    # headers = app_config['api']['headers']

    get_audio_main(sound_url)
    logging.INFO("Audio files downloaded")
    create_db_main(db_name)
    logging.info("Database created")
    logging.info("Setup Completed")
