# app/jobs.py или просто в handlers.py
from app.hhparse import hhParse
from app.habrparse import HabrParser
from app.chanelsparse import ChannelResearch

async def send_vacancies():
    data_from_hh = hhParse()
    data_from_hb = HabrParser()
    data_from_chan = ChannelResearch()

    hh_msg = await data_from_hh.the_latest()
    hb_msg = await data_from_hb.get_vacancies()
    ch_msg = await data_from_chan.parse_vacancies_async()

    ch1_msg = "\n".join(ch_msg) if ch_msg else "Вакансии из каналов не найдены."
    return f"{ch1_msg}\n{hh_msg}\n\n{hb_msg}"

    