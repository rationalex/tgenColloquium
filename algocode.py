from classes import *

import json
import requests

standings_data_url = "https://algocode.ru/standings_data/bp_spring2022/"


def log_main_only(log):
    if __name__ == "__main__":
        print(log)


def load_standings_data():
    r = requests.get(standings_data_url)
    data = json.loads(r.content)
    return data


def normalize(name):
    return name.replace("  ", " ")


def parse_unique_participants(standings_data):
    # parse users
    participants = []
    for user_json in standings_data["users"]:
        participants.append(Participant(name=user_json["name"],
                                        user_id=user_json["id"]))

    for participant in participants:
        participant.name = normalize(participant.name)

    oks = parse_oks(standings_data)
    participants.sort(key=lambda p: p.name)
    unique_participants = []
    i = 0
    while i < len(participants):
        j = i
        most_oks_id = participants[i].user_id
        most_oks_count = sum(oks[most_oks_id])
        while j < len(participants) and participants[j].name == participants[i].name:
            oks_count = sum(oks[participants[j].user_id])
            if oks_count > most_oks_count:
                most_oks_count = oks_count
                most_oks_id = participants[j].user_id
            j += 1

        unique_participants.append(Participant(name=participants[i].name,
                                               user_id=most_oks_id))

        i = j

    return unique_participants


def parse_contests(standings_data):
    contests = []
    for contest_json in standings_data["contests"]:
        contest = Contest(name=contest_json["title"],
                          problems=[])

        for prob in contest_json["problems"]:
            contest.problems.append(Problem(name=prob["long"],
                                            short_name=prob["short"]))

        contests.append(contest)

    return contests


# return map: uid -> [0 0 0 1 1 0 1 ... ] -- list of OK/nonOK for each problem in each contest
# order of contests and problems in them is the same as in parse_contests
def parse_oks(standings_data):
    user_results = dict()
    for contest_json in standings_data["contests"]:
        for user_id, problems_info in contest_json["users"].items():
            user_id = int(user_id)
            if user_id not in user_results:
                user_results[user_id] = []

            for problem_info in problems_info:
                if problem_info["verdict"] == "OK":
                    user_results[user_id].append(1)
                else:
                    user_results[user_id].append(0)

    return user_results


if __name__ == "__main__":
    print(parse_oks(load_standings_data()))
