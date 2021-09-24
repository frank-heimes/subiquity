#!/usr/bin/env python3
# Copyright 2015-2021 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import subprocess

log = logging.getLogger("subiquity.system_setup.common.wsl_utils")

config_ref = {
    "wsl": {
        "automount": {
            "enabled": "automount",
            "mountfstab": "mountfstab",
            "root": "custom_path",
            "options": "custom_mount_opt",
        },
        "network": {
            "generatehosts": "gen_host",
            "generateresolvconf": "gen_resolvconf",
        },
        "interop": {
            "enabled": "interop_enabled",
            "appendwindowspath": "interop_appendwindowspath",
        }
    },
    "ubuntu": {
        "GUI": {
            "theme": "gui_theme",
            "followwintheme": "gui_followwintheme",
        },
        "Interop": {
            "guiintegration": "legacy_gui",
            "audiointegration": "legacy_audio",
            "advancedipdetection": "adv_ip_detect",
        },
        "Motd": {
            "wslnewsenabled": "wsl_motd_news",
        }
    }
}


def is_reconfigure(is_dryrun):
    if is_dryrun and \
                 os.getenv("DRYRUN_RECONFIG") == "true":
        return True
    if_normaluser = False
    with open('/etc/passwd', 'r') as f:
        for line in f:
            # check every normal user except nobody (65534)
            if int(line.split(':')[2]) >= 1000 and \
               int(line.split(':')[2]) != 65534:
                if_normaluser = True
                break
    return not is_dryrun and if_normaluser


def get_windows_locale():
    windows_locale_failed_msg = (
        "Cannot determine Windows locale, fallback to default."
        " Reason of failure: "
    )

    try:
        process = subprocess.run(["powershell.exe", "-NonInteractive",
                                  "-NoProfile", "-Command",
                                  "(Get-Culture).Name"],
                                 capture_output=True)
        if process.returncode:
            log.info(windows_locale_failed_msg +
                     process.stderr.decode("utf-8"))
            return None

        tmp_code = process.stdout.rstrip().decode("utf-8")
        tmp_code = tmp_code.replace("-", "_")
        return tmp_code
    except OSError as e:
        log.info(windows_locale_failed_msg + e.strerror)
        return None
