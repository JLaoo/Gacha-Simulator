import PySimpleGUI as sg
import random
import matplotlib
import statistics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Settings
matplotlib.use("TkAgg")

# Utility functions
def runSimulation(numTimes, rarity, numRateUp, game):
	if game == "Arknights":
		return simulateArknights(numTimes, rarity, numRateUp)
	elif game == "Fate Grand/Order":
		return simulateFGO(numTimes, rarity, numRateUp)
	elif game == "Genshin Impact":
		return simulateGenshin(numTimes, rarity, numRateUp)

def decoder(game, values):
	if game == "Fate Grand/Order":
		numTimes = values['-FGONUMROLLS-']
		if numTimes == '':
			numTimes = 0
		else:
			try:
				numTimes = int(numTimes)
			except:
				return None, None, None
		if values['-FGORARE5-']:
			rarity = 5
		else:
			rarity = 4
		if values['-FGORU-']:
			if values['-FGORU1-']:
				numRateUp = 1
			else:
				numRateUp = 2
		else:
			numRateUp = 0
		return numTimes, rarity, numRateUp
	else:
		return None

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def getFigure(results):
	med = statistics.median(results)
	fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
	fig.add_subplot(111).hist(results, bins='auto', color='c', edgecolor='k', alpha=0.65)
	plt = fig.axes[0]
	plt.axvline(med, color='k', linestyle='dashed', linewidth=1)
	min_ylim, max_ylim = plt.get_ylim()
	plt.text(med*1.1, max_ylim*0.9, 'Median: {:.2f}'.format(med))
	return fig


# Simulation functions
def simulateFGO(numTimes, rarity, numRateUp):
	# Define rates
	rateUp5Star = 0.007
	rateUpSplit5Star = 0.004
	rateUp4Star = 0.015
	rateUpSplit4Star = 0.012
	normal5Star = 0.01
	normal4Star = 0.03
	
	if rarity == 5:
		if numRateUp == 0:
			rate = normal5Star
		elif numRateUp == 1:
			rate = rateUp5Star
		else:
			rate = rateUpSplit5Star
	else:
		if numRateUp == 0:
			rate = normal4Star
		elif numRateUp == 1:
			rate = rateUp4Star
		else:
			rate = rateUpSplit4Star
	results = []
	for trial in range(numTimes):
		count = 0
		while True:
			count += 1
			roll = random.random()
			if roll <= rate:
				break
		results.append(count)
	return results


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
backSet.add('-BACK0-')

menu = [[sg.Text("Which game to simulate rolls?")],
	   [sg.Button(game) for game in games],
	   [sg.Button("Exit")]]

graph = [[sg.Text("Results of Simulation")],
		 [sg.Canvas(key="-CANVAS-")],
		 [sg.Button('Save image', key='-SAVE-'), 
		  sg.Button('Back', key='-BACK0-'),
		  sg.Button('Exit', key='-EXIT-')]]

arknights = [[sg.Text("Unit rarity:")],
			[sg.Radio('6 Star', 'RADIO1', default=True, key="-ARKRARE6-"), 
			 sg.Radio('5 Star', 'RADIO1', default=False, key="-ARKRARE5-")],
			[sg.Checkbox('Rate up unit?', default=False, key="-ARKRU-")],
			[sg.Text("Number of rolls to simulate:"), sg.Input(key="-ARKNUMROLLS-")],
			[sg.Button('Go!', key='-GO2-'), sg.Button('Back', key='-BACK2-')]]

fgo = [[sg.Text("Unit rarity:")],
	  [sg.Radio('5 Star', 'RADIO2', default=True, key="-FGORARE5-"), 
	   sg.Radio('4 Star', 'RADIO2', default=False, key="-FGORARE4-")],
	  [sg.Checkbox('Rate up unit?', default=False, key="-FGORU-")],
	  [sg.Text("Number of rate up units:")],
	  [sg.Radio('1', 'RADIO3', default=True, key="-FGORU1-"), 
	   sg.Radio('2', 'RADIO3', default=False, key="-FGORU2-")],
	  [sg.Text("Number of rolls to simulate:"), sg.Input(key="-FGONUMROLLS-")],
	  [sg.Button('Go!', key='-GO3-'), sg.Button('Back', key='-BACK3-')]]

genshin = [[sg.Text("Unit rarity:")],
	 	  [sg.Radio('5 Star', 'RADIO4', default=True, key="-GIRARE5-"), 
	       sg.Radio('4 Star', 'RADIO4', default=False, key="-GIRARE4-")],
	      [sg.Checkbox('Rate up unit?', default=False, key="-GIRU-")],
	  	  [sg.Text("Number of rolls to simulate:"), sg.Input(key="-GINUMROLLS-")],
	  	  [sg.Button('Go!', key='-GO4-'), sg.Button('Back', key='-BACK4-')]]

layout = [[sg.Column(graph, visible=False, key='-COL0-'),
		   sg.Column(menu, key='-COL1-'), 
		   sg.Column(arknights, visible=False, key='-COL2-'),
		   sg.Column(fgo, visible=False, key='-COL3-'),
		   sg.Column(genshin, visible=False, key='-COL4-')]]

window = sg.Window('Gacha Simulator', layout)

currGame = None
currCol = '-COL1-'
canvas = None
while True:
    event, values = window.read()
    if event in (None, 'Exit', '-EXIT-', sg.WIN_CLOSED):
    	break
    elif event in games:
    	currGame = event
    	window[currCol].update(visible=False)
    	currCol = gamesMapping[currGame]
    	window[currCol].update(visible=True)
    elif event in backSet:
    	if canvas:
    		canvas.get_tk_widget().pack_forget()
    	currGame = None
    	window[currCol].update(visible=False)
    	window['-COL1-'].update(visible=True)
    	currCol = '-COL1-'
    elif event in goSet:
    	numTimes, rarity, numRateUp = decoder(currGame, values)
    	if numTimes:
    		results = runSimulation(numTimes, rarity, numRateUp, currGame)
    		fig = getFigure(results)
    		window[currCol].update(visible=False)
    		window['-COL0-'].update(visible=True)
    		canvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    		currCol = '-COL0-'
    	else:
    		print("Invalid input")



window.close()