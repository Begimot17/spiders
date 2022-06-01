from django.shortcuts import render
from spiders.apps.statistic.Competitionmyteam import main
from datetime import datetime
pl_keys_friends=[1321, 1319, 1318, 1320]
def index(request):
    return render(request, 'statistic.html',{'spiders':main(),'friends':pl_keys_friends,'message':f"All source"})
def date_filter(request):
    date = datetime.strptime(request.POST['started_date'], '%Y-%m-%d')
    return render(request, 'statistic.html',{'spiders':main(1,date),'friends':pl_keys_friends,'message':f"Started with {request.POST['started_date']}"})
def done_filter(request):
    date = datetime.strptime(request.POST['started_date'], '%Y-%m-%d')
    return render(request, 'statistic.html',{'spiders':main(2,date),'friends':pl_keys_friends,'message':f"Done with {request.POST['started_date']}"})