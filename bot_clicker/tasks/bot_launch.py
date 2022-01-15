from __future__ import absolute_import

from celery import current_task, Task

from bo.models import UserAgent
from bot_clicker.celery import app
from core.bot_core.bot_clicker_v1 import BotClickerV1


@app.task()
def test_task():
    print("celery test log")

    return True

@app.task()
def launch_bot(params):
    cpt = 0
    user_agent = UserAgent.objects.get(pk=params["user_agent"])
    for name, proxy in params["proxy"].items():
        try:
            tmp_bot = BotClickerV1(proxy=proxy, query=params["query"], domain=params["domaine"], user_agent=user_agent,
                                   online=params["online"])
            res = tmp_bot.execute()
            if not res:
                return {"detail": False, "result": "you're not in results pages"}
            cpt += 1
            if cpt == params["nb_proxy"]:
                return {"detail": True, "result": res}
        except Exception as exc:
            print(exc)
            return {"detail": False, "result": str(exc)}
