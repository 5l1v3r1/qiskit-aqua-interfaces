# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Qiskit Aqua browser main."""

import sys
import logging
import tkinter as tk
from qiskit_aqua_interfaces.aqua.user_interface import UIPreferences
from qiskit_aqua_interfaces._extras_require import _check_extra_requires
from ._mainview import MainView


def set_preferences_logging():
    """Update logging setting with latest external packages"""
    from qiskit.aqua._logging import get_logging_level, build_logging_config, set_logging_config
    preferences = UIPreferences()
    logging_level = logging.INFO
    if preferences.get_logging_config() is not None:
        set_logging_config(preferences.get_logging_config())
        logging_level = get_logging_level()

    preferences.set_logging_config(build_logging_config(logging_level))
    preferences.save()

    set_logging_config(preferences.get_logging_config())


def main():
    """Runs main Aqua browser command line."""
    _check_extra_requires('gui_scripts', 'qiskit_aqua_browser')
    if sys.platform == 'darwin':
        # pylint: disable=no-name-in-module, import-error
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        if bundle:
            info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            info['CFBundleName'] = 'Qiskit Aqua Browser'

    root = tk.Tk()
    root.withdraw()
    root.update_idletasks()

    preferences = UIPreferences()
    geometry = preferences.get_browser_geometry()
    if geometry is None:
        w_s = root.winfo_screenwidth()
        h_s = root.winfo_screenheight()
        w_a = int(w_s / 1.2)
        h_a = int(h_s / 1.3)
        x = int(w_s / 2 - w_a / 2)
        y = int(h_s / 2 - h_a / 2)
        geometry = '{}x{}+{}+{}'.format(w_a, h_a, x, y)
        preferences.set_browser_geometry(geometry)
        preferences.save()

    root.geometry(geometry)

    MainView(root)
    root.after(0, root.deiconify)
    root.after(0, set_preferences_logging)
    root.mainloop()
