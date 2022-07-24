from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- QUESTION ---------------------------
# ***********************************************************************


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def question_details(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exists!")
    args = {'question': question}
    return render(request, 'details_question.html', args)


@login_required(login_url="/login")
def all_questions(request):

    questions = Question.objects.get_queryset().order_by('description')
    question_filter = QuestionFilter(request.GET, queryset=questions)

    page = request.GET.get('page', 1)
    paginator = Paginator(question_filter.qs, 10)
    try:
        page_questions = paginator.page(page)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'all_questions.html', {'filter': question_filter, 'questions': page_questions})


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def create_question(request):
    answer_forms = forms.AnswerInLineFormSet(
        queryset=Answer.objects.none()
    )
    form = forms.QuestionForm()
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        answer_forms = forms.AnswerInLineFormSet(
            request.POST,
            queryset=Answer.objects.none()
        )
        if form.is_valid() and answer_forms.is_valid():
            question = form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            # return HttpResponseRedirect(reverse('Evaluator:profile'))
            return HttpResponseRedirect(question.get_absolute_url())
    return render(request, 'add_question.html',
                  {
                      'form': form,
                      'formset': answer_forms
                  })


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def edit_question(request, que_pk):
    question = Question.objects.get(pk=que_pk)
    form = forms.QuestionForm(instance=question)
    answer_forms = forms.AnswerInLineFormSet(
        queryset=form.instance.answer_set.all()
    )
    if request.method == 'POST':
        if request.POST.get('delete'):
            question.delete()
            return redirect('Evaluator:question_list')
        form = forms.QuestionForm(request.POST, instance=question)
        answer_forms = forms.AnswerInLineFormSet(
            request.POST,
            queryset=form.instance.answer_set.all()
        )
        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            return HttpResponseRedirect(question.get_absolute_url())
    return render(request, 'add_question.html',
                  {
                      'form': form,
                      'formset': answer_forms
                  })

# ***********************************************************************
# -------------------------------- QUESTION SET -------------------------
# ***********************************************************************


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def create_question_set(request):
    question_set_form = forms.QuestionSetForm()
    if request.method == 'POST':
        question_set_form = forms.QuestionSetForm(request.POST)
        if question_set_form.is_valid():
            question_set = question_set_form.save()
            return HttpResponseRedirect(question_set.get_absolute_url())
    return render(request, 'add_exam.html',
                  {
                      'form': question_set_form
                  })


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def question_set_details(request, qset_pk):
    question_set = QuestionSet.objects.get(pk=qset_pk)
    questions = Question.objects.filter(qset=question_set)
    return render(request, 'details_QuestionSet.html', {'question_set': question_set, 'questions': questions})


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def get_question_sets(request):
    question_sets = QuestionSet.objects.all()
    return render(request, 'all_qsets.html', {'question_sets': question_sets})
