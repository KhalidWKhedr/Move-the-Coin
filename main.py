import fnmatch
import tkinter as tk
import time
import bresenham
import time
import sys
import tkinter.font as fnt
import os

global gameGraph, nodes, currentNode, totalScore, computerTurnFlag, humanStartedFlag, restartPlay, exitPlay
global guaranteedNodesScores, humanWinAdjustedNodesScores, statusMsg1, statusMsg2, newGame, statusMsg3
restartPlay = False
newGame = False
exitPlay = False
# **********************
# For the GUI
# **********************
global Ball_Start_XPosition, Ball_Start_YPosition, Ball_Radius, Ball_min_movement
global Refresh_Sec, NumberOfFrames, rectangleWidth, rectangleHeight, window, canvas, clickedNode, label4
global ball, ballCurrentPosition, VarInput, playPtn, playStarted, choice1, choice2, label3, label2, replayPtn
global exitPtn


def initGlobalVariables():
    global gameGraph, nodes, currentNode, totalScore, computerTurnFlag, humanStartedFlag, playStarted, exitPlay
    global guaranteedNodesScores, humanWinAdjustedNodesScores, statusMsg1, statusMsg2, choice1, choice2, newGame
    global statusMsg3
    currentNode = 'Start'
    totalScore = 0
    playStarted = False
    computerTurnFlag = True
    humanStartedFlag = False
    guaranteedNodesScores = []
    humanWinAdjustedNodesScores = []
    choice1 = '1'
    choice2 = '2'
    statusMsg1 = "Choose if you want to be the starter"
    statusMsg2 = "   then press START/PLAY to begin the game"
    statusMsg3 = " "


def initGuiSettingVariables():
    global Ball_Start_XPosition, Ball_Start_YPosition, Ball_Radius, Ball_min_movement
    global Refresh_Sec, ballCurrentPosition, NumberOfFrames, rectangleWidth, rectangleHeight
    global window, canvas
    # Ball_Start_XPosition = 250
    # Ball_Start_YPosition = 60
    Ball_Radius = 10  # 17
    Ball_min_movement = 2
    Refresh_Sec = 0.01
    # ballCurrentPosition = [0, 0]
    NumberOfFrames = 60
    rectangleWidth = 40  # 80
    rectangleHeight = 30  # 60


def drawGui():
    global window, canvas, ball, ballCurrentPosition, VarInput, playStarted, playPtn, choice1, choice2
    global statusMsg1, statusMsg2, label3, label2, restartPlay, replayPtn, exitPtn, statusMsg3, label4
    if not restartPlay:
        initGuiSettingVariables()
        window = tk.Tk()
        window.geometry("700x800")
        window.configure(background='light sky blue')
        window.title("Moving The Coin")
        label1 = tk.Label(window, text="Moving The Coin...Let's see who wins", fg="black", bg="light sky blue",
                          font=("Comic Sans MS", 14))
        label1.pack()
        canvas = tk.Canvas(window, width=600, height=620)
        canvas.pack()  # fill=tk.BOTH, expand=True
        # draw all nodes and getting the center (x,y) from the nodes dictionary
        for nds in nodes:
            recCenter = nodes.get(nds)
            # print("=" + str(nodes.get(nds)))
            drawNode(recCenter, nds)
        # draw all links, get the links and connect valued from gameGraph
        for begNode in gameGraph.keys():  # draw all links, get the links and connect valued from gameGraph
            fromRecCenter = nodes.get(begNode)
            # print(gameGraph.get(row))
            for link in gameGraph.get(begNode):
                endNode = link[0]
                linkText = link[1]
                toRecCenter = nodes.get(endNode)
                drawLink(fromRecCenter, toRecCenter, linkText)
        # draw the ball in the start position
        ballRecCenter = nodes.get('Start')
        ballCurrentPosition = ballRecCenter
        ball = canvas.create_oval(ballCoordInRectangle(ballRecCenter)[0] - Ball_Radius,
                                  ballCoordInRectangle(ballRecCenter)[1] + Ball_Radius,
                                  ballCoordInRectangle(ballRecCenter)[0] + Ball_Radius,
                                  ballCoordInRectangle(ballRecCenter)[1] - Ball_Radius,
                                  fill="pale violet red", outline="maroon", width=2)
        # draw the different buttons
        frame = tk.Frame(window)
        frame.pack()
        VarInput = tk.StringVar(window, '1')
        choice1 = tk.Radiobutton(frame, text="Machine starts", variable=VarInput, value='1', font=fnt.Font(size=10),
                                 height=1, background='light sky blue')
        choice1.pack(side=tk.LEFT, anchor="w", padx=3, pady=1)
        choice2 = tk.Radiobutton(frame, text="Human starts", variable=VarInput, value='2', font=fnt.Font(size=10),
                                 height=1, background='light sky blue')
        choice2.pack(side=tk.LEFT, anchor="w", padx=3, pady=1)
        playPtn = tk.Button(frame, text='START/PLAY', command=playButtonPressed, height=1, font=fnt.Font(size=10),
                            background='deep sky blue')
        playPtn.pack(side=tk.LEFT, padx=3, pady=1)
        replayPtn = tk.Button(frame, text='RESTART', command=replayButtonPressed, height=1, font=fnt.Font(size=10),
                              background='deep sky blue')
        replayPtn.pack(side=tk.LEFT, padx=3, pady=1)
        replayPtn.config(relief=tk.SUNKEN)
        replayPtn['state'] = tk.DISABLED
        exitPtn = tk.Button(frame, text='EXIT', command=quitGame, height=1, font=fnt.Font(size=10),
                            background='deep sky blue')
        exitPtn.pack(side=tk.LEFT, padx=3, pady=1)
        # exitPtn.config(relief=tk.SUNKEN)
        # exitPtn['state'] = tk.DISABLED
        # display two lines of status messages
        frame2 = tk.Frame(window)
        label2 = tk.Label(frame2, text=statusMsg1, fg="black", bg="beige",
                          font=("Comic Sans MS", 10))
        frame2.pack()
        label2.pack()
        label3 = tk.Label(frame2, text=statusMsg2, fg="black", bg="beige",
                          font=("Comic Sans MS", 10))
        label3.pack()
        label4 = tk.Label(frame2, text=statusMsg3, fg="black", bg="beige",
                          font=("Comic Sans MS", 10))
        label4.pack()
        canvas.bind('<Button-1>', getCoordinates)
    else:
        move_ball(nodes.get(currentNode))
        window.update_idletasks()
        window.update()


def getCoordinates(event):
    global clickedNode
    for nds in nodes:  # Find which node was pressed
        recCenter = nodes.get(nds)
        nodeX = recCenter[0]
        nodeY = recCenter[1]
        marginPixels = int(int(rectangleWidth / 2))
        if ((nodeX - marginPixels <= event.x <= nodeX + marginPixels) and
                (nodeY - marginPixels <= event.y <= nodeY + marginPixels)):
            # print("You pressed Node= " + nds)
            clickedNode = nds


def playButtonPressed():
    global VarInput, humanStartedFlag, playStarted, choice1, choice2, computerTurnFlag
    choice = VarInput.get()
    if choice == '1':
        humanStartedFlag = False
        computerTurnFlag = True
    else:
        humanStartedFlag = True
        computerTurnFlag = False
    playStarted = True
    print("Play/Start Button Pressed with choice: humanStartedFlag= " + str(humanStartedFlag))
    playPtn.config(relief=tk.SUNKEN)
    playPtn['state'] = tk.DISABLED
    exitPtn.config(relief=tk.SUNKEN)
    exitPtn['state'] = tk.DISABLED


def quitGame():
    global exitPlay
    print("Exit Button Pressed")
    exitPlay = True


def replayButtonPressed():
    global playStarted, replayPtn, restartPlay, exitPtn
    print("Restart Button Pressed")
    playStarted = False
    restartPlay = True
    playPtn.config(relief=tk.RAISED)
    playPtn['state'] = tk.ACTIVE
    # choice1['state'] = tk.ACTIVE
    # choice2['state'] = tk.ACTIVE
    replayPtn.config(relief=tk.SUNKEN)
    replayPtn['state'] = tk.DISABLED
    exitPtn.config(relief=tk.RAISED)
    exitPtn['state'] = tk.ACTIVE


def ballCoordInRectangle(rectangleCenter):
    centerX = rectangleCenter[0] - int(rectangleWidth / 2) + Ball_Radius - 9
    centerY = rectangleCenter[1] + int(rectangleHeight / 2) - Ball_Radius + 9
    return [centerX, centerY]


def drawLink(fromCenter, toCenter, linkText):
    fromX = fromCenter[0]
    fromY = fromCenter[1] + int(rectangleHeight / 2)
    toX = toCenter[0]
    toY = toCenter[1] - int(rectangleHeight / 2)
    canvas.create_line(fromX, fromY, toX, toY, fill="brown", arrow=tk.LAST, width=1)
    midX = (fromX + toX) / 2
    midY = (fromY + toY) / 2
    midX = (midX + toX) / 2
    midY = (midY + toY) / 2
    canvas.create_text(midX, midY, font=("Purisa", 12), text=linkText, fill="Black")


def drawNode(rectangleCenter, nodeLabel):
    global canvas
    canvas.create_rectangle(
        rectangleCenter[0] - int(rectangleWidth / 2),
        rectangleCenter[1] - int(rectangleHeight / 2),
        rectangleCenter[0] + int(rectangleWidth / 2),
        rectangleCenter[1] + int(rectangleHeight / 2),
        outline="brown",
        fill="beige")
    canvas.create_text(rectangleCenter[0], rectangleCenter[1], font=("Purisa", 12), text=nodeLabel, fill="Black")


def move_ball(x_y_coord):
    global ballCurrentPosition, canvas, window, ballCurrentPosition
    x = x_y_coord[0]
    y = x_y_coord[1]
    movePointsList = list(bresenham.bresenham(ballCurrentPosition[0], ballCurrentPosition[1], x, y))
    interval = max(int(len(movePointsList) / NumberOfFrames), 1)
    for i in range(0, len(movePointsList), interval):
        # print (str(l[0]-Ball_XPosition)+" "+str(l[1]-Ball_YPosition))
        xinc = movePointsList[i][0] - ballCurrentPosition[0]
        yinc = movePointsList[i][1] - ballCurrentPosition[1]
        canvas.move(ball, xinc, yinc)
        ballCurrentPosition = [movePointsList[i][0], movePointsList[i][1]]
        window.update()
        time.sleep(Refresh_Sec)


def buildGameGraph():
    global gameGraph, nodes
    nodes = {}
    gameGraph = {}
    with open(os.path.join(sys.path[0], 'config.txt'), "r") as f:
        sc = f.readlines()
        nodesCount = int(sc.__getitem__(0))
        nodeNameArrTokens = sc[1: nodesCount + 1]
        connectionTokens = sc[nodesCount + 1:]
        for i, nodeName in enumerate(nodeNameArrTokens):
            check_nodes = str.split(nodeName.rstrip())
            nodeName = check_nodes[0]
            nodeX = int(check_nodes[1])
            nodeY = int(check_nodes[2])
            if nodeName in nodes.keys():
                raise Exception("Error in Configuration file, node repeats more than once")
            nodes[nodeName] = [nodeX, nodeY]
        for i, nodeName in enumerate(connectionTokens):
            check_nodes = str.split(nodeName.rstrip())
            startNode = check_nodes[0]
            endNode = check_nodes[1]
            connectValue = int(check_nodes[2])
            if startNode not in nodes.keys() or endNode not in nodes.keys():
                raise Exception("There is an error in the connection information.")
            if startNode in gameGraph.keys():
                listConnections = gameGraph.get(startNode)
                listConnections.append([endNode, connectValue])
                gameGraph[startNode] = listConnections
            else:
                gameGraph[startNode] = [[endNode, connectValue]]


def getHumanNextNode(currNode):  # this function inputs the user next tile,
    global clickedNode
    # then verifies it and then returns the tile name and the connection value for this tile
    connectionNodes = gameGraph.get(currNode)
    hashSearch = {connectionNodes[i][0]: connectionNodes[i] for i in range(0, len(connectionNodes))}  # get the
    # results in another dictionary
    # nextNode = input("Enter the next node name you want to move to: ")
    clickedNode = ""
    returnValue = hashSearch.get(clickedNode)
    while returnValue is None:
        # nextNode = input("Wrong connection, try again:: ")
        time.sleep(0.2)
        window.update_idletasks()
        window.update()
        returnValue = hashSearch.get(clickedNode)
    return returnValue


def askHumanStartsFirst():
    global humanStartedFlag, computerTurnFlag
    startFirstResponse = input("Do you want to start first (Y/N): ")
    while startFirstResponse not in ('Y', 'y', 'N', 'n'):
        startFirstResponse = input("Do you want to start first (Y/N): ")
    if startFirstResponse in ('Y', 'y'):
        humanStartedFlag = True
        computerTurnFlag = False
    else:
        humanStartedFlag = False
        computerTurnFlag = True


def askHumanPlayAgain():
    global restartPlay, exitPlay, window, canvas
    restartPlay = False
    exitPtn.config(relief=tk.RAISED)
    replayPtn.config(relief=tk.RAISED)
    exitPtn['state'] = tk.ACTIVE
    replayPtn['state'] = tk.ACTIVE
    while not (exitPlay or restartPlay):
        time.sleep(0.2)
        window.update_idletasks()
        window.update()
    if restartPlay:
        restartPlay = True
    else:
        window.destroy()
        exit(0)


def gameEnded():
    if fnmatch.fnmatch(currentNode, "End*"):
        return True
    else:
        return False


def humanMakesOneMove():
    global currentNode, totalScore
    humanNextMove = getHumanNextNode(currentNode)
    currentNode = humanNextMove[0]
    totalScore = totalScore + humanNextMove[1]


def computerMakesOneMove():
    global currentNode, totalScore, humanWinAdjustedNodesScores
    computeNextMoves()
    currentNode = humanWinAdjustedNodesScores[0][0]  # pick the solution with the lowest score computed for humans
    totalScore = totalScore + humanWinAdjustedNodesScores[0][2]


def updateScreenStatus():
    global statusMsg1, statusMsg2, label2, label3, playStarted, statusMsg3, label4
    if humanStartedFlag:
        msg1 = ", You (human) started the game."
    else:
        msg1 = ", Computer started the game."
    ####
    statusMsg1 = "Current Node= " + currentNode + ", Total Score= " + str(totalScore) + msg1
    print(statusMsg1)
    ####
    if gameEnded():
        if (humanStartedFlag and totalScore % 2 == 1) or (not humanStartedFlag and totalScore % 2 == 0):
            statusMsg2 = "Congratulations, you (human) won"
            print(statusMsg2)
        else:
            statusMsg2 = "Sorry, I (the computer) won, good luck next time"
            print(statusMsg2)
        statusMsg3 = "Press RESTART to play again or press EXIT to close the game"
        print(statusMsg3)
        label2.config(text=statusMsg1)
        label3.config(text=statusMsg2)
        label4.config(text=statusMsg3)
        return
    ####
    if not playStarted:
        statusMsg1 = "Choose if you want to be the starter"
        statusMsg2 = "then click the START/PLAY button to play"
        statusMsg3 = ""
        label2.config(text=statusMsg1)
        label3.config(text=statusMsg2)
        label4.config(text=statusMsg3)
        return
    ####
    if computerTurnFlag:
        statusMsg2 = "It's Computer Turn now. Watch the move."
        print(statusMsg2)
    else:
        print(statusMsg2)
        statusMsg2 = "It's your turn now. Click your next Tile."
        print(statusMsg2)
    label2.config(text=statusMsg1)
    label3.config(text=statusMsg2)
    label4.config(text=statusMsg3)


def computeNextMoves():
    global computerTurnFlag
    global totalScore
    global currentNode
    global guaranteedNodesScores, humanWinAdjustedNodesScores
    guaranteedNodesScores = []
    humanWinAdjustedNodesScores = []
    for nodeLink in gameGraph.get(currentNode):
        # print(computerTurnFlag)
        winScore = checkNodeIsWinnable(nodeLink[0], totalScore, nodeLink[1], computerTurnFlag)
        guaranteedNodesScores.append([nodeLink[0], winScore, nodeLink[1]])
        winScore = checkNodeHumanMinScore(nodeLink[0], totalScore, nodeLink[1], computerTurnFlag)
        humanWinAdjustedNodesScores.append([nodeLink[0], winScore[0] * winScore[1], nodeLink[1]])
    print("Guaranteed Computer moves (values with score = 1): " + str(guaranteedNodesScores))
    print("Computed Computer Next Moves= " + str(humanWinAdjustedNodesScores))
    humanWinAdjustedNodesScores.sort(key=mySortKey)
    print("Computed Computer Moves Sorted on Scores, lower score is better= " + str(humanWinAdjustedNodesScores))


def mySortKey(e):
    return e[1]


def checkNodeIsWinnable(moveToNode, previousNodeScore, moveGainValue, compTurnFlag):
    currNodeScore = previousNodeScore + moveGainValue
    if fnmatch.fnmatch(moveToNode, "End*"):
        if humanStartedFlag and currNodeScore % 2 == 1:
            return 0
        if not humanStartedFlag and currNodeScore % 2 == 1:
            return 1
        if humanStartedFlag and currNodeScore % 2 == 0:
            return 1
        if not humanStartedFlag and currNodeScore % 2 == 0:
            return 0
        raise Exception("Code should not be here [1]")
    for nodeLink in gameGraph.get(moveToNode):  # looping on all possible children nodes in next level
        returnResult = checkNodeIsWinnable(nodeLink[0], currNodeScore, nodeLink[1], compTurnFlag ^ True)
        if compTurnFlag:  # if it is the computer turn, return 0 once one of the children nodes made by humans returns 0
            if returnResult == 0:
                return 0
        else:  # when it is the human turn
            if returnResult == 1:  # it is human turn, return 1 once one of the next computer moves return 1
                return 1
    if compTurnFlag:
        return 1  # We are here because no numan moves that happened after, returned a zero
    else:
        return 0  # We are here because no computer moves that happened after, returned a 1


def checkNodeHumanMinScore(moveToNode, previousNodeScore, moveGainValue, compTurnFlag):
    SumOfDepthAdjustFactor = float(0)
    SumOfScoreTimesDepthFactor = float(0)
    minDepthAdjustedScore = float(100)
    maxDepthAdjustedScore = float(0)
    newDepthAdjustFactor = float(1)
    newScore = float(0)
    # print("entry node being processed= " + moveToNode)
    currNodeScore = previousNodeScore + moveGainValue
    if fnmatch.fnmatch(moveToNode, "End*"):
        if humanStartedFlag and currNodeScore % 2 == 1:
            return [1, 4]
        if not humanStartedFlag and currNodeScore % 2 == 1:
            return [0, 1]
        if humanStartedFlag and currNodeScore % 2 == 0:
            return [0, 1]
        if not humanStartedFlag and currNodeScore % 2 == 0:
            return [1, 4]
        raise Exception("Code should not be here [2]")
    for nodeLink in gameGraph.get(moveToNode):  # looping on all possible children nodes in next level
        # print("child node being processed= " + nodeLink[0] + ", turn= " + str(compTurnFlag))
        functionReturn = checkNodeHumanMinScore(nodeLink[0], currNodeScore, nodeLink[1], compTurnFlag ^ True)
        # print("function return= " + str(functionReturn))
        scoreResult = functionReturn[0]
        depthAdjustFactor = functionReturn[1]
        if compTurnFlag:
            # if it is the computer turn, human makes a choice next, and we compute adjusted combined human win score
            SumOfDepthAdjustFactor = SumOfDepthAdjustFactor + depthAdjustFactor
            SumOfScoreTimesDepthFactor = SumOfScoreTimesDepthFactor + depthAdjustFactor * scoreResult
            if depthAdjustFactor * scoreResult > maxDepthAdjustedScore:
                maxDepthAdjustedScore = depthAdjustFactor * scoreResult
                newDepthAdjustFactor = depthAdjustFactor  # get the biggest depthAdjustFactor value
        else:  # when it is the human turn, computer makes choice next, computer chooses the minimum score & depthFactor
            if minDepthAdjustedScore > depthAdjustFactor * scoreResult:  # get the minimum value
                minDepthAdjustedScore = depthAdjustFactor * scoreResult
                newScore = scoreResult  # pick the minimum score value
                newDepthAdjustFactor = depthAdjustFactor  #
                # get the newDepthAdjustFactor that is associated with minimum value of depthAdjustFactor * scoreResult
    if compTurnFlag:
        newScore = SumOfScoreTimesDepthFactor / SumOfDepthAdjustFactor
    newDepthAdjustFactor = max(1.0, newDepthAdjustFactor / 2.0)
    # print("final results for = " + moveToNode + ", Computer Turn= " + str(compTurnFlag))
    # print([moveToNode, newScore, newDepthAdjustFactor])
    return [round(newScore, 2), newDepthAdjustFactor]


def humanStartsOrExitsTheGame():
    global playStarted, exitPlay
    playStarted = False
    ############################################
    while not (playStarted or exitPlay):
        time.sleep(0.3)
        window.update_idletasks()
        window.update()
    ############################################
    if exitPlay:
        print("Exit Requested")
        exitPlay = True
    elif playStarted:
        print("play Start Requested")
        playStarted = True
    else:
        raise Exception("something wrong happened")
    ############################################
    updateScreenStatus()
    window.update_idletasks()
    window.update()


if __name__ == '__main__':
    ######################
    buildGameGraph()
    initGlobalVariables()
    drawGui()
    ######################
    while not exitPlay:
        humanStartsOrExitsTheGame()
        ############################################
        while not (gameEnded() or exitPlay):  # if game ended, announce the winner end exit the first while loop
            updateScreenStatus()
            window.update_idletasks()
            window.update()
            if computerTurnFlag:
                time.sleep(1)
                computerMakesOneMove()
            else:
                humanMakesOneMove()
            computerTurnFlag = computerTurnFlag ^ True  # alternate play
            move_ball(nodes.get(currentNode))
        ############################################
        updateScreenStatus()
        askHumanPlayAgain()
        initGlobalVariables()
        drawGui()
        updateScreenStatus()
