# -*- coding:utf-8 -*-
import sys
import os
import argparse
import shlex
import subprocess

# Add project root path (labbook_BE)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app import app
from app.models.Analyzer import Analyzer
from app.models.Constants import Constants

parser = argparse.ArgumentParser(description="Test the buildLab28 function with a given specimen ID")
parser.add_argument("id_samp", type=int, help="Test specimen ID")

args = parser.parse_args()
id_samp = args.id_samp

app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def send_to_analyzer():
    """
    Function to execute the send script to the analyzer
    """
    cmd = f"sh {Constants.cst_path_script}{Constants.cst_script_analyzer}"
    cmd_split = shlex.split(cmd)
    log_file_path = f"{Constants.cst_path_log}log_script_analyzer.log"

    with open(log_file_path, "a") as log_file:
        process = subprocess.Popen(cmd_split, stdout=log_file, stderr=subprocess.STDOUT)
        process.wait()  # Attendre la fin du script

    return process.returncode == 0

with app.app_context():
    with app.test_request_context():  # Simulates an HTTP Flask request to enable session access
        print(f"HL7 message generation for id_samp={id_samp}")
        result = Analyzer.buildLab28(id_samp)

        if result:
            print(f"OML^O33 message generated with success for id_samp={id_samp}")

            print("Send message to analyzers")
            send_status = send_to_analyzer()

            if send_status:
                 print("Message successfully sent to analyzer")
            else:
                 print("Error sending message. Check logs.")

        else:
            print("Error generating message OML^O33.")
