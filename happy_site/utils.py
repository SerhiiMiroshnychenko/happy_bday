"""MENU and DATA MIXIN"""

menu = [{'title': "Дні народження", 'url_name': 'b_days'},
        {'title': "Додати день народження", 'url_name': 'add_bday'},
        ]


class DataMixin:
    """
    Клас-розширення для класів-відображень сайту
    """
    @staticmethod
    def get_user_context(**kwargs) -> dict:
        """
        The get_user_context function is a helper function that returns the context dictionary for the user.
        The context dictionary contains all the information needed to render a template, including:
            - The menu items (menu)
            - The current page title (title)
            - Any other variables passed in via kwargs

        :param kwargs: Pass a variable number of keyword arguments to the function
        :return: A dictionary with the menu key and its value
        """
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu
        return context
