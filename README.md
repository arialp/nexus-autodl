# Nexus AutoDL 
When utilizing [Nexus Mods](https://nexusmods.com/) for Game Modding, the typical procedure involves manually clicking the download button each time a new mod is added to the download queue. 
However, this manual process can become problematic when dealing with tools such as [Wabbajack](https://www.wabbajack.org/) or [Portmod](https://gitlab.com/portmod/portmod), which may involve numerous mods, potentially numbering in the hundreds or even thousands. 

To address this issue, Nexus AutoDL serves as an autoclicker designed to streamline and automate this process. While Nexus AutoDL is active, it continuously monitors the screen for instances when a download button for a Nexus Mod(the "Slow Download" button) or Collections button from Vortex becomes visible. 
In such cases, Nexus AutoDL takes action by automatically clicking the download button, effectively removing the need for manual intervention. This automation significantly enhances the efficiency and convenience of the mod downloading experience. 
## Note
Using a bot to download from Nexus is in direct violation of their TOS:

> Attempting to download files or otherwise record data offered through our services (including but not limited to the Nexus Mods website and the Nexus Mods API) in a fashion that drastically exceeds the expected average, through the use of software automation or otherwise, is prohibited without expressed permission. Users found in violation of this policy will have their account suspended.

Use this at your own risk.

## Building nexus-autodl

Install latest version of [Python](https://www.python.org/downloads/)

### Upgrade pip
```python -m pip install --upgrade pip``` 

### Install required dependencies 
```
pip install yapf
pip install mypy
pip install pyinstaller
pip install pillow
pip install pyautogui
pip install numpy
pip install click
pip install opencv-python
python -m pip install types-Pillow
```
Download the repo as zip, or, `git clone https://github.com/arialp/nexus-autodl.git` in bash

Download and run Make from [GnuWin32](https://sourceforge.net/projects/gnuwin32/files/make/3.81/) and add the executable to PATH,

Open Makefile with Notepad++ (or any other equivalent),

Edit Makefile and add the required exec paths,

In powershell, run `make all` from the repo folder.

#### If nexus changes the button style you can always make new screenshots of the button and overwrite the ones in /templates/
