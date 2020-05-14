%post --nochroot

mkdir -p /mnt/sysimage/var/lib/qubes/template-packages
dnf config-manager --add-repo /tmp/installer.repo
dnf download --downloaddir=/mnt/sysimage/var/lib/qubes/template-packages qubes-template-*

%end

