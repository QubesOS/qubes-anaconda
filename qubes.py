#
# qubes.py
#
# Copyright (C) 2011  Invisible Things Lab All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from pyanaconda.installclass import BaseInstallClass
from pyanaconda.modules.common.constants.objects import AUTO_PARTITIONING
from pyanaconda.modules.common.constants.services import NETWORK, STORAGE, TIMEZONE, USERS
from pyanaconda.product import *
from pyanaconda.core.i18n import N_
import pyanaconda.platform
from pykickstart.constants import AUTOPART_TYPE_LVM_THINP

from blivet.size import Size
from pyanaconda.platform import platform


class InstallClass(BaseInstallClass):
    # name has underscore used for mnemonics, strip if you dont need it
    id = "qubes"
    name = N_("Qubes")
    _description = N_("The default installation of %s is a minimal install. "
                      "You can optionally select a different set of software "
                      "now.")
    _descriptionFields = (productName,)
    sortPriority = 20000
    hidden = 0
    efi_dir = 'qubes'
    _l10n_domain = "anaconda"
    installUpdates = False

    bootloaderTimeoutDefault = 5

    tasks = [(N_("Minimal"), ["base", "base-x", "qubes"])]

    help_placeholder = "QubesPlaceholder.html"
    help_placeholder_with_links = "QubesPlaceholderWithLinks.html"

    def configure(self, anaconda):
        BaseInstallClass.configure(self, anaconda)
        self.setDefaultPartitioning(anaconda.storage)

        # Default Hostname
        network_proxy = NETWORK.get_proxy()
        network_proxy.SetHostname('dom0')

        # Make encrypted partitions by default
        auto_part_proxy = STORAGE.get_proxy(AUTO_PARTITIONING)
        auto_part_proxy.SetEncrypted(True)

        # Make LVM Thin the default for autopart
        auto_part_proxy.SetType(AUTOPART_TYPE_LVM_THINP)

        # Make disabled NTP by default
        timezone_proxy = TIMEZONE.get_proxy()
        timezone_proxy.SetNTPEnabled(False)

        # Make locked root account by default
        users_proxy = USERS.get_proxy()
        users_proxy.SetRootAccountLocked(True)

    def setDefaultPartitioning(self, storage):
        BaseInstallClass.setDefaultPartitioning(self, storage)
        for autoreq in list(storage.autopart_requests):
            if autoreq.mountpoint == "/":
                autoreq.max_size = None
                autoreq.required_space = Size("10GiB")
            if autoreq.mountpoint == "/home":
                storage.autopart_requests.remove(autoreq)
            if autoreq.mountpoint == "/boot/efi":
                autoreq.max_size = Size("500MiB")
            if autoreq.mountpoint == "/boot" and \
                    isinstance(platform, pyanaconda.platform.EFI):
                # xen.efi don't need /boot
                storage.autopart_requests.remove(autoreq)

    def __init__(self):
        BaseInstallClass.__init__(self)
