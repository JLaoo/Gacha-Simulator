import PySimpleGUI as sg

# List of supported games
games = ['Arknights', 'Fate Grand/Order', 'Genshin Impact']

backSet = set()
goSet = set()
gamesMapping = {}
colNum = 2
for game in games:
	gamesMapping[game] = '-COL{}-'.format(colNum)
	backSet.add('-BACK{}-'.format(colNum))
	goSet.add('-GO{}-'.format(colNum))
	colNum += 1

menu = [[sg.Text("Which game to simulate rolls?")],
	   [sg.Button(game) for game in games],
	   [sg.Button("Exit")]]

arknights = [[sg.Text("Unit rarity")],
			[sg.Radio('6 Star', 'RADIO1', default=True, key="-ARKRARE6-"), 
			 sg.Radio('5 Star', 'RADIO1', default=False, key="-ARKRARE5-")],
			[sg.Text("Number of rolls to simulate:"), sg.Input(key="-ARKNUMROLLS-")],
			[sg.Button('Go!', key='-GO2-'), sg.Button('Back', key='-BACK2-')]]

fgo = [[sg.Text("Unit rarity")],
	  [sg.Radio('5 Star', 'RADIO2', default=True, key="-FGORARE5-"), 
	   sg.Radio('4 Star', 'RADIO2', default=False, key="-FGORARE4-")],
	  [sg.Text("Number of rolls to simulate:"), sg.Input(key="-FGONUMROLLS-")],
	  [sg.Button('Go!', key='-GO3-'), sg.Button('Back', key='-BACK3-')]]

genshin = [[sg.Text("Unit rarity")],
	 	  [sg.Radio('5 Star', 'RADIO3', default=True, key="-GIRARE5-"), 
	       sg.Radio('4 Star', 'RADIO3', default=False, key="-GIRARE4-")],
	  	  [sg.Text("Number of rolls to simulate:"), sg.Input(key="-GINUMROLLS-")],
	  	  [sg.Button('Go!', key='-GO4-'), sg.Button('Back', key='-BACK4-')]]

layout = [[sg.Column(menu, key='-COL1-'), 
		   sg.Column(arknights, visible=False, key='-COL2-'),
		   sg.Column(fgo, visible=False, key='-COL3-'),
		   sg.Column(genshin, visible=False, key='-COL4-')]]

window = sg.Window('Gacha Simulator', layout)

currGame = None
currCol = '-COL1-'
while True:
    event, values = window.read()
    if event in (None, 'Exit', sg.WIN_CLOSED):
    	break
    elif event in games:
    	currGame = event
    	window[currCol].update(visible=False)
    	currCol = gamesMapping[currGame]
    	window[currCol].update(visible=True)
    elif event in backSet:
    	currGame = None
    	window[currCol].update(visible=False)
    	window['-COL1-'].update(visible=True)
    	currCol = '-COL1-'
    elif event in goSet:
    	print("hello")

# Finish up by removing from the screen
window.close()