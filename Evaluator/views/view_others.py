from Evaluator.views.modules import *

# ***********************************************************************
# -------------------------------- Search  ---------------------------
# ***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def search_all(request):
    if request.method == 'GET':
        keyword = request.GET.get('searchKeyword')
        if keyword:
            logger.debug("Search called for keyword: %s" % keyword)
            result = global_search(keyword)
            if result:
                logger.debug("Results found")
                return render(request, 'search_results.html', {'result': result})
            else:
                logger.debug("No Results found")
                return render(request, 'search_results.html', {'message': 'No results'})
        else:
            return render(request, 'search_results.html', {'message': 'Keyword cannot be of zero length'})

# ***********************************************************************
# -------------------------------- Home  ---------------------------
# ***********************************************************************


def index(request):
    return render(request, 'Evaluator/home.html')

# ***********************************************************************
# -------------------------------- Vendor ---------------------------
# ***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def allVendors(request):
    return render(request, 'all_vendors.html', {'vendors': Vendor.objects.all()})


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def vendor_details(request, vendor_pk):
    vendor = Vendor.objects.get(pk=vendor_pk)
    return render(request, 'details_vendors.html', {'vendor': vendor})

# ***********************************************************************
# -------------------------------- Position ---------------------------
# ***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required
def position_details(request, position_pk):
    position = Position.objects.get(pk=position_pk)
    return render(request, 'details_position.html', {'position': position})


@user_passes_test(lambda u: u.is_staff)
@login_required
def all_positions(request):
    return render(request, 'all_positions.html', {'positions': Position.objects.all()})
