%post --nochroot

# Install kernel-latest if running not the one that is installed already
latest=$(rpm --root=$ANA_INSTALL_PATH --qf '%{VERSION}-%{RELEASE}.%{ARCH}\n' -q kernel | sort -V | tail -1)
running=$(uname -r)
if [ "$latest" != "$running" ]; then
    dnf --installroot=$ANA_INSTALL_PATH --setopt=reposdir=/etc/yum.repos.d -y install kernel-latest
    dnf --installroot=$ANA_INSTALL_PATH --setopt=reposdir=/etc/yum.repos.d -y install kernel-latest-qubes-vm
fi

%end
