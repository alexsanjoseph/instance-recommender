#!/usr/bin/env python3

from instance_recommender.ui import run_streamlit_ui
import os

if __name__ == "__main__":
    run_streamlit_ui(os.environ.get('INVENTORY_SOURCE_PATH', 'file://./inventory/instances.json'))