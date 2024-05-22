from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pull: async_sessionmaker):
        self.session_pull = session_pull

    async def __call__(
            self,
            handler:Callable[[TelegramObject, Dict[str, Any]],Awaitable[Any]],
            event: TelegramObject,
            data:Dict[str, Any] 
    )-> Any:
        async with self.session_pull() as session:
            data['session'] = session
            return await handler(event, data)    





# class CounterMiddleware(BaseMiddleware):
#     def __init__(self) -> None:
#         self.counter = 0

#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any]
#     ) -> Any:
#         self.counter += 1
#         data['counter'] = self.counter
#         return await handler(event, data)