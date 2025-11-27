from django.contrib.auth.views import LogoutView

class LogoutAllowGetView(LogoutView):
    def get(self, request, *args, **kwargs):
        # Jalankan logout seperti POST
        return self.post(request, *args, **kwargs)
