from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user
from .models import ques
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.generic import CreateView, RedirectView,UpdateView, DeleteView
from .forms import quesCreateView
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string

def home(request):
  context = initialize_context(request)
  if request.user.is_authenticated:
    user_group_set = set(request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set
  return render(request, 'tutorial/home.html', context)

def initialize_context(request):
  context = {}
  context.update(csrf(request))
  # question = ques.objects.all()
  # context['questions'] = question
  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context  

def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))  

@login_required
def ask(request):
  context = initialize_context(request) 
  if request.method == 'POST':
    form = quesCreateView(request.POST)
    if form.is_valid():
      question = form.cleaned_data.get('question')
      form.instance.asked_by= request.user    
      form.save()
      messages.success(request, f'Your question will Soon be Answered. Meanwhile Browse mostly asked questions!!!!')
      return redirect('home')
  form = quesCreateView()
  context['form'] = form
  return render(request, 'tutorial/ques_ask.html', context)

def search_ques(request):
  context = {}
  if request.method == 'POST':
    search_text = request.POST['search_text']
    all_ques = ques.objects.filter(question__contains=search_text)
    all_ques |= ques.objects.filter(asked_by__contains=search_text)
  else:
    search_text = ''
    all_ques = []  
  if request.user.is_authenticated:  
    user_group_set = set(request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set
  context['all_ques'] = all_ques
  return render(request, 'tutorial/ajax_search.html', context )    

@login_required
def my_ques(request):
  context = initialize_context(request)
  # try:
  #   request.session['user']
  # except:
  #   return HttpResponseRedirect(reverse('signin'))
  # else:
  all_ques = ques.objects.filter(asked_by=request.session['user']['name'])
  context['all_ques'] = all_ques
  if request.user.is_authenticated:
    user_group_set = set(request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set
  return render(request, 'tutorial/my_ques.html', context )  


def all(request):
  # if request.method == 'POST':
    
  question = ques.objects.all().order_by('-date_asked')
  context = {}
  context = initialize_context(request)
  context.update(csrf(request))
  context['questions'] = question
  if request.user.is_authenticated:
    user_group_set = set(request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set
  return render(request, 'tutorial/all.html', context)


def sort_ques(request):
  if request.method == 'POST':
    search_text = str(request.POST['search_text'])
    if search_text=='latest':
      all_ques = ques.objects.all().order_by('-date_asked')
    elif search_text=='oldest':
      all_ques = ques.objects.all().order_by('date_asked')
    elif search_text=='mlike':
      all_ques = ques.objects.annotate(q_count=Count('liked_by')) \
                                 .order_by('-q_count')
    elif search_text=='llike':
      all_ques = ques.objects.annotate(q_count=Count('liked_by')) \
                                 .order_by('q_count')      
        
  else:
    search_text = ''
    all_ques = []  
  context = {}  
  
  if request.user.is_authenticated:
    user_group_set = set(request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set
  context['all_ques'] = all_ques
  return render(request, 'tutorial/ajax_sort.html', context )  


class PostLikeToggle(LoginRequiredMixin, RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    slug = self.kwargs.get("slug")
    obj = get_object_or_404(ques, slug=slug)
    url_ = obj.get_absolute_url()
    user = self.request.user
    if user in obj.liked_by.all():
      obj.liked_by.remove(user)
       
    else:
      obj.liked_by.add(user) 
    context = initialize_context(self.request)
    user_group_set = set(self.request.user.likes.values_list('id',flat=True))
    context['user_group_set'] = user_group_set      
    return url_


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ques
    fields = ['question', 'answer']

    def form_valid(self, form):
      return super().form_valid(form)

    def test_func(self):
      print(self.request.user);
      post = self.get_object()
      if str(self.request.user) == "SHASHANK GOYAL":
          return True
      return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ques
    success_url = '/tutorial/'

    def test_func(self):
        post = self.get_object()
        if str(self.request.user) == "SHASHANK GOYAL":
            return True
        return False