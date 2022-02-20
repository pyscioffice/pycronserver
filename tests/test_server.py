import unittest
import json
import os
import subprocess
from crontab import CronTab
from pycronserver import get_local_pycronserver, create_config_folder


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_dir = os.path.abspath(os.path.expanduser("~/.pycronserver"))
        create_config_folder(config_dir=config_dir)
        cls._connection_str = "sqlite:///" + os.path.join(config_dir, "cron.db")
        with open(os.path.join(config_dir, "config.json"), "w") as f:
            json.dump({"connection_str": cls._connection_str}, f)

    @classmethod
    def tearDownClass(cls):
        with CronTab(user=True, tabfile=None) as cron:
            cron.remove_all(comment="pycronserver")

    def test_tasks(self):
        psc = get_local_pycronserver()
        psc.store(
            crontab="10 * * * *",
            python_funct_path="crontab.get_cronvalue",
            input_dict={"value": 1, "enums": None}
        )
        self.assertEqual(psc._get_crontab_timesteps(), ["10 * * * *"])
        psc.write_to_crontab()
        with CronTab(user=True, tabfile=None) as cron:
            self.assertEqual(list(cron.commands)[0], "pycronserver '10 * * * *', comment=pycronserver")
        subprocess.check_output(list(cron.commands)[0], shell=True)
