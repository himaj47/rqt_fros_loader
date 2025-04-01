#!/usr/bin/env python

import os



from python_qt_binding import loadUi
# from python_qt_binding.QtCore import Qt, Slot, qWarning
# from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QWidget

import rclpy
from rqt_fros_loader.loader_utils import FrosLoader, ROSExecutor, get_resource

class FrosLoaderWidget(QWidget):
    def __init__(self, node):
        super(FrosLoaderWidget, self).__init__()
        self.setObjectName('FrosLoaderWidget')
        self._node = node

        pkg_name = 'rqt_fros_loader'
        _, package_path = get_resource('packages', pkg_name)
        ui_file = os.path.join(
            package_path, 'share', pkg_name, 'resource', 'fros_loader_widget.ui')
        
        self.overlay_selected = ""
        
        self.fros_loader = FrosLoader()
        self.exec_ = ROSExecutor()
        self.exec_.add_node_to_executor(self.fros_loader)
        self.exec_.spin()

        loadUi(ui_file, self)

        self._load_overlays.clicked.connect(self.load_overlays)
        self._refresh_available_overlays.clicked.connect(self.refresh_system_overlays_list)
        self._refresh_loaded_overlays.clicked.connect(self.refresh_loaded_overlays_list)

        self._available_overlays_list.itemClicked.connect(self.select_overlay)
        self._progressBar.setValue(0)

        self.fros_loader.update_progress_bar_.connect(self._progressBar.setValue)

    def select_overlay(self, item):
        self.overlay_selected = item.text()

    def refresh_loaded_overlays_list(self):
        pass    

    def refresh_system_overlays_list(self):
        self.fros_loader.overlays = self.fros_loader.search_system_overlays()
        self._available_overlays_list.clear()
        self._available_overlays_list.addItems(self.fros_loader.found_fros_pkgs)

    def load_overlays(self):
        if self.overlay_selected:
            self.fros_loader.handle_load(self.overlay_selected)
            # TODO unselect the selected item
        self.overlay_selected = ""

    def shutdown_plugin(self):
        # TODO unregister all publishers here

        self.fros_loader.destroy_loader()
        self.exec_.shutdown()

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
        pass
