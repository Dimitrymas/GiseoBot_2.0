from sweater import bot
from sweater.controller.user_controller import UserController


def listen_callback(callback):
    if callback.data == 'registration':
        UserController.registration_step_start(message=callback.message)



