from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- INTERVIEW ---------------------------
# ***********************************************************************


def get_interviews_as_per_filters(request_get):
    args = {}
    status = request_get["status"]
    if status:
        args["status"] = status

    position = request_get["position"]

    if request_get["position"]:
        args["position"] = position

    start_date = request_get["start_date"]
    if start_date:
        args["date__gte"] = start_date

    end_date = request_get["end_date"]
    if end_date:
        args["date__lte"] = end_date

    # 1 is today, 2 is past 7 days, 3 is this month, 4 is this year, yesterday is 5
    reg_year = {
        "today": timezone.now().today().date(),
        "month": timezone.now().month,
        "year": timezone.now().year,
        "yesterday": timezone.now().today().date() - timezone.timedelta(days=1),
        "past7days": timezone.now().today().date() - timezone.timedelta(days=7),
    }

    registry_year = request_get["registry_year"]

    if registry_year != "":
        if registry_year == "4":
            # interviews = Interview.objects.filter(status=status, date__lte=end_date, date__gte=start_date, date__year=reg_year['year'], position=position).order_by('id')
            args["date__year"] = reg_year["year"]
        elif registry_year == "1":
            # interviews = Interview.objects.filter(status=status, date=reg_year['today'], position=position).order_by('id')
            args["date"] = reg_year["today"]
        elif registry_year == "2":
            # interviews = Interview.objects.filter(status=status, date__lte=reg_year['today'], date__gte=reg_year['past7'], position=position).order_by('id')
            args["date__lte"] = reg_year["today"]
            args["date__gte"] = reg_year["past7days"]
        elif registry_year == "3":
            # interviews = Interview.objects.filter(status=status, date__month=reg_year['month'], position=position).order_by('id')
            args["date__month"] = reg_year["month"]
        elif registry_year == "5":
            # interviews = Interview.objects.filter(status=status, date=reg_year['yesterday'], position=position).order_by('id')
            args["date"] = reg_year["yesterday"]

    interviews = Interview.objects.filter(**args)

    return interviews


@user_passes_test(lambda u: u.is_staff)
@login_required
def all_interviews(request):

    if "download_interview" in request.GET.keys():
        """
        If user clicks the "Download Report button, the request.GET has a key by the name 'download_interview'. "
        The key has been injected on the template "templates/all_interviews.html" with name given to the download button.
        This one: <button class="btn btn-primary btn-lg" type="submit" name="download_interview">Download Results</button>
        We collect the filter values and get all interviews as per filters selected.
        Then we write the values for each interview in a csv file. The file is directly download on the user's machine.
        """
        interviews = get_interviews_as_per_filters(request.GET)

        result = [
            ["Candidate Name", "Interview Date", "Position", "Status", "Result"],
        ]
        for interview in interviews:
            row = [
                interview.candidate.name,
                interview.date,
                interview.position.name,
                interview.get_status_display(),
                interview.get_result_display(),
            ]
            result.append(row)

        logger.debug(
            "Download interview filter results. Initiated by: %s"
            % request.user.username
        )
        response = download_csv_report(result, report_name="report_interview.csv")
        return response

    interviews = Interview.objects.get_queryset().order_by("-date")
    interview_filter = InterviewFilter(request.GET, queryset=interviews)

    page = request.GET.get("page", 1)
    paginator = Paginator(interview_filter.qs, 10)
    try:
        page_interviews = paginator.page(page)
    except PageNotAnInteger:
        page_interviews = paginator.page(1)
    except EmptyPage:
        page_interviews = paginator.page(paginator.num_pages)

    return render(
        request,
        "all_interviews.html",
        {"filter": interview_filter, "interviews": page_interviews},
    )


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def get_interviews_by_date(request, year, month, day):
    try:
        date = datetime.date(int(year), int(month), int(day))
    except ValueError:
        return render(
            request,
            "Evaluator/interview_list.html",
            {"message": "Incorrect Date range entered ! "},
        )
    interviews = Interview.objects.filter(date=date).order_by("date")
    if interviews:
        return render(
            request, "Evaluator/interview_list.html", {"interviews": interviews}
        )
    else:
        return render(
            request,
            "Evaluator/interview_list.html",
            {"message": "No interviews found scheduled! "},
        )


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
@user_passes_test(lambda u: "Evaluator.add_interview" in u.get_group_permissions())
def add_interview(request):
    round_forms = forms.RoundInLineFormSet(queryset=Round.objects.none())
    form = forms.AddInterview()
    if request.method == "POST":
        form = forms.AddInterview(request.POST)
        round_forms = forms.RoundInLineFormSet(
            request.POST, queryset=Round.objects.none()
        )
        if form.is_valid() and round_forms.is_valid():
            interview = form.save()
            rounds = round_forms.save(commit=False)
            for a_round in rounds:
                a_round.interview = interview
                a_round.save()
            return HttpResponseRedirect(interview.get_absolute_url())
    return render(request, "add_interview.html", {"form": form, "formset": round_forms})


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def interviews_details(request, interview_pk):
    try:
        interview = Interview.objects.get(pk=interview_pk)
    except Interview.DoesNotExist:
        raise Http404("Interview does not exists!")

    all_rounds = interview.round_set.order_by("created_at")
    args = {"interview": interview, "rounds": all_rounds}

    return render(request, "details_interview.html", args)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def edit_interview(request, interview_pk):
    interview = Interview.objects.get(pk=interview_pk)
    form = forms.AddInterview(instance=interview)
    round_forms = forms.RoundInLineFormSet(queryset=form.instance.round_set.all())
    if request.method == "POST":
        form = forms.AddInterview(request.POST, instance=interview)
        round_forms = forms.RoundInLineFormSet(
            request.POST, queryset=form.instance.round_set.all()
        )
        if form.is_valid() and round_forms.is_valid():
            form.save()
            rnds = round_forms.save(commit=False)
            for rnd in rnds:
                rnd.interview = interview
                rnd.save()
            return HttpResponseRedirect(interview.get_absolute_url())
    return render(request, "add_interview.html", {"form": form, "formset": round_forms})


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def calendar(request, year, month):
    my_interviews = Interview.objects.order_by("date").filter(
        date__year=year, date__month=month
    )
    cal = InterviewCalendar(my_interviews).formatmonth(year, month)
    return render(
        request,
        "Evaluator/calendar.html",
        {"calendar": mark_safe(cal), "year_passed": year, "month_passed": month},
    )
