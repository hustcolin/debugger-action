#@title **RDP**
#@markdown  It takes 4-5 minutes for installation

import os
import subprocess

#@title **Create User**
#@markdown Enter Username and Password

username = "user" #@param {type:"string"}
password = "user" #@param {type:"string"}

print("Creating User and Setting it up")

# Creation of user
os.system(f"useradd -m {username}")

# Add user to sudo group
os.system(f"adduser {username} sudo")
    
# Set password of user to 'root'
os.system(f"echo '{username}:{password}' | sudo chpasswd")

# Change default shell from sh to bash
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

print("User Created and Configured")


## 第二部分
#@markdown  Visit http://remotedesktop.google.com/headless and Copy the command after authentication

CRP = "DISPLAY= /opt/google/chrome-remote-desktop/start-host --code=\"4/0AX4XfWjfxvZ6lkXJM0cyid1d_-3eTLbx5fuWbD5J80niS3nPuWgFTYx9GyztuQgK_XoVRQ\" --redirect-url=\"https://remotedesktop.google.com/_/oauthredirect\" --name=$(hostname)" #@param {type:"string"}

#@markdown Enter a pin more or equal to 6 digits
Pin = 123456 #@param {type: "integer"}


class CRD:
    def __init__(self):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installGoogleChorme()
        self.finish()

    @staticmethod
    def installCRD():
        print("Installing Chrome Remote Desktop")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)

    @staticmethod
    def installDesktopEnvironment():
        print("Installing Desktop Environment")
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("systemctl disable lightdm.service")

    @staticmethod
    def installGoogleChorme():
        print("Installing Google Chrome")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)

    @staticmethod
    def finish():
        print("Finalizing")
        os.system(f"adduser {username} chrome-remote-desktop")
        command = f"{CRP} --pin={Pin}"
        os.system(f"su - {username} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        print("Finished Succesfully")


try:
    if username:
        if CRP == "":
            print("Please enter authcode from the given link")
        elif len(str(Pin)) < 6:
            print("Enter a pin more or equal to 6 digits")
        else:
            CRD()
except NameError as e:
    print("username variable not found")
    print("Create a User First")
	
	
	
## 第三部分	
#@title **SSH**

! pip install colab_ssh --upgrade &> /dev/null

Ngrok = True #@param {type:'boolean'}
Agro = False #@param {type:'boolean'}


#@markdown Copy authtoken from https://dashboard.ngrok.com/auth (only for ngrok)
ngrokToken = "1sLEzQdE9WuXWd9wUShJoLkSlqb_21bpRZSV4KQpNKKhh8ZVf" #@param {type:'string'}


def runNGROK():
    from colab_ssh import launch_ssh
    from IPython.display import clear_output
    launch_ssh(ngrokToken, password)
    clear_output()

    print("ssh", username, end='@')
    ! curl -s http://localhost:4040/api/tunnels | python3 -c \
            "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'][6:].replace(':', ' -p '))"


def runAgro():
    from colab_ssh import launch_ssh_cloudflared
    launch_ssh_cloudflared(password=password)


try:
    if username:
        pass
    elif password:
        pass
except NameError:
    print("No user found using username and password as 'root'")
    username='root'
    password='root'


if Agro and Ngrok:
    print("You can't do that")
    print("Select only one of them")
elif Agro:
    runAgro()
elif Ngrok:
    if ngrokToken == "":
        print("No ngrokToken Found, Please enter it")
    else:
        runNGROK()
else:
    print("Select one of them")	
	