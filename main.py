import sys, pygame ,os, spritesheet,time,random,copy,numpy

size = width, height = 840, 580
black = 0, 0, 0

cards = pygame.sprite.Group()

class Card(pygame.sprite.Sprite):
	
	def __init__(self,ss,x,y):

		pygame.sprite.Sprite.__init__(self,cards)

                front_image = ss.image_at((48 * x, 64 * y, 48, 64))
                back_image = ss.image_at((48 * 3,64 * 5, 48, 64))
		
                self.width = 50
                self.height = 75

		self.front_image = pygame.transform.scale(front_image,(self.width,self.height)) 
		self.back_image = pygame.transform.scale(back_image,(self.width,self.height)) 

		self.image = self.back_image
		self.rect = self.image.get_rect() 

		pos = (x+10*y)
		self.mark = pos/13
		self.number = pos % 13 + 1
		
	def turn(self):
		if self.image == self.front_image:
			self.image = self.back_image
		else: self.image = self.front_image
class Text:

	def __init__(self,text,location):
		self.basic_font = pygame.font.SysFont(None, 48)
		self.text = self.basic_font.render(text,True,(255, 0 , 0),(255, 255, 255))
		self.location = location
	
	def update(self,text):
		self.text = self.basic_font.render(text,True,(255, 0 , 0),(255, 255, 255))

	def draw(self,screen):
		screen.blit(self.text,self.location)


class GamePlayer:

	def __init__(self,name,screen,textLocation):
		self.screen = screen
		self.cardCount = 0
		self.name = name
		self.text = Text(self.name+':'+str(self.cardCount),textLocation)
		#for first drawing in main functon
		self.text.draw(self.screen)

	def selectFirst(self):
		pass

	def selectSecond(self,firstCard):
		pass

	def play(self):
           	self.text.draw(self.screen)
		
		successFlag = False

		card1 = self.selectFirst()
		card2 = self.selectSecond(card1)
		#success                
		if card1.number == card2.number:
			cards.remove(card1)
			cards.remove(card2)

			self.cardCount += 2

			#update and draw text
			self.screen.fill(black)
                        self.text.update(self.name +':'+str(self.cardCount))
            		self.text.draw(self.screen)

			successFlag = True
		#fail
		else:	
			card1.turn()
			card2.turn()

            	cards.draw(self.screen)

	    	pygame.display.update()

     	        if  cards.sprites() == []:
                        sys.exit()

		if successFlag:
			self.play()
			
class human(GamePlayer):

	def __init__(self,name,screen):
		GamePlayer.__init__(self,name,screen,[500,400])

	def selectCard(self,first_card):
		#until player select card
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.MOUSEBUTTONUP: 
					pos = pygame.mouse.get_pos()
				#turn card	
					for card in cards:	
						if card.rect.collidepoint(pos) and not(first_card == card):
							card.turn()
							return card
	def selectFirst(self):
		card = self.selectCard(False)
		#draw card
            	cards.draw(self.screen)
	    	pygame.display.update()

		return card

	def selectSecond(self,firstCard):
		card = self.selectCard(firstCard)
		#draw card
		cards.draw(self.screen)
	    	pygame.display.update()

		time.sleep(0.5)
		
		return card

class computer(GamePlayer):

	def __init__(self,name,screen):
		GamePlayer.__init__(self,name,screen,[500,450])

	def selectFirst(self):
		card_array = numpy.asarray(cards.sprites())
		card_index = random.choice(range(len(card_array)))

		card = card_array[card_index]

		card.turn()
		cards.draw(self.screen)
		pygame.display.update()

		time.sleep(0.5)
		
		return card

	def selectSecond(self,firstCard):
		card_list = cards.sprites()
		card_list.remove(firstCard)

		card_array = numpy.asarray(card_list)
		card_index = random.choice(range(len(card_array)))

		card = card_array[card_index]
		card.turn()

		cards.draw(self.screen)
		pygame.display.update()
		time.sleep(0.5)

		return card

def initCards(ss):
	for j in range(0,6):
		for i in range(0,10):
			if (j*10+i) <= 51:
       	 			Card(ss,i,j)

	cardLst = []

	for card in cards:
		cardLst.append(card) 

	random.shuffle(cardLst)

	for j in range(0,5):
		for i in range(0,13):
			if (j*13+i) <= 51:
				cardLst[j*13+i].rect.topleft = [25+48*i+i*card.width/5,25+64*j+j*card.height/4]				
def main():
	pygame.init()
	screen = pygame.display.set_mode((width,height))

	player = human('player',screen)
	cpu = computer('cpu',screen)

	ss = spritesheet.spritesheet('./img/trump.png')
	initCards(ss)

	while 1:
		for event in pygame.event.get():
                	if event.type == pygame.QUIT: sys.exit()

		cards.draw(screen)
		pygame.display.update()

            	player.play()	
            	time.sleep(0.3)
            	cpu.play()	
            	time.sleep(0.5)

main()
