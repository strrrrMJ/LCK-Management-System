from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import PlayerInfo, PlayerData, Schedule


def getTeamRank(year, season):
    res = dict()
    schedule = Schedule.query.filter(
        (Schedule.year == year) & (Schedule.season == season)
    ).all()
    for record in schedule:
        blue = record.blue_team
        red = record.red_team
        winner = record.winner
        if blue not in res:
            res[blue] = 0
        if red not in res:
            res[red] = 0
        res[winner] += 1
    ans = []
    for team_name, win_cnt in res.items():
        ans.append((win_cnt, team_name))
    ans.sort(reverse=True)
    return ans


@blueprint.route("/index.html")
@login_required
def index():
    YEAR = 2022
    SEASON = "Spring"
    SHOW_DATA_NUM = 7
    high_kda_data_list = (
        PlayerData.query.filter_by(year=YEAR, season=SEASON)
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
        PlayerData.query.filter_by(year=YEAR, season=SEASON)
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
        PlayerData.query.filter_by(year=YEAR, season=SEASON)
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
    team_rank = getTeamRank(year=YEAR, season=SEASON)
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
        team_rank=team_rank,
        team_num=len(team_rank),
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


@blueprint.route("/player-data.html/<player_id>")
@login_required
def player_data_specific(player_id):
    player_data = (
        PlayerData.query.filter_by(id=player_id).order_by(PlayerData.year.desc()).all()
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


@blueprint.route("/team-data.html", methods=["GET", "POST"])
@login_required
def team_data():
    if request.method == "POST":
        team_name = request.form["team-name"]
        schedule = (
            Schedule.query.filter(
                (Schedule.blue_team == team_name) | (Schedule.red_team == team_name)
            )
            .order_by(Schedule.year.desc())
            .all()
        )
        if not schedule:
            return render_template(
                "home/team-data.html",
                segment="team-data",
                search=True,
                message="This Team Doesn't Exist!",
            )
        else:
            return render_template(
                "home/team-data.html",
                segment="team-data",
                search=False,
                team_name=team_name,
                schedule=schedule,
            )
    else:
        return render_template("home/team-data.html", segment="team-data", search=True)


@blueprint.route("/team-data.html/<team_name>")
@login_required
def team_data_specific(team_name):
    schedule = (
        Schedule.query.filter(
            (Schedule.blue_team == team_name) | (Schedule.red_team == team_name)
        )
        .order_by(Schedule.year.desc())
        .all()
    )
    if not schedule:
        return render_template(
            "home/team-data.html",
            segment="team-data",
            search=True,
            message="This Team Doesn't Exist!",
        )
    else:
        return render_template(
            "home/team-data.html",
            segment="team-data",
            search=False,
            team_name=team_name,
            schedule=schedule,
        )


# @blueprint.route("/profile.html")
# @login_required
# def profile():
#     return render_template("home/profile.html", segment="profile")
