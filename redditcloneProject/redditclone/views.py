from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, ListView
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django_comments.models import Comment

from .models import Tread, MPTTComment
from .forms import RegistrationForm, LoginForm, TreadForm, EditComment

# Create your views here.

class home(ListView):
    template_name = 'redditclone/home.html'
    queryset = Tread.objects.all()
    object_list = queryset
    context_object_name = 'treads'

class treadCreate(FormView, LoginRequiredMixin):
    template_name = 'redditclone/tread_create.html'
    form_class = TreadForm
    success_url = 'home'

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        comment = form.cleaned_data.get('comment')
        tread = Tread.objects.create(title=title, comment=comment, user_id=self.request.user.id)
        return redirect(self.success_url)

class tread(View):
    template_name = 'redditclone/tread.html'

    def get(self, request, tread_id):
        tread = Tread.objects.filter(id=tread_id)
        context = {'tread' : tread}
        return render(self.request, self.template_name, context)

    def post(self, request, tread_id):
        tread = Tread.objects.filter(id=tread_id)
        context = {'tread' : tread}
        try:
            comment_id = self.request.POST['comment_id']
            comment = MPTTComment.objects.filter(id=comment_id)
            if (self.request.user.id == comment[0].user_id or self.request.user.is_superuser) and 'Delete' in request.POST:
                MPTTComment.objects.filter(id=comment_id).delete()
            if (self.request.user.id == comment[0].user_id or self.request.user.is_superuser) and 'Edit' in request.POST:
                return redirect('edit_comment', comment_id)
            if self.request.user.username and 'Upvote' in request.POST:
                upvote = MPTTComment.objects.filter(id=comment_id).update(votes=comment[0].votes + 1)
                return render(self.request, self.template_name, context)
            if self.request.user.username and 'Downvote' in request.POST:
                downvote = MPTTComment.objects.filter(id=comment_id).update(votes=comment[0].votes - 1)
                return render(self.request, self.template_name, context)
        except:
            return render(self.request, self.template_name, context)

class registration(FormView):
    template_name = 'redditclone/registration.html'
    form_class = RegistrationForm
    success_url = 'home'

    def form_valid(self, form):
        form = RegistrationForm(self.request.POST)
        login(self.request, form.save())
        return redirect(self.success_url)

class loginView(FormView):
    template_name = 'redditclone/login.html'
    form_class = LoginForm
    success_url = 'home'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        redirect_to = self.request.POST['next']
        context = {'form' : form}
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            form.add_error('username', 'Username doesn\t exists.')
            return render(self.request, self.template_name, context)
        if user is not None:
            password_validation = check_password(password, user.password)
            if password_validation:
                login(self.request, user)
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect(self.success_url)
            else:
                form.add_error('password', 'Wrong password')
                return render(self.request, self.template_name, context)

class edit(FormView, LoginRequiredMixin):
    template_name = 'redditclone/edit.html'
    form_class = EditComment

    def get(self, request, comment_id):
        comment = Comment.objects.filter(id=comment_id)

        if self.request.user.id == comment[0].user_id or self.request.user.is_superuser:
            form = EditComment(initial={'comment' : comment[0].comment})
            context = {'form' : form, 'comment_id' : comment[0].id}
            parent = MPTTComment.objects.filter(comment_ptr_id=comment_id)
            if parent[0].parent_id is not None:
                parent_comment_id = parent[0].parent_id
                parent_comment = Comment.objects.filter(id=parent_comment_id)
                context['parent_comment'] = parent_comment[0]
            return render(self.request, self.template_name, context)
        else:
            return redirect('home')

    def form_valid(self, form):
        comment = form.cleaned_data.get('comment')
        comment_id = self.request.POST['comment_id']
        tread_id = Comment.objects.filter(id=comment_id)
        try: 
            self.request.POST['Cancel']
            return redirect('tread', tread_id=tread_id[0].object_pk)
        except:
            new_comment = Comment.objects.filter(id=comment_id).update(comment=comment)
            return redirect('tread', tread_id=tread_id[0].object_pk)


class logoutView(View, LoginRequiredMixin):
    template_name = 'redditclone/logout.html'

    def get(self, request):
        logout(self.request)
        return render(self.request, self.template_name)
