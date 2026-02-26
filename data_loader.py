import pandas as pd
import glob
import os

def load_district_data(file_path='up.csv'):
    """Loads the main district-level data."""
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print(f"Warning: The file '{file_path}' is empty.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {e}")
        return None

def load_block_data(file_path='up2.csv'):
    """Loads the block-level condition data."""
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print(f"Warning: The file '{file_path}' is empty.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {e}")
        return None

def load_yearly_data(file_path='rechargefinal.csv'):
    """Loads the yearly recharge data for plotting graphs."""
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print(f"Warning: The file '{file_path}' is empty.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {e}")
        return None

def load_availability_data(file_path='availablefinal.csv'):
    """Loads the yearly availability data for plotting graphs."""
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print(f"Warning: The file '{file_path}' is empty.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {e}")
        return None

