#!/usr/bin/env python

import glob, gspread, os, pprint, pusher, sys, re, time
from pygtail import Pygtail
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials


def delete_file(x):
    if os.path.exists(x):
        os.unlink(x)


def write_line_to_file():
    hand_file_working = open(hand_file, "a")
    hand_file_working.write(line)
    hand_file_working.close()


def search_for_completed_hand():
    global hand
    hand_file_working = open(hand_file)
    hand = regex_hand.search(hand_file_working.read())
    hand_file_working.close()


def parse_file():
    global board
    global chips
    global summary_split
    hand_file_working = open(hand_file)
    chips = regex_chips.findall(hand_file_working.read())
    hand_file_working.close()
    hand_file_working = open(hand_file)
    summary = regex_summary.search(hand_file_working.read())
    hand_file_working.close()
    hand_file_working = open(hand_file)
    board = regex_board.search(hand_file_working.read())
    if board:
        board = board[1]
    hand_file_working.close()
    summary_split = regex_summary_split.findall(summary[0])


def get_latest_file():
    global latest_file
    latest_file = max(
        glob.iglob(
            "/Users/jNap/Library/Application Support/PokerStarsUK/HandHistory/jnynap/*"
        ),
        key=os.path.getctime,
    )


# --------------------pusher-API-------------------- #
pusher_client = pusher.Pusher(
    app_id="xxx", key="xxx", secret="xxx", cluster="eu", ssl=True,
)
# -------------------------------------------------- #

# --------------------sheets-API-------------------- #
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/Users/jNap/Documents/VSCode/Python/test/Sheets-xxx.json", scope
)

client = gspread.authorize(creds)

gsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/xxx/edit?usp=sharing"
).sheet1
# -------------------------------------------------- #

data = {}
hand_list = []
hand_number = 0

get_latest_file()

log_file = latest_file
offset_file = "/Users/jNap/Documents/VSCode/Python/test/offset_file.txt"
hand_file = Path("/Users/jNap/Documents/VSCode/Python/test/hand_file.txt")

regex_hand = re.compile(r"PokerStars.*?\n\n", re.DOTALL)

regex_chips = re.compile(r"Seat\s\d:\s(.*?)\s\((\d*?)(?=\s)", re.DOTALL)

regex_summary = re.compile(r"(?<=\*\*\*\sSUMMARY\s\*\*\*).*?(Seat.*)(?=\n)", re.DOTALL)

regex_board = re.compile(r"Board\s\[(.*?)(?=\])", re.DOTALL)

regex_summary_split = re.compile(
    r"Seat\s(\d):\s.*?((\(|collected|folded|mucked|showed)(.*?))(?=\n)", re.DOTALL
)

delete_file(offset_file)
delete_file(hand_file)

gsheet.clear()

gsheet_initialize_list = []
for x in range(50):
    gsheet_initialize_list.append("")

gsheet.batch_update([{"range": "A1", "values": [gsheet_initialize_list]}])

gsheet.format(
    "", {"numberFormat": {"type": "TEXT"},},
)

gsheet.freeze(rows=1)

gsheet.batch_update(
    [
        {
            "range": "A1",
            "values": [
                [
                    "player1_hand",
                    "player1_seat",
                    "player1_name",
                    "player1_chips",
                    "player1_action",
                    "player2_hand",
                    "player2_seat",
                    "player2_name",
                    "player2_chips",
                    "player2_action",
                    "player3_hand",
                    "player3_seat",
                    "player3_name",
                    "player3_chips",
                    "player3_action",
                    "player4_hand",
                    "player4_seat",
                    "player4_name",
                    "player4_chips",
                    "player4_action",
                    "player5_hand",
                    "player5_seat",
                    "player5_name",
                    "player5_chips",
                    "player5_action",
                    "player6_hand",
                    "player6_seat",
                    "player6_name",
                    "player6_chips",
                    "player6_action",
                    "player7_hand",
                    "player7_seat",
                    "player7_name",
                    "player7_chips",
                    "player7_action",
                    "player8_hand",
                    "player8_seat",
                    "player8_name",
                    "player8_chips",
                    "player8_action",
                    "player9_hand",
                    "player9_seat",
                    "player9_name",
                    "player9_chips",
                    "player9_action",
                    "hand",
                    "board",
                ]
            ],
        },
    ]
)


while True:
    for line in Pygtail(log_file, offset_file=offset_file):
        # write line to file
        write_line_to_file()
        # search for completed hand
        search_for_completed_hand()
        # when complete hand found
        if hand is not None:
            gsheet_hand_data = []
            gsheet_seat_list = [None] * 9
            seat_list = []  # for dictionary key
            summary_split_clean = []
            hand_number += 1
            parse_file()
            # store data in dictionary
            for i in range(len(chips)):
                name = chips[i][0]  # regex result
                chip_stack = chips[i][1]  # regex result
                # redact mucked hands
                summary_split_clean.append(
                    re.sub(
                        r"mucked\s\[..\s..\]", "mucked [Xx Xx]", summary_split[i][1]
                    )  # result from initial regex
                )

                data[
                    hand_number, int(summary_split[i][0])
                ] = (  # dictionary keys, hand number and seat number (seat number result from regex)
                    str(hand_number),  # hand number
                    summary_split[i][0],  # seat number
                    name,  # name
                    chip_stack,  # chip stack
                    summary_split_clean[i],  # action
                )
                seat_list.append(
                    int(summary_split[i][0])
                )  # list of seat numbers to iterate through second dictionary key

            # --------------------get-value-lengths-------------------- #
            hand_length_list = []
            seat_length_list = []
            name_length_list = []
            chip_length_list = []
            action_length_list = []
            for i in range(len(seat_list)):
                hand_length_list.append(
                    len((data[hand_number, seat_list[i]][0]))
                )  # hand
                seat_length_list.append(
                    len((data[hand_number, seat_list[i]][1]))
                )  # seat
                name_length_list.append(
                    len((data[hand_number, seat_list[i]][2]))
                )  # name
                chip_length_list.append(
                    len((data[hand_number, seat_list[i]][3]))
                )  # chip count
                action_length_list.append(
                    len((data[hand_number, seat_list[i]][4]))
                )  # action
            hand_length_list.sort(reverse=True)
            seat_length_list.sort(reverse=True)
            name_length_list.sort(reverse=True)
            chip_length_list.sort(reverse=True)
            action_length_list.sort(reverse=True)
            hand_lemgth_max = seat_length_list[0]
            seat_lemgth_max = seat_length_list[0]
            name_lemgth_max = name_length_list[0]
            chip_lemgth_max = chip_length_list[0]
            action_lemgth_max = action_length_list[0]
            # --------------------------------------------------------- #

            # print data
            if board:
                print(board)

            for i in range(len(seat_list)):
                for x in range(
                    hand_lemgth_max
                    + seat_lemgth_max
                    + name_lemgth_max
                    + chip_lemgth_max
                    + action_lemgth_max
                    + 18
                ):
                    print("-", end="")
                print("\n", end="")
                print(
                    "  "
                    + (data[hand_number, seat_list[i]][0]).center(
                        hand_lemgth_max, " "
                    )  # hand
                    + " | "
                    + (data[hand_number, seat_list[i]][1]).center(
                        seat_lemgth_max, " "
                    )  # seat
                    + " | "
                    + (data[hand_number, seat_list[i]][2]).center(
                        name_lemgth_max, " "
                    )  # name number
                    + " | "
                    + (data[hand_number, seat_list[i]][3]).center(
                        chip_lemgth_max, " "
                    )  # chip count
                    + " | "
                    + (data[hand_number, seat_list[i]][4]).center(
                        action_lemgth_max, " "
                    )  # action
                )
            for x in range(
                hand_lemgth_max
                + seat_lemgth_max
                + name_lemgth_max
                + chip_lemgth_max
                + action_lemgth_max
                + 18
            ):
                print("-", end="")

            print("\n")

            for x in range(len(seat_list)):
                gsheet_seat_list[seat_list[x] - 1] = seat_list[x]

            for i in range(9):
                if gsheet_seat_list[i] is not None:
                    for x in range(5):
                        gsheet_hand_data.append(
                            data[hand_number, gsheet_seat_list[i]][x]
                        )
                else:
                    for x in range(5):
                        gsheet_hand_data.append(None)

            gsheet_hand_data.append(hand_number)

            if board:
                gsheet_hand_data.append(board)
            else:
                gsheet_hand_data.append(None)

            gsheet.batch_update(
                [{"range": "A" + str(hand_number + 1), "values": [gsheet_hand_data]}]
            )

            pusher_client.trigger(
                "poker101",
                "row-update",
                {
                    "handnumber": gsheet_hand_data[45],
                    "board": gsheet_hand_data[46],
                    "player1": {
                        "name": gsheet_hand_data[2],
                        "chips": gsheet_hand_data[3],
                        "action": gsheet_hand_data[4],
                    },
                    "player2": {
                        "name": gsheet_hand_data[7],
                        "chips": gsheet_hand_data[8],
                        "action": gsheet_hand_data[9],
                    },
                    "player3": {
                        "name": gsheet_hand_data[12],
                        "chips": gsheet_hand_data[13],
                        "action": gsheet_hand_data[14],
                    },
                    "player4": {
                        "name": gsheet_hand_data[17],
                        "chips": gsheet_hand_data[18],
                        "action": gsheet_hand_data[19],
                    },
                    "player5": {
                        "name": gsheet_hand_data[22],
                        "chips": gsheet_hand_data[23],
                        "action": gsheet_hand_data[24],
                    },
                    "player6": {
                        "name": gsheet_hand_data[27],
                        "chips": gsheet_hand_data[28],
                        "action": gsheet_hand_data[29],
                    },
                    "player7": {
                        "name": gsheet_hand_data[32],
                        "chips": gsheet_hand_data[33],
                        "action": gsheet_hand_data[34],
                    },
                    "player8": {
                        "name": gsheet_hand_data[37],
                        "chips": gsheet_hand_data[38],
                        "action": gsheet_hand_data[39],
                    },
                    "player9": {
                        "name": gsheet_hand_data[42],
                        "chips": gsheet_hand_data[43],
                        "action": gsheet_hand_data[44],
                    },
                },
            )

            time.sleep(1.5)

            # print(hand_number)
            # print(gsheet_hand_data)
            # print(gsheet_seat_list)
            # print(seat_list)
            # print("\n")
            # print("\n")
            # delete file after every hand
            delete_file(hand_file)

    # --------------------comment-out-to-run-live-------------------- #
    # break
    # --------------------------------------------------------------- #
# pprint.pprint(data, width=200)

print("\n")
