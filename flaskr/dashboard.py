from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flaskr.db import get_db
from flaskr.auth import get_user, login_required, s2_required, s3_required
from flaskr.projects import get_project, get_project_users, get_all_projects, get_project_tickets
from flaskr.teams import get_users_projects, get_all_users
from flaskr.tickets import get_user_tickets
import json

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    securityLevel = g.user['security_level']

    if securityLevel == 1:
        tickets = get_user_tickets(g.user['user_id'])
        projectTitles = []
        donutData = [0,0,0,0]
        project_ticketCount_map = {}
        mapping = {"High":0, "Medium":1, "Low":2}
        for ticket in tickets:
            proj = get_project(ticket['project_id'])
            t = proj['title']
            projectTitles.append(t)
            if t not in project_ticketCount_map:
                project_ticketCount_map[t] = 1
            else:
                project_ticketCount_map[t] += 1
            donutData[mapping[ticket['priority']]] +=1
        
        if len(tickets) == 0:
            donutData = [0,0,0,1]
        
        return render_template('dashboard/dashboardS1.html', g = g, tickets = tickets, projectTitles = projectTitles, ticketCount = len(tickets), donutData = str(donutData), projectBarData = json.dumps(project_ticketCount_map))


    elif securityLevel == 2:
        projects = get_users_projects(g.user['user_id'])
        project_ticketCount_map = {}
        project_userCount = {}
        project_data = []
        donutData = [0,0,0,0]
        mapping = {"High":0, "Medium":1, "Low":2}
        for project in projects:
            tickets = get_project_tickets(project['project_id'])
            users = get_project_users(project['project_id'])
            
            project_title = project['title']
            if project_title not in project_ticketCount_map:
                project_ticketCount_map[project_title] = len(tickets)
            else:
                project_ticketCount_map[project_title] += len(tickets)
            if project_title not in project_userCount:
                project_userCount[project_title] = len(users)
            else:
                project_userCount[project_title] += len(users)
            
            project_data.append({"project":project, "tickets":tickets, "ticketCount":len(tickets), "users":users, "teamSize":len(users), "donutData":json.dumps(donutData)})
            
            
        

        return render_template('dashboard/dashboardS2.html', g = g, project_data = project_data, projectBarData = json.dumps(project_ticketCount_map), projectBarData2 = json.dumps(project_userCount))


    elif securityLevel == 3:
        allProjects = get_all_projects()
        project_ticketCount_map = {}
        project_userCount = {}
        donutData = [0,0,0,0]
        mapping = {"High":0, "Medium":1, "Low":2}
        allTickets = []
        allUsers = get_all_users()
        securityMap = {"1":0, "2":0, "3":0}

        for project in allProjects:
            tickets = get_project_tickets(project['project_id'])
            users = get_project_users(project['project_id'])
            for ticket in tickets:
                allTickets.append(ticket)
                donutData[mapping[ticket['priority']]] += 1

            project_title = project['title']
            if project_title not in project_ticketCount_map:
                project_ticketCount_map[project_title] = len(tickets)
            else:
                project_ticketCount_map[project_title] += len(tickets)
            if project_title not in project_userCount:
                project_userCount[project_title] = len(users)
            else:
                project_userCount[project_title] += len(users)
        
        for user in allUsers:
            securityMap[str(user['security_level'])] += 1


        return render_template('dashboard/dashboardS3.html', g = g, securityMap = securityMap, userCount = len(allUsers), totalTicketCount = len(allTickets), projectBarData = json.dumps(project_ticketCount_map), projectBarData2 = json.dumps(project_userCount), donutData = json.dumps(donutData))