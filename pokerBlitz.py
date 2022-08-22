from tkinter import *
from GetRankAndFiveCards import returnRank, suitList, returnValueHandLists
import random
import tkinter.font as tkFont

root = Tk()
root.title('Poker Cards')
root.geometry("750x750")

UTFCardList = [
    ['🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎', '🃁'],
    ['🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞', '🃑'],
    ['🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾', '🂱'],
    ['🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮', '🂡']
]

valueList = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

cardFontStyle = tkFont.Font(size=128)
textFontStyle = tkFont.Font(size=32)


def generateNineCardsList():
    fiftyTwoCardsList = []

    # consider pictures with numbers
    for value in valueList:
        for suit in suitList:
            fiftyTwoCardsList.append([value, suit])

    random.shuffle(fiftyTwoCardsList)
    shuffled = list(fiftyTwoCardsList)

    return(shuffled[0:9])


def generateHands(nineCardList):
    communityCardList = nineCardList[0:5]

    leftPrivateList = nineCardList[7:9]

    rightPrivateList = nineCardList[5:7]

    leftHandList = leftPrivateList + communityCardList

    rightHandList = rightPrivateList + communityCardList

    return leftHandList, rightHandList, leftPrivateList, rightPrivateList, communityCardList


class CardClass:
    def __init__(self, handFrame, cardID, gridCol):
        self.handFrame = handFrame
        self.cardID = cardID

        cardFrame = LabelFrame(handFrame)
        cardFrame.grid(row=0, column=gridCol)

        cardText = ""
        cardColor = ""

        if cardID[1] == "D":
            for rank, UTFCard in zip(valueList, UTFCardList[0]):
                if rank == cardID[0]:
                    cardText = UTFCard
                    cardColor = "red"

        if cardID[1] == "C":
            for rank, UTFCard in zip(valueList, UTFCardList[1]):
                if rank == cardID[0]:
                    cardText = UTFCard
                    cardColor = "black"

        if cardID[1] == "H":
            for rank, UTFCard in zip(valueList, UTFCardList[2]):
                if rank == cardID[0]:
                    cardText = UTFCard
                    cardColor = "red"

        if cardID[1] == "S":
            for rank, UTFCard in zip(valueList, UTFCardList[3]):
                if rank == cardID[0]:
                    cardText = UTFCard
                    cardColor = "black"

        self.rankAndSuitCanvas = Canvas(cardFrame, bg='white')
        self.rankAndSuitCanvas.grid(row=0, column=0)
        self.rankAndSuitText = self.rankAndSuitCanvas.create_text(
            5, -29, text=cardText, fill=cardColor, font=cardFontStyle, anchor='nw')
        bbox = self.rankAndSuitCanvas.bbox(self.rankAndSuitText)
        self.rankAndSuitCanvas.configure(width=bbox[2], height=bbox[3]-16)


timeLimit = True


def rankConvertValue(rank):
    RCVRankList = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    RCVValueList = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    return RCVValueList[RCVRankList.index(rank)]


class GameClass:
    gameScore = IntVar()
    gameScore.set(0)

    gameStatus = StringVar()

    gameOver = False

    def __init__(self, leftHandList, rightHandList, leftPrivateList, rightPrivateList, communityCardList):
        self.leftHandList = leftHandList
        self.rightHandList = rightHandList
        self.leftPrivateList = leftPrivateList
        self.rightPrivateList = rightPrivateList
        self.communityCardList = communityCardList

        self.biggerHand = ""

        leftHandRankAndFiveCards, rightHandRankAndFiveCards = returnRank(
            self.leftHandList), returnRank(self.rightHandList)

        print(f"community: {communityCardList}\n")
        print(
            f"left: {leftPrivateList}   {self.returnRankText(leftHandRankAndFiveCards[0])} {leftHandRankAndFiveCards[1]} \nright: {rightPrivateList}   {self.returnRankText(rightHandRankAndFiveCards[0])} {rightHandRankAndFiveCards[1]}\n")

        if leftHandRankAndFiveCards[0] > rightHandRankAndFiveCards[0]:
            print("leftbigger")
            self.biggerHand = "left"
        elif rightHandRankAndFiveCards[0] > leftHandRankAndFiveCards[0]:
            print("rightbigger")
            self.biggerHand = "right"

        # below ensure wheel straight is smaller than other straights, the below has not been tested
        elif rightHandRankAndFiveCards[0] == 5 and leftHandRankAndFiveCards[0] == 5:
            if all(elem in returnValueHandLists(rightHandRankAndFiveCards[1]) for elem in [14, 2, 3, 4, 5]) and all(elem in returnValueHandLists(leftHandRankAndFiveCards[1]) for elem in [14, 2, 3, 4, 5]):
                print("draw")
                self.biggerHand = "draw"
            elif all(elem in returnValueHandLists(rightHandRankAndFiveCards[1]) for elem in [14, 2, 3, 4, 5]):
                print("leftbigger")
                self.biggerHand = "left"
            elif all(elem in returnValueHandLists(leftHandRankAndFiveCards[1]) for elem in [14, 2, 3, 4, 5]):
                print("rightbigger")
                self.biggerHand = "right"
            else:
                for leftCard, rightCard in zip(leftPrivateList, rightPrivateList):
                    if rankConvertValue(leftCard[0]) > rankConvertValue(rightCard[0]):
                        print("leftbigger")
                        self.biggerHand = "left"
                        break
                    elif rankConvertValue(rightCard[0]) > rankConvertValue(leftCard[0]):
                        print("rightbigger")
                        self.biggerHand = "right"
                        break
                    else:
                        print("draw")
                        self.biggerHand = "draw"
                        break
        else:
            for leftCard, rightCard in zip(leftPrivateList, rightPrivateList):
                if rankConvertValue(leftCard[0]) > rankConvertValue(rightCard[0]):
                    print("leftbigger")
                    self.biggerHand = "left"
                    break
                elif rankConvertValue(rightCard[0]) > rankConvertValue(leftCard[0]):
                    print("rightbigger")
                    self.biggerHand = "right"
                    break
                else:
                    print("draw")
                    self.biggerHand = "draw"
                    break

        print("\n\n")

        self.loadDisplay()

        # insertIntoFrame for various cardlist

    def loadDisplay(self):
        self.gameScoreLabel = Label(
            root, text=f"Score: {GameClass.gameScore.get()} {GameClass.gameStatus.get()}", font=textFontStyle)
        self.gameScoreLabel.grid(row=0, column=0, columnspan=3)

        self.communityFrame = LabelFrame(root)
        self.communityFrame.grid(row=1, column=0, columnspan=3)

        self.leftHandFrame = LabelFrame(root)
        self.leftHandFrame.grid(row=2, column=0)

        self.leftHandButton = Button(
            root, text="left", font=textFontStyle, command=lambda: self.clickButton("left"))
        self.leftHandButton.grid(row=3, column=0)

        self.drawHandButton = Button(
            root, text="draw", font=textFontStyle, command=lambda: self.clickButton("draw"))
        self.drawHandButton.grid(row=3, column=1)

        self.rightHandFrame = LabelFrame(root)
        self.rightHandFrame.grid(row=2, column=2)

        self.rightHandButton = Button(
            root, text="right", font=textFontStyle, command=lambda: self.clickButton("right"))
        self.rightHandButton.grid(row=3, column=2)

        self.insertIntoFrame(self.communityFrame, self.communityCardList)
        self.insertIntoFrame(self.leftHandFrame, self.leftPrivateList)
        self.insertIntoFrame(self.rightHandFrame, self.rightPrivateList)

    def forgetDisplay(self):
        self.gameScoreLabel.grid_forget()
        self.communityFrame.grid_forget()
        self.leftHandFrame.grid_forget()
        self.leftHandButton.grid_forget()
        self.drawHandButton.grid_forget()
        self.rightHandFrame.grid_forget()
        self.rightHandButton.grid_forget()

    def returnRankText(self, rank):
        rankText = ""
        if rank == 1:
            rankText = "High Card"
        if rank == 2:
            rankText = "Pair"
        if rank == 3:
            rankText = "2 Pair"
        if rank == 4:
            rankText = "3 of a Kind"
        if rank == 5:
            rankText = "Straight"
        if rank == 6:
            rankText = "Flush"
        if rank == 7:
            rankText = "Full House"
        if rank == 8:
            rankText = "Four of a Kind"
        if rank == 9:
            rankText = "Straight Flush"

        return rankText

    def clickButton(self, clickedBtn):
        if clickedBtn == self.biggerHand:
            self.forgetDisplay()
            GameClass.gameScore.set(GameClass.gameScore.get()+1)
            leftHandList, rightHandList, leftPrivateList, rightPrivateList, communityCardList = generateHands(
                generateNineCardsList())
            GameClass(leftHandList, rightHandList, leftPrivateList,
                      rightPrivateList, communityCardList)
        else:
            self.gameScoreLabel.grid_forget()
            GameClass.gameStatus.set("Game Over")
            self.gameScoreLabel = Label(
                root, text=f"Score: {GameClass.gameScore.get()} {GameClass.gameStatus.get()}", font=textFontStyle)
            self.gameScoreLabel.grid(row=0, column=0, columnspan=3)
            self.drawHandButton.grid_forget()
            self.leftHandButton.grid_forget()
            self.rightHandButton.grid_forget()

            GameClass.gameOver = True

    def insertIntoFrame(self, handFrame, cardList):
        print("he")
        for i, card in enumerate(cardList):
            CardClass(handFrame, card, i)


print("hello")
leftHandList, rightHandList, leftPrivateList, rightPrivateList, communityCardList = generateHands(
    generateNineCardsList())
GameClass(leftHandList, rightHandList, leftPrivateList,
          rightPrivateList, communityCardList)


root.mainloop()
