import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.handlers import send_and_dispatch
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TG_TOKEN


async def main():
   
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_and_dispatch, "cron", hour=14, minute=30, args=[bot])  
    scheduler.start()
  
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)

 
async def startup(dispatcher: Dispatcher):
    print('Starting up......')
async def shutdown(dispatcher: Dispatcher):
    print('Shutdown......')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('OK. EXIT!')