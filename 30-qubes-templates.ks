%post --nochroot

mkdir -p /mnt/sysimage/var/lib/qubes/template-packages
dnf download \
        --setopt=reposdir=/tmp/installer.repos.d \
        --destdir=/mnt/sysimage/var/lib/qubes/template-packages \
        'qubes-template-*'

%end

