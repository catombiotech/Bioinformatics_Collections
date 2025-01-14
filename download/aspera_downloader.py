import argparse
import subprocess
import os
import io 
import pandas as pd

def get_file(SRR, TYPE):
    # Define the base path for the file
    base_path = f"/vol1/{TYPE}/{SRR[:6]}/{SRR}"

    # Add your own file templates here
    file_templates = [
        f"{base_path}/00{SRR[-1]}/{SRR}/{SRR}.fastq.gz",    # SE_template_a
        f"{base_path}/{SRR}/{SRR}.fastq.gz",                # SE_template_b
        f"{base_path}/00{SRR[-1]}/{SRR}/{SRR}_1.fastq.gz",  # PE_template_a_1
        f"{base_path}/00{SRR[-1]}/{SRR}/{SRR}_2.fastq.gz",  # PE_template_a_2
        f"{base_path}/{SRR}/{SRR}_1.fastq.gz",              # PE_template_b_1
        f"{base_path}/{SRR}/{SRR}_2.fastq.gz"               # PE_template_b_2
    ]

    return file_templates

def get_args():
    parser = argparse.ArgumentParser(description="Download files from ENA using Aspera")
    parser.add_argument("-i", "--input", type=str, help="Input file with list of SRXs to download", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output directory to save files", default="./", required=False)
    parser.add_argument("-k", "--asperakey", type=str, help="Path to aspera key", required=True)
    parser.add_argument("-s", "--asperaserver", type=str, help="Aspera server", default="era-fasp@fasp.sra.ebi.ac.uk", required=False)
    parser.add_argument("-ms", "--maxspeed", help="Max speed for download", default="300m", required=False)
    return parser.parse_args()

def SRX_to_SRR(SRX):
    fetch_cmd = f"esearch -db sra -query {SRX} | efetch -format runinfo"
    fetch_result =  subprocess.run(fetch_cmd, shell=True, capture_output=True, text=True)
    if "command not found" in fetch_result.stderr:
        raise Exception("Esearch or efetch command not found. Please install edirect first.")
    
    if fetch_result.stdout == '':
        SRR = f"{SRX} not found."
        print(SRR)
    else:
        fetch_df = pd.read_csv(io.StringIO(fetch_result.stdout))
        SRR = fetch_df.Run.to_list()
    return SRR

def print_loggings_to_console(file, path, cmd, result):
    print(f"Start downloading {file}")
    print(f"Output directory: {path}")
    print(f"Command: {cmd}")
    print("Log:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)
    print("#########################")

def session_stop(cmd_result):
    flag = "Session Stop  (Error: Server aborted session: No such file or directory)" in cmd_result.stdout
    return flag

def download_from_SRX(args, SRX):
    SRR_ids = SRX_to_SRR(SRX)
    path = os.path.join(args.output, SRX)
    os.makedirs(path, exist_ok=True)
    for SRR in SRR_ids:
        file_templates = get_file(SRR, "fastq") + get_file(SRR, "sra")

        for count, tmp in enumerate(file_templates):
            file_path = args.asperaServer + ":" + tmp
            download_cmd = f"ascp -QT -l {args.maxspeed} -i {args.asperakey} {file_path} {path}"
            result = subprocess.run(download_cmd, shell=True, capture_output=True, text=True)
            if not session_stop(result):
                print_loggings_to_console(file_path, path, download_cmd, result)
                break
            if count == len(file_templates) - 1:
                print(f"File not found for {SRR} of {SRX}")


if __name__ == "__main__":
    args = get_args()

    # Create output directory if not exists
    os.makedirs(args.output, exist_ok=True)

    with open(args.input, "r") as f:
        for line in f:
            SRX = line.strip()
            print(f"Start downloading {SRX}")
            download_from_SRX(args, SRX)