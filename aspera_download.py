# WRR
import subprocess
import os
import io
import pandas as pd

#export PATH=/xtdisk/yangyg_group/wangrr/miniforge3/bin:$PATH
os.environ['ASCP_PATH'] = "/xtdisk/yangyg_group/wangrr/miniforge3/envs/aspera-cli/bin/ascp"
ASPERA_KEY="/xtdisk/yangyg_group/wangrr/miniforge3/envs/aspera-cli/etc/asperaweb_id_dsa.openssh"
ASPERA_SERVER="era-fasp@fasp.sra.ebi.ac.uk"
MAX_SPEED="300m"

download_dir = "/xtdisk/yangyg_group/wangrr/my_file/download_test"
TYPE = "fastq" # sra / fastq
SRX_list = ["SRX2201090", "SRX2201091"]

# Check at https://www.ebi.ac.uk/ena/browser/home
#################### File templates ############################
# TYPE: "sra" or "fastq"
######## Single end: (one of the following) ####################
# a.
def get_file(SRR):
    SE_a = f"/vol1/{TYPE}/{SRR[:6]}/00{SRR[-1]}/{SRR}/{SRR}.fastq.gz"
    # b.
    SE_b = f"/vol1/{TYPE}/{SRR[:6]}/{SRR}/{SRR}.fastq.gz"
    ####### Paired end (one of the following) ######################
    # a.
    PE_a_1 = f"/vol1/{TYPE}/{SRR[:6]}/00{SRR[-1]}/{SRR}/{SRR}_1.fastq.gz"
    PE_a_2 = f"/vol1/{TYPE}/{SRR[:6]}/00{SRR[-1]}/{SRR}/{SRR}_2.fastq.gz"
    # b. 
    PE_b_1 = f"/vol1/{TYPE}/{SRR[:6]}/{SRR}/{SRR}_1.fastq.gz"
    PE_b_2 = f"/vol1/{TYPE}/{SRR[:6]}/{SRR}/{SRR}_2.fastq.gz"
    return SE_a, SE_b, PE_a_1, PE_a_1, PE_b_1, PE_b_2
#################################################################

def SRX_2_SRR(SRX):
    cmd = f"esearch -db sra -query {SRX} | efetch -format runinfo"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if "command not found" in result.stderr:
        raise RuntimeError("esearch or efetch command not found.")
        
    # SRX not found
    if result.stdout == '':
        SRR = f'{SRX} Not Found'
        print(SRR)
    else:
        df = pd.read_csv(io.StringIO(result.stdout))
        #print(df)
        SRR = df.Run.to_list()
    return SRR

def print_log(file, path, cmd, result):
    print(f"Start downloading {file}")
    print(f"Output directory: {path}")
    print(f"Command: {cmd}")
    print("Log:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)
    print("#########################")

def download_from_SRX(SRX):
    def session_stop(cmd_result):
        flag = "Session Stop  (Error: Server aborted session: No such file or directory)" in cmd_result.stdout
        return flag

    path = os.path.join(download_dir, SRX)
    if not os.path.exists(path): 
        os.makedirs(path)

    SRR_ids = SRX_2_SRR(SRX) 
    for SRR in SRR_ids:
        SE_a, SE_b, PE_a_1, PE_a_1, PE_b_1, PE_b_2 = get_file(SRR)
        # 1st try
        file = ASPERA_SERVER + ":" + SE_a
        cmd = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file} {path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if not session_stop(result):
            print_log(file, path, cmd, result)
        # 2nd try
        else:
            file = ASPERA_SERVER + ":" + SE_b
            cmd = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file} {path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if not session_stop(result):
                print_log(file, path, cmd, result)
            # 3rd try:
            else:
                file_1 = ASPERA_SERVER + ":" + PE_a_1
                file_2 = ASPERA_SERVER + ":" + PE_a_2
                cmd_1 = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file_1} {path}"
                cmd_2 = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file_2} {path}"
                result_1 = subprocess.run(cmd_1, shell=True, capture_output=True, text=True)
                result_2 = subprocess.run(cmd_2, shell=True, capture_output=True, text=True)
                if not session_stop(result_1):
                    print_log(file_1, path, cmd_1, result_1)
                    print_log(file_2, path, cmd_2, result_2)
                else:
                    file_1 = ASPERA_SERVER + ":" + PE_b_1
                    file_2 = ASPERA_SERVER + ":" + PE_b_2
                    cmd_1 = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file_1} {path}"
                    cmd_2 = f"ascp -QT -l {MAX_SPEED} -P33001 -i {ASPERA_KEY} {file_2} {path}"
                    result_1 = subprocess.run(cmd_1, shell=True, capture_output=True, text=True)
                    result_2 = subprocess.run(cmd_2, shell=True, capture_output=True, text=True)
                    print_log(file_1, path, cmd_1, result_1)
                    print_log(file_2, path, cmd_2, result_2)

def download_from_SRX_list(SRX_list):
    for SRX in SRX_list:
        print(f"Start downloading {SRX}")
        download_from_SRX(SRX)


if __name__ == "__main__":
    download_from_SRX_list(SRX_list)














