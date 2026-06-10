import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers import catalog, common, orders

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not settings.bot_token:
        logger.warning("BOT_TOKEN не задан — бот не запускается. Заполни .env.")
        return

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(common.router)
    dp.include_router(catalog.router)
    dp.include_router(orders.router)

    # Сбрасываем вебхук на случай переключения с webhook на polling.
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен (long polling)")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
