#!/usr/bin/env python

import rclpy
import rclpy.executors
from rclpy.node import Node
from std_msgs.msg import ByteMultiArray

from time import sleep
from rqt_fros_loader import logging
import threading
from ament_index_python.resources import get_resources, get_resource

from python_qt_binding.QtCore import Signal, QObject


CHUNCK_SIZE = 1024
class FrosLoader(Node, QObject):
    _update_progress_bar = Signal(int)

    def __init__(self):
        Node.__init__(self, node_name="loader_utils")
        QObject.__init__(self)
        logging.info('loader_utils Node Initialized')

        self.overlays = self.search_system_overlays()
        
        # self.overlays = ui.Load_overlays(ui.preLoadedOverlays)
        # self.pg_bar = ui.pg_bar

        self.found_fros_pkgs = []

        self.msg = ByteMultiArray()
        self.pub =  self.create_publisher(ByteMultiArray, "load_node", 10)
        # self.timer_ = self.create_timer(0.2, self.loader)

    # def loader(self):
    #     global load_overlay, choosen_overlay
    #     if load_overlay:
    #         print("loading overlay ...")
    #         self.handle_load(choosen_overlay)
    #         print(f"successfully loaded {choosen_overlay}")
    #         load_overlay = False

    def divide_chunks(self, l, n):
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def handle_load(self, selected_option):
        self.get_logger().info(f'Loaded: {selected_option}')

        data = str()
        for overlay in self.overlays:
            if overlay[0] == selected_option:

                self.get_logger().info(f"reading elf file {overlay[1]}")
                fd = open(overlay[1], 'rb')
                data = fd.read()
                fd.close()

        self.msg.layout.data_offset = len(data)
        chuncks = list(self.divide_chunks(data, CHUNCK_SIZE))

        i = 0
        for chunck in chuncks:
            print(chunck)
            self.msg.data = [i.to_bytes(1, 'little') for i in chunck]
            self.pub.publish(self.msg)

            sleep(0.1)

            i += 1
            val = int((100/len(chuncks)) * i)

            self._update_progress_bar.emit(val)

            # self.pg_bar.setTextVisible(True)
            # self.pg_bar.setValue(val)
        
        # self.pg_bar.setTextVisible(False)

    def search_system_overlays(self):
        resource_type = "fros-overlays"
        found_res = list()
        found_pkgs = list()
        try:
            # Get all resources of the specified type
            resources = get_resources(resource_type)

            if not resources:
                # print(f"No resources of type '{resource_type}' found.")
                logging.info(f"No resources of type '{resource_type}' found.")
                return found_res

            # print(f"Resources of type '{resource_type}':")
            for package_name in resources:
                # Get the resource content or location (if applicable)
                resource_content = get_resource(resource_type, package_name)
                found_res.append([package_name, resource_content[0]])
                # print(f"- Package: {package_name}")
                # print(f"  Resource content: {resource_content}")
                found_pkgs.append(package_name)
        except KeyError as e:
            print(f"Error locating resources: {e}")
            logging.error(f"Error locating resources: {e}")

        self.found_fros_pkgs = found_pkgs
        return found_res
    
    def destroy_loader(self):
        self.pub.destroy()
        # self.timer_.destroy()
        self.destroy_node()


class ROSExecutor:
    def __init__(self):
        self.executor_ = rclpy.executors.MultiThreadedExecutor()
        self.ros_thread = threading.Thread(target=self.exec_spin, name="ros_thread", daemon=True)

    def add_node_to_executor(self, node:Node):
        self.executor_.add_node(node)

    def exec_spin(self):
        self.executor_.spin() 

    def spin(self):
        self.ros_thread.start()

    def shutdown(self):
        self.executor_.shutdown()