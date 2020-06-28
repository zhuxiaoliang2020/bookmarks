from django.contrib.auth.models import User



#自定义采用邮件和密码登录的验证后端
class EmailAuthBackend:
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.filter(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None