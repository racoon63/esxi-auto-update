#!/usr/bin/env python3

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

from esxi import Versions

if __name__ == "__main__":    

    loader = DataLoader()
    esxi_versions = Versions()

    latest = esxi_versions.latest()
    playbook_path = "esxi-update.yaml"

    executor = PlaybookExecutor(playbook_path, [], {}, loader, {})

    executor.run()