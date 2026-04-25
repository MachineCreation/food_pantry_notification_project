#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/utilities/routes.py
# Author: Joseph Egan
# 2026-04-22
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description: route handler

# Local imports

# python imports


def send_to_route(route: str, gui: callable) -> None:
    '''
    send to route
    '''
    from app.GUI.GUI import GUI
    from app.GUI.dashboard.models.DashBoard import DashBoard
    from app.GUI.LogInOut.models.SignIn import SignIn
    from app.GUI.LogInOut.models.SignUp import SignUp
    from app.GUI.LogInOut.models.SignInUpChoice import SignInUpChoice
    from app.GUI.NotificationLog.NotificationLog import NotificationLog

    if not isinstance(gui, GUI):
        raise TypeError("Expected a GUI instance")
    routes = {
        "sign_in": SignIn,
        "sign_up": SignUp,
        "sign_in_up_choice": SignInUpChoice,
        "dashboard": DashBoard,
        "send_notification": DashBoard,
        "notification_log": NotificationLog,
        "create_template": DashBoard,
        "manage_users": DashBoard
        }

    try:
        route_class = routes[route]
        gui.show_route(route_class)
    except KeyError:
        print(f"Route '{route}' not found.")
