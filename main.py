import logging
import time

import gspread
from algocode import *
from cells import *

logging.basicConfig(level=logging.INFO)

sa = gspread.service_account()
ss = sa.open("Коллоквиум")
sheet = ss.sheet1


def main():
    logging.info("Loading standings data...")
    standings_data = load_standings_data()

    logging.info("Initializing participants data")
    # init participants
    participants = parse_unique_participants(standings_data)
    # participant_name_cells = sheet.range(f"A3:A{2 + len(participants)}")
    # participant_id_cells = sheet.range(f"B3:B{2 + len(participants)}")

    # for i, participant in enumerate(participants):
    #     participant_name_cells[i].value = participant.name
    #     participant_id_cells[i].value = participant.user_id

    # logging.info("Updating participants' names and uids")
    # sheet.update_cells(participant_name_cells)
    # sheet.update_cells(participant_id_cells)

    # init contests
    logging.info("Initializing contests and problems data")
    contests = parse_contests(standings_data)

    first_problem_column = 'C'
    last_problem_column = first_problem_column
    for contest in contests:
        # contest_name_cell = sheet.range(f"{first_problem_column}1:{first_problem_column}1")
        # contest_name_cell[0].value = contest.name
        # sheet.update_cells(contest_name_cell)

        last_problem_column =\
            column_name_by_index(column_index_by_name(first_problem_column) + len(contest.problems) - 1)

        # contest_problems_cells = sheet.range(f"{first_problem_column}2:{last_problem_column}2")
        # for i, problem in enumerate(contest.problems):
        #     contest_problems_cells[i].value = problem.short_name
        # sheet.update_cells(contest_problems_cells)

        first_problem_column = next_column(last_problem_column)

    logging.info("Initializing OKs")
    # init oks
    oks_by_participant = parse_oks(standings_data)
    for i, participant in enumerate(participants):
        participant_oks_cells = None
        while True:
            try:
                participant_oks_cells = sheet.range(f"C{3+i}:{last_problem_column}{3 + i}")
                logging.info(f"Fetched results for {participant.name}")
                break
            except gspread.exceptions.APIError:
                logging.info("Exceeded requests quota, sleeping for 70 seconds now")
                time.sleep(70)

        for cell, val in zip(participant_oks_cells, oks_by_participant[participant.user_id]):
            cell.value = val

        while True:
            try:
                sheet.update_cells(participant_oks_cells)
                logging.info(f"Updated results for {participant.name}")
                break
            except gspread.exceptions.APIError:
                logging.info("Exceeded requests quota, sleeping for 70 seconds now")
                time.sleep(70)


if __name__ == "__main__":
    main()
