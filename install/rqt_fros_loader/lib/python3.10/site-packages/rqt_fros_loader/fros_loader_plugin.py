from rqt_gui_py.plugin import Plugin
from rqt_fros_loader.loader_widget import FrosLoaderWidget


class FrosLoaderPlugin(Plugin):

    def __init__(self, context):
        super(FrosLoaderPlugin, self).__init__(context)
        self.setObjectName('FrosLoaderPlugin')

        assert hasattr(context, 'node'), 'Context does not have a node.'
        self._widget = FrosLoaderWidget(context.node)
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

    def save_settings(self, plugin_settings, instance_settings):
        self._widget.save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        self._widget.restore_settings(plugin_settings, instance_settings)

    def trigger_configuration(self):
        self._widget.trigger_configuration()