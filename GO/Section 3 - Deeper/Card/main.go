package main

func main() {
	// cards := newDeck()
	// hand, remainingCard := deal(cards, 5)
	// hand.print()
	// remainingCard.print()
	// cards.saveToFile("MyFile")
	newCards := newDeckFormFIle("MyFile")
	newCards.shuffle()
	newCards.print()
}
