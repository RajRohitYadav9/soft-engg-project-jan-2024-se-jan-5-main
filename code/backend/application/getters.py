from flask import request

def get_user_id() ->str:
    """
        Usage
        ------
        Get User-Id from the request header,
        ------
        Returns
        ------
        """
    return request.headers.get('User-Id')

def get_web_token() ->str:
    """
        Usage
        ------
        Get Web-Token from the request header,
        ------
        Returns
        ------
        """
    return request.headers.get('Web-Token')


def get_username(db_table, user_id):
    return db_table.query.filter_by(user_id=user_id).first().username