from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- Openings ---------------------------
# ***********************************************************************


@login_required
def all_openings(request):
    openings = JobOpening.objects.all()
    return render(request, 'Evaluator/job_openings.html', {'openings': openings})


@login_required
def create_opening(request):
    form = forms.CreateJobOpeningForm()
    if request.method == 'POST':
        form = forms.CreateJobOpeningForm(request.POST)
        if form.is_valid():
            opening = form.save()
            return redirect('Evaluator:allOpenings')

    args = {'form': form}
    return render(request, 'add_job_opening.html', args)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def edit_job_opening(request, opening_pk):
    opening = JobOpening.objects.get(pk=opening_pk)
    form = forms.CreateJobOpeningForm(instance=opening)
    if request.method == 'POST':
        form = forms.CreateJobOpeningForm(request.POST, instance=opening)
        if form.is_valid():
            form.save()
            return redirect('Evaluator:allOpenings')
    return render(request, 'add_job_opening.html',
                  {
                      'form': form,
                  })
