from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- EXAM ---------------------------
# ***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def exams(request):
    Exams = Exam.objects.all()
    return render(request, 'exams.html', {'exams': Exams})


@login_required
def exam_launch_page(request):
    return render(request, 'exams_launch.html')


# ***********************************************************************
# -------------------------------- Ratings ---------------------------
# ***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def add_ratings(request, interview_pk, round_pk):
    logger.debug("%s is trying to add ratings for interview id: %s and for round id: %s" % (
        request.user.username, interview_pk, round_pk))
    if interview_pk:
        try:
            interview = Interview.objects.get(pk=interview_pk)
            max_range = interview.position.rating_sheet.rate_max
            min_range = interview.position.rating_sheet.rate_min
        except Interview.DoesNotExist:
            logger.debug("Interview not found")
            raise Http404("Interview does not exists!")
        except AttributeError:
            raise Http404(
                "No rating sheet template available for this position. Please create one!")

    if round_pk:
        try:
            rnd = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            logger.debug("Round not found")
            raise Http404("Round Name not provided")

    if request.method == 'POST':
        irs = InterviewRatingSheet.objects.create(
            name=str(interview) + '_' + rnd.name,
            interview=interview,
            round_name=rnd,
            comment=request.POST['comments'],
        )
        logger.debug("InterviewRatingSheet successfully created.")

        for key in request.POST.keys():
            if request.POST[key] == '0':
                continue  # Don't create rating aspect for a 0 entry.
            else:
                if '_aspect' in key:
                    aspect_first = key.split('_')[0]
                    rating_aspect = RatingAspect(
                        name=aspect_first,
                        interview_rating_sheet=irs,
                        points=request.POST[key],
                        comment=request.POST['{}_{}'.format(
                            aspect_first, 'comment')],
                        expected_points=int(
                            request.POST['{}_{}'.format(aspect_first, 'expected_rate')]),
                    )
                    rating_aspect.save()

        # Change the round's status as per decision
        decision = request.POST['finalDecision']
        if decision == 'OnHold':
            rnd.result = 'OH'
        elif decision == 'Advanced':
            rnd.result = 'ADV'
        elif decision == 'Rejected':
            rnd.result = 'RJ'
        else:
            raise Http404("Invalid Decision.")

        rnd.save()

        logger.debug("All Aspects for IRS successfully created...Returning")
        return HttpResponseRedirect(interview.get_absolute_url())

    return render(request, 'add_rating.html',
                  {
                      'interview': interview,
                      'round': rnd,
                      'rating_range': range(min_range, max_range+1),
                  })


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def rating_details(request, rating_pk):
    try:
        rating = InterviewRatingSheet.objects.get(pk=rating_pk)
    except InterviewRatingSheet.DoesNotExist:
        raise Http404("Ratings does not exists!")

    rating_aspects = RatingAspect.objects.filter(interview_rating_sheet=rating)
    aspects_name = [aspect.name for aspect in rating_aspects]
    aspects_points = [aspect.points for aspect in rating_aspects]
    aspects_exp_points = [aspect.expected_points for aspect in rating_aspects]

    return render(request, 'details_rating.html',
                  {
                      'rating_sheet': rating,
                      'aspects': rating_aspects,
                      'aspects_name': json.dumps(aspects_name),
                      'aspects_points': json.dumps(aspects_points),
                      'aspects_exp_points': json.dumps(aspects_exp_points),

                  })
