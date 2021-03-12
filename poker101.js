const { google } = require('googleapis');

// Google credentials
const creds = require('xxx');

// ID of the Google Sheets spreadsheet to retrieve data from
const spreadsheetId = 'xxx';

// Name of the sheet tab
const sheetName = 'Sheet1';

// Google credentials
const authClient = new google.auth.JWT(
    creds.client_email,
    null,
    creds.private_key,
    ['https://www.googleapis.com/auth/spreadsheets.readonly']);

const sheets = google.sheets({ version: 'v4', auth: authClient });


//--------------------andy-sheet--------------------//

// ID of the Google Sheets spreadsheet to retrieve data from
const andySpreadsheetId = 'xxx';

// Name of the sheet tab
const andySheetName = 'Sheet2';

// Google credentials
const andyAuthClient = new google.auth.JWT(
    creds.client_email,
    null,
    creds.private_key,
    ['https://www.googleapis.com/auth/spreadsheets.readonly']);

const andySheets = google.sheets({ version: 'v4', auth: andyAuthClient });

//--------------------------------------------------//


var Pusher = require('pusher-client');

var pusher = new Pusher('xxx', {
    cluster: 'eu'
});

var channel = pusher.subscribe('poker101');


var PusherServer = require('pusher');

var pusherServer = new PusherServer({
    appId: 'xxx',
    key: 'xxx',
    secret: 'xxx',
    cluster: 'eu',
    useTLS: true
});


async function get_gsheet() {

    const gsheetResponse = await sheets.spreadsheets.values.batchGet({
        spreadsheetId: spreadsheetId,
        // A1 notation of the values to retrieve  
        ranges: [sheetName],
        majorDimension: 'COLUMNS'
    });

    rangesOfValues = gsheetResponse.data.valueRanges

    var gsheetResults = [];

    rangesOfValues.forEach((range) => {
        //console.log(range);
        gsheetResults.push(range)
    });
    //console.log(gsheetResults[0].values);

    board = '';
    hand = [];
    handNumberList = [];
    player_name = [];
    player_chips = [];

    hand = gsheetResults[0].values[45].slice(-1);
    hand = parseInt(hand);
    handNumberList = gsheetResults[0].values[45].slice(1);
    /*handNumberList = handNumberList.map(function (x) {
        return parseInt(x);
    });*/

    if (gsheetResults[0].values[46][hand]) {
        board = gsheetResults[0].values[46][hand];
    } else {
        board = '';
    }
    for (let i = 0; i < 9; i++) {
        if (gsheetResults[0].values[2 + i * 5][1]) {
            player_name[i] = gsheetResults[0].values[2 + i * 5][1];
        }
        else {
            player_name[i] = 'empty';
        }
        //console.log(player_name[i]);
        if (gsheetResults[0].values[3 + i * 5][1]) {
            player_chips[i] = gsheetResults[0].values[3 + i * 5].slice(1).map(function (x) {
                return parseInt(x);
            });
        }
        else {
            player_chips[i] = '';
        }

        //console.log(player_chips[i]);
        //console.log(typeof (player_chips[i][1]));
    }

    /*debugString = "";
    debugString += hand + '</br>' + '&nbsp;' + '</br>';

    for (let i = 0; i < 9; i++) {
        debugString += player_name[i];
        debugString += '</br>';
        debugString += player_chips[i];
        debugString += '</br>' + '&nbsp;' + '</br>';
        //console.log(player_name[i]);
        //console.log(player_chips[i].slice(0, 10));
        //console.log(debugString);
    }*/

    pusherServer.trigger('poker101', 'sheet-update', {
        "message": 'hello world',
        "chartUpdate":
        {
            "handnumber": hand,
            "handnumberlist": handNumberList,
            "board": board,
            "player1": {
                "name": player_name[0],
                "chips": player_chips[0],
            },
            "player2": {
                "name": player_name[1],
                "chips": player_chips[1],
            },
            "player3": {
                "name": player_name[2],
                "chips": player_chips[2],
            },
            "player4": {
                "name": player_name[3],
                "chips": player_chips[3],
            },
            "player5": {
                "name": player_name[4],
                "chips": player_chips[4],
            },
            "player6": {
                "name": player_name[5],
                "chips": player_chips[5],
            },
            "player7": {
                "name": player_name[6],
                "chips": player_chips[6],
            },
            "player8": {
                "name": player_name[7],
                "chips": player_chips[7],
            },
            "player9": {
                "name": player_name[8],
                "chips": player_chips[8],
            }
        }
    });

    //console.log(player_name[0]);
    //console.log(player_chips[0]);
    console.log(hand);
    //console.log('\n');
    //console.log(Array.isArray(gsheetResults[0].values[2]));
    //console.log(gsheetResponse.data);
}

async function get_andy_gsheet() {

    const andyGsheetResponse = await andySheets.spreadsheets.values.batchGet({
        spreadsheetId: andySpreadsheetId,
        // A1 notation of the values to retrieve  
        ranges: [andySheetName],
        majorDimension: 'COLUMNS'
    });

    andyRangesOfValues = andyGsheetResponse.data.valueRanges

    var andyGsheetResults = [];

    andyRangesOfValues.forEach((range) => {
        //console.log(range);
        andyGsheetResults.push(range)
    });

    pointsaccum1 = [0];
    pointsaccum2 = [0];
    pointsaccum3 = [0];
    pointsaccum4 = [0];
    pointsaccum5 = [0];
    pointsaccum6 = [0];
    pointsaccum7 = [0];
    pointsaccum8 = [0];

    for (let i = 2; i < 10; i++) {
        for (let x = 65; x < 76; x++) {

            if (andyGsheetResults[0].values[i][x] != '0') {
                andyGsheetResults[0].values[i][x] = parseInt(andyGsheetResults[0].values[i][x]);
                //concat('pointsaccum' + (i - 1) + '[' + (x - 65) + ']') += pointsaccum.reduce(function (acc, val) { return acc + val; }, 0) + parseInt(andyGsheetResults[0].values[i][x]);
                //console.log(concat('pointsaccum' + (i - 1) + '[' + (x - 65) + ']'));
            }
            else {
                andyGsheetResults[0].values[i][x] = null;
            }
        }
    }


    console.log(andyGsheetResults[0].values[2][64]);
    console.log(andyGsheetResults[0].values[2].slice(65, 75));

    console.log(andyGsheetResults[0].values[3][64]);
    console.log(andyGsheetResults[0].values[3].slice(65, 75));

    console.log(andyGsheetResults[0].values[4][64]);
    console.log(andyGsheetResults[0].values[4].slice(65, 75));

    console.log(andyGsheetResults[0].values[5][64]);
    console.log(andyGsheetResults[0].values[5].slice(65, 75));

    console.log(andyGsheetResults[0].values[6][64]);
    console.log(andyGsheetResults[0].values[6].slice(65, 75));

    console.log(andyGsheetResults[0].values[7][64]);
    console.log(andyGsheetResults[0].values[7].slice(65, 75));

    console.log(andyGsheetResults[0].values[8][64]);
    console.log(andyGsheetResults[0].values[8].slice(65, 75));

    console.log(andyGsheetResults[0].values[9][64]);
    console.log(andyGsheetResults[0].values[9].slice(65, 75));

    console.log('\n');





    pusherServer.trigger('poker101', 'andy-sheet-update', {
        "message": 'hello world',
        "tableUpdate":
        {
            "player1": {
                "name": andyGsheetResults[0].values[2][64],
                "points": andyGsheetResults[0].values[2].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[2][77],
                "pointsaccum": pointsaccum1,
            },
            "player2": {
                "name": andyGsheetResults[0].values[3][64],
                "points": andyGsheetResults[0].values[3].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[3][77],
                "pointsaccum": pointsaccum2,
            },
            "player3": {
                "name": andyGsheetResults[0].values[4][64],
                "points": andyGsheetResults[0].values[4].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[4][77],
                "pointsaccum": pointsaccum3,
            },
            "player4": {
                "name": andyGsheetResults[0].values[5][64],
                "points": andyGsheetResults[0].values[5].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[5][77],
                "pointsaccum": pointsaccum4,
            },
            "player5": {
                "name": andyGsheetResults[0].values[6][64],
                "points": andyGsheetResults[0].values[6].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[6][77],
                "pointsaccum": pointsaccum5,
            },
            "player6": {
                "name": andyGsheetResults[0].values[7][64],
                "points": andyGsheetResults[0].values[7].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[7][77],
                "pointsaccum": pointsaccum6,
            },
            "player7": {
                "name": andyGsheetResults[0].values[8][64],
                "points": andyGsheetResults[0].values[8].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[8][77],
                "pointsaccum": pointsaccum7,
            },
            "player8": {
                "name": andyGsheetResults[0].values[9][64],
                "points": andyGsheetResults[0].values[9].slice(65, 75),
                "totalpoints": andyGsheetResults[0].values[9][77],
                "pointsaccum": pointsaccum8,
            }
        }
    });

}

channel.bind('row-update', function (data) {
    get_gsheet();
});

setInterval(get_andy_gsheet, 5000);
