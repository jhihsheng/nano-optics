## 安裝VPN與設定VPN連線
1. Install `openvpn`.
2. Click `openvpn` icon at the right bottom corner and import the config file *GPU-research*.
3. After importing, click the icon again and you will see *GPU-research*. Right-click it and connect.
4. Enter Username (vpn user帳號) and Password (VPN pass).

## 安裝與設定mobaxterm
1. Install `mobaxterm` and open it.
2. Start a new SSH session. Remote host = container IP, user name = 學號, password = 預設密碼.
   After that you will see the termial interface. You can use the termial to access the Linux container
   
## Install Conda 
1. Switch to bash shell by typing 
```
bash
```
2. Download anaconda using `wget`. We download the miniconda and save it as **miniconda.sh** 
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
```
3. Install miniconda by the command
```
bash miniconda.sh -b -p miniconda
```
and type `ls`. You will see a folder *miniconda*

4. The system need to know the path of the folder so that you can use python at any folders. To do this, you need to export the path.
    - install text editor *nano*. You need to enter 預設密碼  to use `sudo`
    ```
    sudo apt update
    sudo apt install nano
    ```
    - use nano to write the path in the *.bashrc* file
    ```
    nano ~/.bashrc
    ```
    This will open a text editor for editing the *./bashrc* file.
    - at the end of the file, add
    ```
    export PATH=~/miniconda/bin:$PATH
    ```
    use `ctrl+ X` to save the change and exit.
    
    - to make the changes take effect, 

    ```
    source ~/.bashrc
    ```
Now, you can use *conda* at any location of the system!

## Install Meep
1.  Conda environment for PyMeep (serial version) to isolate it from other Python libraries that may be installed.

```
conda create -n mp -c conda-forge pymeep pymeep-extras
```

Proceed ([y]/n) y

2. Initialize conda
```
conda init
source ~/.bashrc
```

3. activate the environment by 

```
conda activate mp
```

Now, your meep environment is complete!

4. You can install python packake in this environment.


## Install jupyterlab and ipyml 

```
conda install -c conda-forge ipympl jupyterlab
```

## Set tunneling in Mobaexterm 
1. Click tunneling on Mobaxterm and New SSH tunnel
2. Remote server = localhost, remote port = 8000, forward port = 8000, SSH Server = container ip, SSH login = 學號, SSH port = 22
2. Remember to start the tunneling by click :arrow_forward:

## Using Jupyterlab 
Now, you should be all set to begin the exploration of scienfic computing with Jupyterlab.

```
jupyter lab --port 8000
```

Copy and paste  the link `http://localhost...`
to the browser.