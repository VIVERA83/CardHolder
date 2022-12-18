from typing import TYPE_CHECKING

from store.database.database import Database

if TYPE_CHECKING:
    from app.core.app import Application


class Store:
    def __init__(self, app: "Application"):
        from store.card.accessor import CardAccessor
        self.card = CardAccessor(app)


def setup_store(app: "Application"):
    app.db = Database(app)
    app.on_event("startup")(app.db.connect)
    app.on_event("shutdown")(app.db.disconnect)
    app.store = Store(app)

# class Store:
#     def __init__(self, app: "Application"):
#         from app.store.bot.manager import BotManager
#         from app.store.admin.accessor import AdminAccessor
#         from app.store.quiz.accessor import QuizAccessor
#         from app.store.vk_api.accessor import VkApiAccessor
#
#         self.quizzes = QuizAccessor(app)
#         self.admins = AdminAccessor(app)
#         self.vk_api = VkApiAccessor(app)
#         self.bots_manager = BotManager(app)
#
#
# def setup_store(app: "Application"):
#     app.database = Database(app)
#     app.on_startup.append(app.database.connect)
#     app.on_cleanup.append(app.database.disconnect)
#     app.store = Store(app)
