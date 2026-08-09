print() {
    echo "${color_B}${1}${color_N}"
}

input() {
    echo "${color_Y}[Input] ${1}${color_N}"
}

log() {
    echo "${color_G}[Log] ${1}${color_N}"
}

warn() {
    echo "${color_Y}[WARNING] ${1}${color_N}"
}

error() {
    echo -e "${color_R}[Error] ${1}\n${color_Y}${*:2}${color_N}"
    exit 1
}

pause() {
    input "Press Enter/Return to continue (or press Ctrl+C to cancel)"
    read -s
}

get_distro() {
    source /etc/os-release

    # version check
    if [[ -n $UBUNTU_CODENAME ]]; then
        case $UBUNTU_CODENAME in
            "jammy" | "kinetic"   ) ubuntu_ver=22;;
            "lunar" | "mantic"    ) ubuntu_ver=23;;
            "noble" | "oracular"  ) ubuntu_ver=24;;
            "plucky" | "questing" ) ubuntu_ver=25;;
            "resolute" ) ubuntu_ver=26;;
        esac
        if [[ -z $ubuntu_ver ]]; then
            source /etc/upstream-release/lsb-release 2>/dev/null
            ubuntu_ver="$(echo "$DISTRIB_RELEASE" | cut -c -2)"
        fi
        if [[ -z $ubuntu_ver ]]; then
            ubuntu_ver="$(echo "$VERSION_ID" | cut -c -2)"
        fi
    elif [[ -e /etc/debian_version ]]; then
        debian_ver=$(cat /etc/debian_version)
        case $debian_ver in
            *"sid" | "kali"* ) debian_ver="sid";;
            * ) debian_ver="$(echo "$debian_ver" | cut -c -2)";;
        esac
    elif [[ $ID == "fedora" || $ID_LIKE == "fedora" || $ID == "nobara" ]]; then
        fedora_ver=$VERSION_ID
    fi

    # distro check
    if [[ $ID == "arch" || $ID_LIKE == "arch" || $ID == "artix" || $ID == "cachyos" ]]; then
        distro="arch"
    elif (( ubuntu_ver >= 22 )) || (( debian_ver >= 12 )) || [[ $debian_ver == "sid" ]]; then
        distro="debian"
    elif (( fedora_ver >= 40 )); then
        distro="fedora"
        if [[ $(command -v rpm-ostree) ]]; then
            distro="fedora-atomic"
        fi
    # i don't use void, opensuse, or gentoo.
    # elif [[ $ID == "opensuse-tumbleweed" ]]; then
    #     distro="opensuse"
    # elif [[ $ID == "gentoo" || $ID_LIKE == "gentoo" || $ID == "pentoo" ]]; then
    #     distro="gentoo"
    # elif [[ $ID == "void" ]]; then
    #     distro="void"
    else
        warn "Your distro ($platform_ver - $platform_arch) is not detected/supported. See the repo README for supported OS versions/distros"
        print "* You may still continue, but you will need to install required packages and libraries manually as needed."
        sleep 5
        pause
    fi
}

install_deps() {
    print "* eraNAS will be installing dependencies from your distribution's package manager"
    print "* Enter your user password when prompted"
    print "* Your password input may not be visible, but it is still being entered."

    if [[ $distro != "debian" && $distro != "fedora-atomic" ]]; then
        echo
        warn "Before continuing, make sure that your system is fully updated first!"
        echo "${color_Y}* This operation can result in a partial upgrade and may cause breakage if your system is not updated${color_N}"
        echo
    fi
    pause

    echo "Installing dependencies..."
    if [[ $distro == "arch" ]]; then
        $sudo pacman -Sy --noconfirm --needed wine-staging winetricks wget git
    elif [[ $distro == "debian" ]]; then
        $sudo apt update
        $sudo apt install -m -y wget
        case $debian_ver in
            14 ) $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/forky/winehq-forky.sources;;
            13 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/trixie/winehq-trixie.sources;;
            12 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources;;
        esac
        case $ubuntu_ver in
            25 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/questing/winehq-questing.sources;;
            24 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/plucky/winehq-plucky.sources;;
            23 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources;;
            22 ) $sudo dpkg --add-architecture i386 & $sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources;;
        esac
        $sudo apt install --install-recommends winehq-staging
        $sudo apt install -m -y winetricks git
    elif [[ $distro == "fedora" ]]; then
        $sudo dnf install -y wine-staging winetricks wget git

    # i don't use void, opensuse, or gentoo.
    # elif [[ $distro == "opensuse" ]]; then
    #     $sudo zypper -n install aria2 ca-certificates curl git libimobiledevice-1_0-6 libzstd1 openssl-3 patch python3 sshfs usbmuxd unzip vim zenity zip
    #     prepare_udev_rules usbmux usbmux # idk if this is right

    # elif [[ $distro == "gentoo" ]]; then
    #     $sudo emerge -av --noreplace app-arch/zstd app-misc/ca-certificates libimobiledevice net-fs/sshfs net-misc/aria2 net-misc/curl openssh python udev app-arch/unzip usbmuxd usbutils vim zenity app-arch/zip

    # elif [[ $distro == "void" ]]; then
    #     $sudo xbps-install aria2 curl git patch openssh python3 unzip xxd zenity zip
    elif [[false]]; then
        echo yes

    fi

    # echo "$platform_ver" > "../resources/"

    log "Distro dependency installation done! eraNAS should now boot promptly after setting up the prefix."
}
sudo="/usr/bin/sudo"
if [[ $($sudo -V 2>&1) == "sudo-rs"* ]]; then
    if [[ -z $device_disable_sudoloop && -z $device_disable_usbmuxd ]]; then
        log "sudo-rs detected. Switching to sudo.ws"
    fi
    sudo+=".ws"
fi
BASEDIR="$( cd "$( dirname "$0" )" && pwd )"
TERM=xterm-256color # fix colors for msys2 terminal
color_R=$(tput setaf 9)
color_G=$(tput setaf 10)
color_B=$(tput setaf 12)
color_Y=$(tput setaf 208)
color_N=$(tput sgr0)
if [[ ! $(cat "/usr/bin/wget") || ! $(cat "/usr/bin/tar") || ! $(cat "/usr/bin/wine") || ! $(cat "/usr/bin/winetricks") ]]; then
    get_distro
    install_deps
fi
cd $BASEDIR
# Check if key exist
if ! (test -f "id_ed25519_eraCorrectionHub"); then
    echo "${color_R}* id_ed25519_eraCorrectionHub file not found..."
    echo "This file is used to authenticate with the host server and is required to use this launcher."
    echo "Please re-extract eraNAS."
    error "id_ed25519_eraCorrectionHub file not found..."
fi

# Determine which branch to fetch from
GIT_SSH_COMMAND=ssh -i id_ed25519_eraCorrectionHub
if [[ -f .git/HEAD ]]; then
    log "Git installation detected"
    git pull
else
    # if [[ -f .git/HEAD && $(git rev-parse --abbrev-ref HEAD) == "dev/NASNightly" ]]; then
    #     branch="dev/NASNightly"
    # else
    #     branch="dev/omogatari-kai"
    # fi
    # download VERSION file from the git branch
    log "Archive installation detected"
    log "Downloading VERSION file from the git branch"
    log "If it asks for you credentials just don't enter anything, if it asks you abut SSH keys respond with yes."
    git archive --remote=git@ssh.gitgud.io:mrpopsalot/pops-tw "dev/omogatari-kai" VERSION | tar -xO > VERSION
fi
# download .net desktop 8
log "Downloading .NET 8 Desktop Runtimes"
winetricks dotnetdesktop8 arch=64
# run game
log "Launching eraNAS. Have fun!"
wine start /unix "$BASEDIR/LazyLoadingV26.exe"
