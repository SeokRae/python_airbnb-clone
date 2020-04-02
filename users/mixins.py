from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# email 로그인이 아닌 계정에 대한 페이지 권한 관리 (password change)
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 로그아웃한 사람만 볼 수 있는 페이지 권한 체크 (signup)
class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 로그인 관련 권한 체크
class LoggedInOnlyView(LoginRequiredMixin):
    # 로그인 되어 있지 않은 사용자에게 url 요청
    login_url = reverse_lazy("users:login")
