# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import PlayerInfo, PlayerData


@blueprint.route("/index.html")
@login_required
def index():
    SHOW_DATA_NUM = 7
    high_kda_data_list = (
        PlayerData.query.filter_by(year=2022, season="Spring")
        .order_by(PlayerData.kda.desc())
        .limit(SHOW_DATA_NUM)
        .all()
    )
    kda_data = {
        "labels": [high_kda_data_list[i].id for i in range(SHOW_DATA_NUM)],
        "datasets": [
            {
                "label": "KDA",
                "tension": 0.4,
                "borderWidth": 0,
                "borderRadius": 4,
                "borderSkipped": False,
                "backgroundColor": "rgba(255, 255, 255, .8)",
                "data": [high_kda_data_list[i].kda for i in range(SHOW_DATA_NUM)],
                "maxBarThickness": 6,
            },
        ],
    }

    high_kill_data_list = (
        PlayerData.query.filter_by(year=2022, season="Spring")
        .order_by(PlayerData.k.desc())
        .limit(SHOW_DATA_NUM)
        .all()
    )
    kill_data = {
        "labels": [high_kill_data_list[i].id for i in range(SHOW_DATA_NUM)],
        "datasets": [
            {
                "label": "KILL",
                "tension": 0.4,
                "borderWidth": 0,
                "borderRadius": 4,
                "borderSkipped": False,
                "backgroundColor": "rgba(255, 255, 255, .8)",
                "data": [high_kill_data_list[i].k for i in range(SHOW_DATA_NUM)],
                "maxBarThickness": 6,
            },
        ],
    }

    high_assistance_data_list = (
        PlayerData.query.filter_by(year=2022, season="Spring")
        .order_by(PlayerData.a.desc())
        .limit(SHOW_DATA_NUM)
        .all()
    )
    assistance_data = {
        "labels": [high_assistance_data_list[i].id for i in range(SHOW_DATA_NUM)],
        "datasets": [
            {
                "label": "ASSISTANCE",
                "tension": 0.4,
                "borderWidth": 0,
                "borderRadius": 4,
                "borderSkipped": False,
                "backgroundColor": "rgba(255, 255, 255, .8)",
                "data": [high_assistance_data_list[i].a for i in range(SHOW_DATA_NUM)],
                "maxBarThickness": 6,
            },
        ],
    }

    return render_template(
        "home/index.html",
        segment="index",
        kda_data=kda_data,
        kill_data=kill_data,
        assistance_data=assistance_data,
        best_kda_player=high_kda_data_list[0],
        best_kill_player=high_kill_data_list[0],
        best_assistance_player=high_assistance_data_list[0],
        best_cp_player=PlayerData.query.filter_by(year=2022, season="Spring")
        .order_by(PlayerData.cp.desc())
        .all()[1],
    )


@blueprint.route("/tables.html")
@login_required
def tables():
    all_playerinfo = PlayerInfo.query.all()
    playerinfolist = []
    for playerinfo in all_playerinfo:
        item = dict()
        item["team_name"] = (
            PlayerData.query.filter_by(id=playerinfo.id)
            .order_by(PlayerData.year.desc())
            .first()
            .team_name
        )
        item["id"] = playerinfo.id
        item["name"] = playerinfo.name
        item["birthday"] = playerinfo.birthday
        item["residency"] = playerinfo.residency
        playerinfolist.append(item)
    return render_template(
        "home/tables.html", segment="tables", playerinfolist=playerinfolist
    )


@blueprint.route("/player-data.html", methods=["GET", "POST"])
@login_required
def player_data():
    if request.method == "POST":
        player_id = request.form["player-id"]
        player_data = (
            PlayerData.query.filter_by(id=player_id)
            .order_by(PlayerData.year.desc())
            .all()
        )
        if not player_data:
            return render_template(
                "home/player-data.html",
                segment="player-data",
                search=True,
                message="This Player Doesn't Exist!",
            )
        else:
            return render_template(
                "home/player-data.html",
                segment="player-data",
                search=False,
                player_data=player_data,
                player_team=player_data[0].team_name,
                player_id=player_data[0].id,
            )
    else:
        return render_template(
            "home/player-data.html", segment="player-data", search=True
        )


# def tables():
#     all_playerinfo = PlayerInfo.query.all()
#     tbody_str = ""
#     tr_template = "<tr><td class='text-sm font-weight-bold'><img src='static/assets/img/player-pic/{id}.png' class='border-radius-lg' width='60px' /><a href='#'>{id}</a></td><td class='text-xs font-weight-bold'>{realname}</td><td class='text-xs font-weight-bold'>{birthday}</td><td \
#         class='text-xs font-weight-bold'>{residency}</td></tr>"

#     for playerinfo in all_playerinfo:
#         tbody_str += tr_template.format(
#             id=playerinfo.id,
#             realname=playerinfo.name,
#             birthday=playerinfo.birthday,
#             residency=playerinfo.residency,
#         )
#     return render_template("home/tables.html", segment="tables", tbody_str=tbody_str)


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
