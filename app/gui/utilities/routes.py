#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/utilities/routes.py
# Author: Joseph Egan
# 2026-04-22
# Sources:
# Contributors: Justin Crump, Lloyd Truong
# -------------------------------------------------------------------------------
# Description: route handler

# Local imports
from app.gui.template_creation.models.template_frame import TemplateFrame


# python imports
from typing import Callable


def send_to_route(route: str, gui: Callable) -> None:
    '''
    send to route
    '''
    from app.gui.GUI import GUI
    from app.gui.log_in_out.models.SignIn import SignIn
    from app.gui.log_in_out.models.SignUp import SignUp
    from app.gui.log_in_out.models.SignInUpChoice import SignInUpChoice
    from app.gui.dashboard.models.DashBoard import DashBoard
    from app.gui.send_notification.models.SendNotification import \
        SendNotification
    from app.gui.notification_log.NotificationLog import NotificationLog
    from app.gui.template_creation.models.template_frame import TemplateFrame

    if not isinstance(gui, GUI):
        raise TypeError("Expected a GUI instance")

    # structure for routes, and the frame class after importing
    routes = {

        "sign_in": SignIn,
        "sign_up": SignUp,
        "sign_in_up_choice": SignInUpChoice,
        "dashboard": DashBoard,
        "notification_log": NotificationLog,
        "send_notification": SendNotification,
        "create_template": TemplateFrame,
        # "manage_users": ,
        }

    try:
        route_class = routes[route]
        gui.show_route(route_class)
    except KeyError:
        print(f"Route '{route}' not found.")
