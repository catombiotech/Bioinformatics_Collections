# Help document for download

## aspera downloader
### Requirements
```shell
mamba create -n aspera_env
mamba install bioconda::entrez-direct
mamba install install hcc::aspera-cli
mamba activate aspera_env
```
Your sshkey is storeds at `~/miniforge3/envs/aspera_env/etc/asperaweb_id_dsa.openssh`

### Quick start
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