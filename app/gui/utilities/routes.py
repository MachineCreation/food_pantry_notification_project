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
    from app.gui.GUI import GUI
    # import frames her to avoid circular imports

    if not isinstance(gui, GUI):
        raise TypeError("Expected a GUI instance")

    # structure for routes, and the frame class after importing
    routes = {

        # "sign_in": SignIn,
        # "sign_up": SignUp,
        # "sign_in_up_choice": SignInUpChoice,
        # "dashboard": DashBoard,
        # "send_notification": ,
        # "notification_log": ,
        # "create_template": ,
        # "manage_users": ,
        }

    try:
        route_class = routes[route]
        gui.show_route(route_class)
    except KeyError, ValueError:
        print(f"Route '{route}' not found.")
