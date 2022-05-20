# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import PlayerInfo


@blueprint.route("/index.html")
@login_required
def index():
    return render_template("home/index.html", segment="index")


@blueprint.route("/tables.html")
@login_required
def tables():
    all_playerinfo = PlayerInfo.query.all()
    tbody_str = ""
    tr_template = "<tr><td class='font-weight-bold'>{id}</td><td class='font-weight-bold'>{realname}</td><td class='font-weight-bold'>{birthday}</td><td \
        class='font-weight-bold'>{residency}</td></tr>"

    for playerinfo in all_playerinfo:
        tbody_str += tr_template.format(
            id=playerinfo.id,
            realname=playerinfo.name,
            birthday=playerinfo.birthday,
            residency=playerinfo.residency,
        )
    return render_template("home/tables.html", segment="tables", tbody_str=tbody_str)


@blueprint.route("/billing.html")
@login_required
def billing():
    return render_template("home/billing.html", segment="billing")


@blueprint.route("/notifications.html")
@login_required
def notifications():
    return render_template("home/notifications.html", segment="notifications")


@blueprint.route("/profile.html")
@login_required
def profile():
    return render_template("home/profile.html", segment="profile")


# # Helper - Extract current page name from request
# def get_segment(request):

#     try:

#         segment = request.path.split("/")[-1]

#         if segment == "":
#             segment = "index"

#         return segment

#     except:
#         return None
