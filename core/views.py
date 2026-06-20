from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse

from .models import PartyMember, PollingStation
from .forms import PartyMemberForm

from core.admin import PartyMemberResource, PollingStationResource


# ─────────────────────────────────────────
#  Auth
# ─────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Invalid username or password.')

    # Minimal form-like object so the template can access {{ form.username.value }}
    class _FakeForm:
        class username:
            @staticmethod
            def value():
                return request.POST.get('username', '')
        non_field_errors = []

    return render(request, 'core/login.html', {'form': _FakeForm()})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────
#  Dashboard
# ─────────────────────────────────────────

@login_required
def home_view(request):
    now = timezone.now()
    recent_members = PartyMember.objects.select_related('polling_station').order_by('-date_registered')[:5]
    total_members = PartyMember.objects.count()
    total_stations = PollingStation.objects.count()
    new_this_month = PartyMember.objects.filter(
        date_registered__year=now.year,
        date_registered__month=now.month,
    ).count()
    active_stations = PollingStation.objects.filter(members__isnull=False).distinct().count()

    return render(request, 'core/home.html', {
        'recent_members': recent_members,
        'total_members': total_members,
        'total_stations': total_stations,
        'new_this_month': new_this_month,
        'active_stations': active_stations,
    })


# ─────────────────────────────────────────
#  Members
# ─────────────────────────────────────────

@login_required
def member_list_view(request):
    qs = PartyMember.objects.select_related('polling_station').order_by('-date_registered')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(member_id__icontains=q) |
            Q(phone__icontains=q)
        )

    station_id = request.GET.get('station', '')
    if station_id:
        qs = qs.filter(polling_station_id=station_id)

    return render(request, 'core/member_list.html', {
        'members': qs,
        'stations': PollingStation.objects.all(),
        'q': q,
        'selected_station': station_id,
    })


@login_required
def member_detail_view(request, pk):
    member = get_object_or_404(PartyMember, pk=pk)
    return render(request, 'core/member_detail.html', {'member': member})


@login_required
def member_create_view(request):
    # Pre-select station from query param if provided
    initial = {}
    preselected = request.GET.get('station', '')
    if preselected:
        initial['polling_station'] = preselected

    if request.method == 'POST':
        form = PartyMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.registered_by = request.user
            member.save()
            messages.success(request, f'Member {member.first_name} {member.last_name} registered successfully.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = PartyMemberForm(initial=initial)

    return render(request, 'core/member_form.html', {'form': form})


@login_required
def member_edit_view(request, pk):
    member = get_object_or_404(PartyMember, pk=pk)

    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit member records.')
        return redirect('member_detail', pk=pk)

    if request.method == 'POST':
        form = PartyMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member record updated successfully.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = PartyMemberForm(instance=member)

    return render(request, 'core/member_form.html', {
        'form': form,
        'member': member,
    })


# ─────────────────────────────────────────
#  Polling Stations
# ─────────────────────────────────────────

@login_required
def station_list_view(request):

    query = request.GET.get("q", "").strip()
    stations = PollingStation.objects.all()
    if query:
        stations = stations.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
   
    return render(request, 'core/station_list.html', {'stations': stations, 'query':query})


@login_required
def station_detail_view(request, pk):
    station = get_object_or_404(PollingStation, pk=pk)
    members = station.members.order_by('last_name', 'first_name')
    
    return render(request, 'core/station_detail.html', {
        'station': station,
        'members': members,
    })


@login_required
def station_create_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only master admin can add polling stations.')
        return redirect('station_list')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Station name is required.')
        else:
            station = PollingStation.objects.create(
                name=name,
                location=request.POST.get('location', '').strip(),
                constituency=request.POST.get('constituency', '').strip(),
                description=request.POST.get('description', '').strip(),
            )
            messages.success(request, f'Polling station "{station.name}" added successfully.')
            return redirect('station_detail', pk=station.pk)

    return render(request, 'core/station_form.html')


@login_required
def station_edit_view(request, pk):
    station = get_object_or_404(PollingStation, pk=pk)

    if not request.user.is_staff:
        messages.error(request, 'Only administrators can edit polling stations.')
        return redirect('station_detail', pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Station name is required.')
        else:
            station.name = name
            station.location = request.POST.get('location', '').strip()
            station.constituency = request.POST.get('constituency', '').strip()
            station.description = request.POST.get('description', '').strip()
            station.save()
            messages.success(request, f'Station "{station.name}" updated successfully.')
            return redirect('station_detail', pk=station.pk)

    return render(request, 'core/station_form.html', {'station': station})


# ─────────────────────────────────────────
#  Admin Dashboard
# ─────────────────────────────────────────

@login_required
def admin_dashboard_view(request):
    """Custom admin panel — staff only. Superusers access Django /admin/."""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin panel.')
        return redirect('home')

    now = timezone.now()

    # Aggregate stats
    total_members    = PartyMember.objects.count()
    total_stations   = PollingStation.objects.count()
    new_this_month   = PartyMember.objects.filter(
        date_registered__year=now.year,
        date_registered__month=now.month,
    ).count()
    male_count       = PartyMember.objects.filter(gender='M').count()
    female_count     = PartyMember.objects.filter(gender='F').count()

    # All users except superusers (they manage themselves via Django admin)
    from django.contrib.auth.models import User
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')

    # Recent registrations
    recent_members = (
        PartyMember.objects
        .select_related('polling_station', 'registered_by')
        .order_by('-date_registered')[:10]
    )

    # Stations with member counts
    stations = PollingStation.objects.all()

    return render(request, 'core/admin_dashboard.html', {
        'total_members':  total_members,
        'total_stations': total_stations,
        'new_this_month': new_this_month,
        'male_count':     male_count,
        'female_count':   female_count,
        'users':          users,
        'recent_members': recent_members,
        'stations':       stations,
    })


@login_required
def admin_user_toggle_view(request, user_id):
    """Toggle a user's is_staff status — superuser only."""
    if not request.user.is_superuser:
        messages.error(request, 'Only the master administrator can change user roles.')
        return redirect('admin_dashboard')

    from django.contrib.auth.models import User
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, 'You cannot change your own role.')
        return redirect('admin_dashboard')

    user.is_staff = not user.is_staff
    user.save()
    role = 'Administrator' if user.is_staff else 'Member'
    messages.success(request, f'{user.get_full_name() or user.username} is now a {role}.')
    return redirect('admin_dashboard')


@login_required
def admin_user_delete_view(request, user_id):
    """Delete a user account — superuser only."""
    if not request.user.is_superuser:
        messages.error(request, 'Only the master administrator can delete users.')
        return redirect('admin_dashboard')

    from django.contrib.auth.models import User
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_dashboard')

    name = user.get_full_name() or user.username
    user.delete()
    messages.success(request, f'User "{name}" has been deleted.')
    return redirect('admin_dashboard')



#exporting data
@login_required
def export_data(request,pk):
    station = get_object_or_404(PollingStation, pk=pk)
    queryset = PartyMember.objects.filter(polling_station=station)
    dataset = PartyMemberResource().export(queryset=queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f"attachment; filename='members_{station.name}.xlsx"
    return response
