import importlib
import json
from crontab import CronTab
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class CronTasks(Base):
    __tablename__ = "crontasks"
    id = Column(Integer, primary_key=True)
    crontab = Column(String)
    python_funct = Column(String)
    input_json = Column(String)


class PyCronServer:
    def __init__(self, session, username=True):
        self._session = session
        self._username = username

    def get_crontab_timesteps(self):
        return [entry[0] for entry in self._session.query(CronTasks.crontab).all()]

    def write_to_crontab(self):
        with CronTab(user=self._username) as cron:
            cron.remove_all(comment="pycronserver")
            for cron_tab in set(self.get_crontab_timesteps()):
                job = cron.new(
                    command='pycronserver "' + cron_tab + '"', comment="pycronserver"
                )
                job.setall(cron_tab)

    def store(self, crontab, python_funct_path, input_dict):
        self._session.add(
            CronTasks(
                crontab=crontab,
                python_funct=python_funct_path,
                input_json=json.dumps(input_dict),
            )
        )

    def execute_tasks(self, crontab):
        for task in (
            self._session.query(CronTasks).filter(CronTasks.crontab == crontab).all()
        ):
            execute_funct(
                module_funct=task.python_funct, input_dict=json.loads(task.input_json)
            )

    @staticmethod
    def execute_funct(module_funct, input_dict):
        return execute_funct(module_funct=module_funct, input_dict=input_dict)


def execute_funct(module_funct, input_dict):
    module_funct_lst = module_funct.split(".")
    funct_name = module_funct_lst[-1]
    module_path = ".".join(module_funct_lst[:-1])
    module = importlib.import_module(module_path)
    funct = getattr(module, funct_name)
    return funct(**input_dict)


def get_pycronserver(engine, session, username=True):
    Base.metadata.create_all(engine)
    return PyCronServer(session=session, username=username)
