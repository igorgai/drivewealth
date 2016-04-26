from ..schemas import create_object_from_json_response


class UserApiMixin:
    def get_user(self, user_id):
        '''
        Provides details on a specific user.
        '''
        res = self.drive_wealth.users(user_id).GET()
        return create_object_from_json_response('User', res)
