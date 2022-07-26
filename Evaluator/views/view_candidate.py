from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- CANDIDATE ---------------------------
# ***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def bulk_upload_candis(request):
    logger.debug('Creating Bulk candidates and interviews')
    form = forms.BulkCreateInterviewsAndCandidates()
    round_forms = forms.RoundInLineFormSet(
        queryset=Round.objects.none()
    )

    if request.method == 'POST':
        form = forms.BulkCreateInterviewsAndCandidates(request.POST)
        round_forms = forms.RoundInLineFormSet(
            request.POST,
            queryset=Round.objects.none()
        )

        if form.is_valid() and round_forms.is_valid():

            names = form.cleaned_data['name_list']
            names = names.split('\r\n')

            position_id = form.cleaned_data['position'].id
            position = Position.objects.get(id=position_id)

            experience = form.cleaned_data['experience']
            vendor_id = form.cleaned_data['vendor'].id
            vendor = Vendor.objects.get(id=vendor_id)
            date = form.cleaned_data['date']

            # Create Candidates
            for candi in names:
                logger.debug('Creating for :%s' % candi)
                my_candi = Candidate(
                    name=candi, position_applied=position, experience=experience, vendor=vendor)
                my_candi.save()
                logger.debug('Candidate created')

                my_interview = Interview(
                    candidate=my_candi,
                    date=date,
                    position=position,
                )

                my_interview.save()

                logger.debug('Interview created')

                # Creating and Saving Rounds
                logger.debug('Creating Rounds')
                for int_round in round_forms:
                    r = Round.objects.create(
                        name=int_round.cleaned_data['name'],
                        assignee=int_round.cleaned_data['assignee'],
                        comments=int_round.cleaned_data['comments'],
                        date=int_round.cleaned_data['date'],
                        contact_time=int_round.cleaned_data['contact_time'],
                        round_type=int_round.cleaned_data['round_type'],
                        interview=my_interview,
                    )
                    for support in int_round.cleaned_data['supporting_interviewer']:
                        r.supporting_interviewer.add(support)
                    r.save()

                logger.debug('Rounds created')
            return redirect('Evaluator:all_candidates')
        else:
            args = {'form': form, 'message': 'No Valid Form'}
            return render(request, 'bulk_upload_candis.html', args)

    args = {'form': form, 'round_form': round_forms}
    return render(request, 'bulk_upload_candis.html', args)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def add_candidate(request):
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.name = form.cleaned_data['name']
            candidate.contact_primary = form.cleaned_data['contact_primary']
            candidate.experience = form.cleaned_data['experience']
            candidate.position_applied = form.cleaned_data['position_applied']
            candidate.save()
            for sk in form.cleaned_data['skill']:
                skill = Skill.objects.get(name=sk)
                candidate.skill.add(skill)

            return HttpResponseRedirect(candidate.get_absolute_url())
    else:
        form = forms.AddCandidateForm()
        args = {'form': form}
        return render(request, 'add_candidate.html', args)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def all_candidates(request):
    candidates = Candidate.objects.get_queryset().order_by('-created_at')
    candidate_filter = CandidateFilter(request.GET, queryset=candidates)
    page = request.GET.get('page', 1)
    paginator = Paginator(candidate_filter.qs, 10)
    try:
        page_candidates = paginator.page(page)
    except PageNotAnInteger:
        page_candidates = paginator.page(1)
    except EmptyPage:
        page_candidates = paginator.page(paginator.num_pages)

    return render(request, 'all_candidates.html', {'candidates': page_candidates, 'filter': candidate_filter})


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def edit_candidate(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(candidate.get_absolute_url())
    else:
        form = forms.AddCandidateForm(instance=candidate)
        args = {'form': form}
        return render(request, 'add_candidate.html', args)


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def candi_details(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    interviews = Interview.objects.filter(candidate=candidate)

    # This is for showing the Upload button.
    resume_form = forms.DocumentForm()
    if request.method == 'POST':
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            # This is because, candidate is not passed in form.POST
            document.candidate = candidate
            document.save()

    # Find out if the candidate has a resume attached.
    try:
        candi_document = Document.objects.get(candidate=candidate_pk)
    except Document.DoesNotExist:
        candi_document = None

    args = {'candidate': candidate, 'interviews': interviews,
            'candi_doc': candi_document, 'resume_form': resume_form}

    return render(request, 'details_candidate.html', args)
