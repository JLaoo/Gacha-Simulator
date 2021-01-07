import PySimpleGUI as sg
import random
import os
import glob
import matplotlib
import statistics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Settings
matplotlib.use("TkAgg")

# Utility functions
def runSimulation(limited, numTimes, rarity, numRateUp, game):
	if game == "Arknights":
		return simulateArknights(limited, numTimes, rarity, numRateUp)
	elif game == "Fate Grand/Order":
		return simulateFGO(numTimes, rarity, numRateUp)
	elif game == "Genshin Impact":
		return simulateGenshin(limited, numTimes, rarity)

def decoder(game, values):
	if game == "Fate Grand/Order":
		numTimes = values['-FGONUMROLLS-']
		if numTimes == '':
			numTimes = 0
		else:
			try:
				numTimes = int(numTimes)
			except:
				return None, None, None, None
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
		return None, numTimes, rarity, numRateUp
	elif game == "Arknights":
		numTimes = values['-ARKNUMROLLS-']
		if numTimes == '':
			numTimes = 0
		else:
			try:
				numTimes = int(numTimes)
			except:
				return None, None, None, None
		if values['-ARKRARE6-']:
			rarity = 6
		else:
			rarity = 5
		if values['-ARKRU-']:
			if values['-ARKRU1-']:
				numRateUp = 1
			elif values['-ARKRU2-']:
				numRateUp = 2
			else:
				numRateUp = 3
		else:
			numRateUp = 0
		if values['-ARKLI-']:
			limited = True
		else:
			limited = False
		return limited, numTimes, rarity, numRateUp
	elif game == 'Genshin Impact':
		numTimes = values['-GINUMROLLS-']
		if numTimes == '':
			numTimes = 0
		else:
			try:
				numTimes = int(numTimes)
			except:
				return None, None, None, None
		if values['-GIRARE5-']:
			rarity = 5
		else:
			rarity = 4
		if values['-GIRU-']:
			limited = True
		else:
			limited = False
		return limited, numTimes, rarity, None

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def getFigure(results):
	med = statistics.median(results)
	fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
	fig.add_subplot(111).hist(results, bins=30, color='c', edgecolor='k', alpha=0.65, density=True)
	plt = fig.axes[0]
	plt.axvline(med, color='k', linestyle='dashed', linewidth=1)
	min_ylim, max_ylim = plt.get_ylim()
	min_xlim, max_xlim = plt.get_xlim()
	plt.text(max_xlim*0.7, max_ylim*0.9, 'Median: {:.2f}'.format(med))
	plt.set_title('Results of {} simulations'.format(len(results)))
	return fig

def saveImage(figure, game):
	if game == 'Arknights':
		abbrev = 'AK'
	elif game == 'Fate Grand/Order':
		abbrev = 'FGO'
	elif game == 'Genshin Impact':
		abbrev = 'GI'
	if not os.path.isdir('savedImages'):
		os.makedirs('savedImages')
	currImages = glob.glob('savedImages/*.png')
	count = 0
	for file in currImages:
		if abbrev in file:
			count += 1
	figure.savefig('savedImages/{}{}.png'.format(abbrev, str(count)))


# Simulation functions
def simulateArknights(limited, numTimes, rarity, numRateUp):
	# Ignore guaranteed 5* or 6* in first 10 rolls (no idea how it works)
	sixStar = 0.02
	fiveStar = 0.08

	results = []
	if rarity == 5:
		if numRateUp == 0:
			rate = fiveStar
		elif numRateUp == 1:
			rate = fiveStar / 2
		elif numRateUp == 2:
			rate = fiveStar / 4
		else:
			rate = fiveStar / 6
		for trial in range(numTimes):
			count = 0
			while True:
				count += 1
				roll = random.random()
				if roll <= rate:
					break
			results.append(count)
		return results
	else:
		for trial in range(numTimes):
			pityCount = 0
			count = 0
			currRate = sixStar
			while True:
				count += 1
				if limited and count == 300:
					break
				pityCount += 1
				if pityCount > 50:
					currRate += 0.02
				roll = random.random()
				if roll <= currRate:
					if numRateUp == 0:
						break
					if not limited:
						roll = random.random()
						if roll <= 0.5 / numRateUp:
							break
						else:
							currRate = sixStar
							pityCount = 0
					else:
						roll = random.random()
						if roll <= 0.7 / numRateUp:
							break
						else:
							currRate = sixStar
							pityCount = 0
			results.append(count)
		return results

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

def simulateGenshin(limited, numTimes, rarity):
	# Define rates
	fiveStar = 0.006
	fourStar = 0.051

	if rarity == 5:
		rate = fiveStar
		pity = 90
	else:
		rate = fourStar
		pity = 10
	results = []
	if limited:
		for trial in range(numTimes):
			firstHit = True
			count = 0
			pityCount = 0
			while True:
				count += 1
				pityCount += 1
				if pityCount == pity:
					if firstHit:
						roll = random.random()
						if roll <= 0.5:
							break
						firstHit = False
						pityCount = 0
					else:
						break
				roll = random.random()
				if roll <= rate:
					if firstHit:
						roll = random.random()
						if roll <= 0.5:
							break
						firstHit = False
						pityCount = 0
					else:
						break
			results.append(count)
	else:
		for trial in range(numTimes):
			count = 0
			while True:
				count += 1
				if count == pity:
					break
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
			[sg.Text("Number of rate up units:")],
	  		[sg.Radio('1', 'RADIO5', default=True, key="-ARKRU1-"), 
	   		 sg.Radio('2', 'RADIO5', default=False, key="-ARKRU2-"),
	   		 sg.Radio('3', 'RADIO5', default=False, key="-ARKRU3-")],
	   		[sg.Checkbox('Limited unit?', default=False, key="-ARKLI-")],
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
	      [sg.Checkbox('Limited Banner?', default=False, key="-GIRU-")],
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
    	limited, numTimes, rarity, numRateUp = decoder(currGame, values)
    	if numTimes:
    		results = runSimulation(limited, numTimes, rarity, numRateUp, currGame)
    		fig = getFigure(results)
    		window[currCol].update(visible=False)
    		window['-COL0-'].update(visible=True)
    		canvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    		currCol = '-COL0-'
    	else:
    		print("Invalid input")
    elif event == '-SAVE-':
    	saveImage(fig, currGame)

window.close()