from tkinter import *
from GetRankAndFiveCards import returnRank, suitList
import tkinter.font as tkFont

root = Tk()
root.title('Poker Cards')
root.geometry("1500x1000")

UTFCardList = [
    ['🃂', '🃃', '🃄', '🃅', '🃆', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎', '🃁'],
    ['🃒', '🃓', '🃔', '🃕', '🃖', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞', '🃑'],
    ['🂲', '🂳', '🂴', '🂵', '🂶', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾', '🂱'],
    ['🂢', '🂣', '🂤', '🂥', '🂦', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮', '🂡']
]

cardFontStyle = tkFont.Font(size=128)

bodyFrame = LabelFrame(root)
bodyFrame.pack()

valueList = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

sevenCardList = []

cardObjectList = []


def updateCardLabel(card):
    if card.cardButtonVariable.get() == 0:
        card.rankAndSuitCanvas.configure(bg=card.cardColor)

        card.rankAndSuitCanvas.itemconfig(card.rankAndSuitText, fill="white")

        sevenCardList.append(card.rankAndSuitID)

        card.cardButtonVariable.set(1)
    elif card.cardButtonVariable.get() == 1:
        card.rankAndSuitCanvas.configure(bg="white")

        card.rankAndSuitCanvas.itemconfig(
            card.rankAndSuitText, fill=card.cardColor)

        sevenCardList.remove(card.rankAndSuitID)

        card.cardButtonVariable.set(0)


class Card:
    def __init__(self, theFrame, rankAndSuit, rankAndSuitID, gridRow, gridCol, cardColor, haveButton):
        self.rankAndSuit = rankAndSuit
        self.gridRow = gridRow
        self.gridCol = gridCol
        self.rankAndSuitID = rankAndSuitID

        self.cardButtonVariable = IntVar()
        self.cardButtonVariable.set(0)

        self.cardColor = cardColor

        cardFrame = LabelFrame(theFrame)
        cardFrame.grid(row=gridRow, column=gridCol)

        self.rankAndSuitCanvas = Canvas(cardFrame, bg='white')
        self.rankAndSuitCanvas.grid(row=0, column=0)
        self.rankAndSuitText = self.rankAndSuitCanvas.create_text(
            5, -29, text=rankAndSuit, fill=cardColor, font=cardFontStyle, anchor='nw')
        bbox = self.rankAndSuitCanvas.bbox(self.rankAndSuitText)
        self.rankAndSuitCanvas.configure(width=bbox[2], height=bbox[3]-16)

        if haveButton:
            cardButton = Button(
                cardFrame, text="select", font="bold", command=lambda: updateCardLabel(self))
            cardButton.grid(row=1, column=0, ipadx=10)

    def __str__(self):
        return self.rankAndSuitID

    __repr__ = __str__


for i, (card, cardID) in enumerate(zip(UTFCardList[0], valueList)):
    cardObjectList.append(
        Card(bodyFrame, card, [cardID, "D"], 0, i, "red", True))

for i, (card, cardID) in enumerate(zip(UTFCardList[1], valueList)):
    cardObjectList.append(
        Card(bodyFrame, card, [cardID, "C"], 1, i, "black", True))

for i, (card, cardID) in enumerate(zip(UTFCardList[2], valueList)):
    cardObjectList.append(
        Card(bodyFrame, card, [cardID, "H"], 2, i, "red", True))

for i, (card, cardID) in enumerate(zip(UTFCardList[3], valueList)):
    cardObjectList.append(
        Card(bodyFrame, card, [cardID, "S"], 3, i, "black", True))

footerFrame = LabelFrame(root)
footerFrame.pack()

# create the window to display the results
resultWindow = Toplevel()
resultWindow.title("result")
resultWindow.geometry("1000x1000")

# this ensure that it starts at top but spawns top down
resultWindowFrame = LabelFrame(resultWindow)
resultWindowFrame.pack()

fiftyTwoCardsList = []

for suit in suitList:
    for value in valueList:
        fiftyTwoCardsList.append([value, suit])


def returnUTFCard(rankAndSuit):
    UTFCardIndex = 51

    for i, card in enumerate(fiftyTwoCardsList):
        if card[0] == rankAndSuit[0] and card[1] == rankAndSuit[1]:
            UTFCardIndex = i

    fullUTF = UTFCardList[0] + UTFCardList[1] + UTFCardList[2] + UTFCardList[3]
    return fullUTF[UTFCardIndex]


class ResultFrameClass:
    resultFrameClassList = []

    def __init__(self, sevenCardList, resultRankText):

        self.resultFrame = LabelFrame(resultWindowFrame)
        self.resultFrame.pack(side=BOTTOM)

        handList = []

        resultRank = Label(self.resultFrame, text=resultRankText)
        resultRank.grid(row=0, column=0)

        for i, card in enumerate(sevenCardList):
            cardColor = "black" if card[1] == "S" or card[1] == "C" else "red"
            handList.append(Card(
                self.resultFrame, returnUTFCard(card), card, 0, i+1, cardColor, False))


def showRankNFiveCards():
    print(sevenCardList)
    temp = returnRank(sevenCardList)

    rankText = ""

    if temp[0] == 1:
        rankText = "1. High Card"
    if temp[0] == 2:
        rankText = "2. Pair"
    if temp[0] == 3:
        rankText = "3. 2 Pair"
    if temp[0] == 4:
        rankText = "4. 3 of a Kind"
    if temp[0] == 5:
        rankText = "5. Straight"
    if temp[0] == 6:
        rankText = "6. Flush"
    if temp[0] == 7:
        rankText = "7. Full House"
    if temp[0] == 8:
        rankText = "8. Four of a Kind"
    if temp[0] == 9:
        rankText = "9. Straight Flush"

    print(f"{rankText}  {temp[1]}\n\n")

    ResultFrameClass.resultFrameClassList.append(
        ResultFrameClass(temp[1], rankText))

    if len(ResultFrameClass.resultFrameClassList) >= 6:
        ResultFrameClass.resultFrameClassList[0].resultFrame.pack_forget()
        del ResultFrameClass.resultFrameClassList[0]


def clear():
    for card in cardObjectList:
        if card.cardButtonVariable.get() == 1:
            card.rankAndSuitCanvas.configure(bg="white")
            card.rankAndSuitCanvas.itemconfig(
                card.rankAndSuitText, fill=card.cardColor)

            sevenCardList.remove(card.rankAndSuitID)
            # delete later
            print(sevenCardList)

            card.cardButtonVariable.set(0)


getRankNFiveCardsBtn = Button(
    root, text="Get Rank and Five Cards", command=showRankNFiveCards)
getRankNFiveCardsBtn.pack()

clearBtn = Button(
    root, text="clear", command=clear)
clearBtn.pack()

root.mainloop()
