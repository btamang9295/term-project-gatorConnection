from django.shortcuts import render



def about(request):
    return render(request, 'about.html', {})
    
def about_team_member_alec(request):
    return render(request, 'team_members/about_alec.html')

def about_team_member_lakshita(request):
    return render(request, 'team_members/about_lakshita.html')

def member_bikram(request):
    return render(request, 'team_members/about_bikram.html')

def about_team_member_angelo(request):
    return render(request, 'team_members/about_angelo.html')

def about_team_member_benjamin(request):
    return render(request, 'team_members/about_benjamin.html')

def about_team_member_jiaxin(request):
    return render(request, 'team_members/about_jiaxin.html')

def about_team_member_carmen(request):
    return render(request, 'team_members/about_carmen.html')

