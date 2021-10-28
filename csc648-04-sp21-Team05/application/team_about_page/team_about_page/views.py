from django.shortcuts import render
from team_about_page.models import AlecTestInsert
from team_about_page.models import AngeloTestInsert
from django.contrib import messages
from django.shortcuts import redirect


import logging

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'about.html', {})
    
def about_team_member_alec(request):
    return render(request, 'team_members/about_alec.html')

def about_team_member_lakshita(request):
    return render(request, 'team_members/about_lakshita.html')

def member_bikram(request):
    return render(request, 'team_members/about_bikram.html')
# def about_team_member_alec(request):
#     return render(request, 'team_members/about_alec.html')
#
# def about_team_member_angelo(request):
#     return render(request, 'team_members/about_angelo.html')

def about_team_member(request):
    print(request.path[1:])
    return render(request, 'team_members/about_' + request.path[1:] + '.html')

def about_team_member_angelo(request):
    return render(request, 'team_members/about_angelo.html')

def about_team_member_benjamin(request):
    return render(request, 'team_members/about_benjamin.html')

def about_team_member_jiaxin(request):
    return render(request, 'team_members/about_jiaxin.html')

def about_team_member_carmen(request):
    return render(request, 'team_members/about_carmen.html')

def InsertrecordAlec(request):
    logger.error('in request')
    logger.error(request.POST)
    if request.method == 'POST':
        logger.error('in POST')
        if request.POST.get('user_name') and request.POST.get('email'):
            logger.error(request.POST.get('user_name') + request.POST.get('email'))
            saverecord = AlecTestInsert()
            saverecord.user_name = request.POST.get('user_name')
            saverecord.email = request.POST.get('email')
            saverecord.save()
            messages.success(request, 'Record Saved succesfully')
            logger.error('saved request')
            
            return redirect('/team_members_alec')
        else:
            logger.error(' request not saved ')
            messages.success(request, 'Record not saved')
            return render(request, 'about.html')

def InsertrecordAngelo(request):
    logger.error('in request')
    if request.method == 'POST':
        logger.error('in POST')
        if request.POST.get('username') and request.POST.get('email'):
            saverecord = AngeloTestInsert()
            saverecord.username = request.POST.get('username')
            saverecord.email = request.POST.get('email')
            saverecord.save()
            messages.success(request, 'Record Saved succesfully')
            return redirect('/team_members_angelo')
        else:
            logger.error(' request not saved ')
            messages.success(request, 'Record not saved')
            return render(request, 'about.html')

