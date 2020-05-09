%post --nochroot

mkdir -p /mnt/sysimage/root/qubes-templates
cp -r /mnt/install/repo/Packages/qubes-template-*.rpm /mnt/sysimage/root/qubes-templates

%end