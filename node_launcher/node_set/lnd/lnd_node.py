from PySide2.QtCore import QProcess

from node_launcher.node_set.lib.network_node import NetworkNode
from node_launcher.node_set.lib.node_status import NodeStatus
from .lnd_configuration import LndConfiguration
from .lnd_unlocker import LndUnlocker
from .lnd_client import LndClient
from .lnd_process import LndProcess
from .lnd_software import LndSoftware


class LndNode(NetworkNode):
    client: LndClient
    configuration: LndConfiguration
    process: LndProcess
    software: LndSoftware

    def __init__(self):
        super().__init__(
            network='lnd',
            Software=LndSoftware,
            Configuration=LndConfiguration,
            Process=LndProcess
        )
        self.client = LndClient(self)
        self.unlocker = LndUnlocker(file=self.configuration.file_path,
                                    client=self.client)

    def handle_status_change(self, new_status):
        if new_status == NodeStatus.SYNCED:
            self.unlocker.auto_unlock_wallet()

    def stop(self):
        if self.process.state() == QProcess.Running:
            self.process.expecting_shutdown = True
            self.client.stop()
