# Help document for download

## aspera downloader
### Requirements
We recommend to use `mamba` to manage your environments.
```shell
mamba create -n aspera_env
mamba activate aspera_env
mamba install bioconda::entrez-direct
mamba install install hcc::aspera-cli
```
Your sshkey is stored at `~/miniforge3/envs/aspera_env/etc/asperaweb_id_dsa.openssh`.

### How to use
Check out `python aspera_downloader.py --help` for details:
```
usage: aspera_downloader.py [-h] -i INPUT [-o OUTPUT] -k ASPERAKEY [-s ASPERASERVER] [-ms MAXSPEED]

Download files from ENA using Aspera

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Input file with list of SRXs to download
  -o, --output OUTPUT   Output directory to save files
  -k, --asperakey ASPERAKEY
                        Path to aspera key
  -s, --asperaserver ASPERASERVER
                        Aspera server
  -ms, --maxspeed MAXSPEED
                        Max speed for download
```

Your input SRX list should be organized into a file with a single column, without any other information. For example:
your input file should look like srx_list.txt
```
SRX123456
SRX123457
SRX123458
```
Then run the command below after activating your environment:
```shell
python aspera_downloader.py -i srx_list.txt \
                            -o ./output_dir/ \
                            -k ~/miniforge3/envs/aspera_env/etc/asperaweb_id_dsa.openssh 
```
