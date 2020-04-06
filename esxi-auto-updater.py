#!/usr/bin/env python3

import json
import os
import shutil
import sys

from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C

from esxi import Versions

def run_playbook(playbook_path, hosts_path, key_file):
    pass

if __name__ == "__main__":    

    esxi_versions = Versions()

    latest = esxi_versions.latest()
    
    
    playbook_path = "esxi-update.yaml"

    if not os.path.exists(playbook_path):
        sys.exit("Playbook can not be found")

    class ResultCallback(CallbackBase):
    
        def v2_runner_on_ok(self, result, **kwargs):
            
            host = result._host
            print(json.dumps({host.name: result._result}, indent=4))

    context.CLIARGS = ImmutableDict(connection='local', module_path=['/to/mymodules'], forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False)

    loader = DataLoader()
    passwords = dict(vault_pass='secret')
    results_callback = ResultCallback()
    inventory = InventoryManager(loader=loader, sources='localhost,')
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    play = Play().load(playbook_path, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords=passwords,
            stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
        )
        result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        if tqm is not None:
            tqm.cleanup()

        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)