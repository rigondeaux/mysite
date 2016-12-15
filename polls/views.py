from django.shortcuts import get_object_or_404, render, HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list' # overrides default question_list

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
    return Question.objects.filter(pub_date__lte=timezone.now())
    .order_by('-pub_date')[:5]
    # amended to not include those published in future
    # lte = less than equal to


# DetailView expects a primary key captured from the url
# to be called "pk", hence why question_id was changed
# to pk in urls.py
# looks for template called <app name>/</model name>_detail.html
# it would be "polls/question_detail.html" in this case, but
# we have overridden it with "polls/detail.html"
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# vote generic view is the same as previous, no changes needed
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



#  NO LONGER USED, refactored to generic views
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # build template, fill a context, return a HttpResponse object
#     # with the results of the rendered template
#     context = {'latest_question_list': latest_question_list}
#     # return a HttpResponse object of the given template
#     # rendered with the given context
#     return render(request, 'polls/index.html', context)
#     # render takes a request object as its first argument
#     # and a template name as its second argument and
#     # a dictionary as an optional third argument
#
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #         'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))
#
# # Leave the rest of the views (detail, results, vote) unchanged
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#         # raises 404 exception if question with the requested
#         # id does not exist
#         # raise Http404("Question does not exist")
#
#     # idiom is to use get() and raise Http404 if the object doesn't exist
#     # thus the try catch block previously is replaced with:
#     question = get_object_or_404(Question, pk=question_id)
#     # get_object_or_404 takes a model as its first argument, then
#     # keyword arguments which it passes to the get() function of
#     # the model's manager. it raises an exception if the object
#     # doesn't exist (ObjectDoesNotExist)
#     # throwing an exception at the view level is better than
#     # having the exception thrown at ht emodel layer (404),
#     # as it means the view is not coupled to the model
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
