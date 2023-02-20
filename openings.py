import sqlite3


def addPlayer(player):
    if player in players:
        players[player] += 1
    else:
        players[player] = 1
        
        
def extract_sequence(source):
    seq = ''
    list_seq = source.split('\n')[0:10]
    for l_s in list_seq:
        list_seq2 = l_s.split(' ')
        seq += list_seq2[1][0:2] + list_seq2[2][0:2]

    return seq


def addSequence(source):
    length = len(source) // 2
    if source in openings[length-1]:
        openings[length-1][source] += 1
    else:
        openings[length-1][source] = 1


players = dict()
openings = list()
for _ in range(20):
    openings.append(dict())    

conn = sqlite3.connect('y.sqlite')
cursorObj = conn.cursor()
cursorObj.execute('SELECT * FROM games')

for row in cursorObj:
    addPlayer(row[1])
    addPlayer(row[2])
    seq = extract_sequence(row[8])
    for i in range(20):
        addSequence(seq[0:i*2+2])

players = sorted(players.items(), key=lambda x: x[1], reverse=True)
with open("players.txt", 'w') as f: 
    for player in players: 
        f.write(f'{player[0]}: {player[1]}\n')

for i in range(20):
    opening = sorted(openings[i].items(), key=lambda x: x[1], reverse=True)
    with open(f"opening{i+1}.txt", 'w') as f: 
        for op in opening: 
            f.write(f'{op[0]}: {op[1]}\n')
    
    
cursorObj.close()
conn.close()
