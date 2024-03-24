from . import user


def setup_handlers(dp):
    dp.include_router(user.router)
