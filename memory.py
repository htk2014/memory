import sys, pygame ,os, spritesheet,time,random,copy

size = width, height = 1800, 1800

cards = pygame.sprite.Group()

class Card(pygame.sprite.Sprite):
	
	def __init__(self,ss,x,y):

		def allocate(x,y):
			pos = (x+10*y)
			self.mark = pos/13
			self.number = pos % 13 + 1

		pygame.sprite.Sprite.__init__(self,cards)

                front_image = ss.image_at((48 * x, 64 * y, 48, 64))
                back_image = ss.image_at((48 * 3,64 * 5, 48, 64))
		
                self.width = 80
                self.height = 110

		self.front_image = pygame.transform.scale(front_image,(self.width,self.height)) 
		self.back_image = pygame.transform.scale(back_image,(self.width,self.height)) 

		self.image = self.back_image
		self.rect = self.image.get_rect() 

		allocate(x,y)
		
	def turn(self):
		if self.image == self.front_image:
			self.image = self.back_image
		else: self.image = self.front_image
class Text:
	def __init__(self,text,location):
		basic_font = pygame.font.SysFont(None, 48)

		self.text = basic_font.render(text,True,(255, 0 , 0),(255, 255, 255))
		self.location = location

	def draw(self,screen):
		screen.blit(self.text,self.location)

	
class Memory:

	def __init__(self):
		pygame.init()
		self.black = 0, 0, 0
		self.card_lst = []
		
		self.player_number = 0
		self.cpu_number = 0

		self.screen = pygame.display.set_mode(size)
		
	def makeCards(self,ss):

		for j in range(0,6):
			for i in range(0,10):
				if (j*10+i) <= 51:
       		 			Card(ss,i,j)

		for card in cards:
			self.card_lst.append(card) 

		random.shuffle(self.card_lst)

		for j in range(0,5):
			for i in range(0,13):
				if (j*13+i) <= 51:
					card = self.card_lst[j*13+i]  
					card.rect.topleft = [50+48*i+i*card.width,50+64*j+j*card.height]				

	def selectCard(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.MOUSEBUTTONUP: 
					pos = pygame.mouse.get_pos()
				#turn card	
					for card in cards:	
						if card.rect.collidepoint(pos):
							card.turn()

							return card
	def player(self):
		card1 = self.selectCard()
		cards.draw(self.screen)
		pygame.display.flip()

		card2 = self.selectCard()
		cards.draw(self.screen)
		pygame.display.flip()


		if card1.number == card2.number:
			cards.remove(card1)
			cards.remove(card2)
			self.player_number += 2

		else:	
			card1.turn()
			card2.turn()


	def cpu(self):

		copy_cards = copy.copy(self.card_lst)

		card1 = copy_cards[random.choice(range(len(copy_cards)))]
		card1.turn()
		cards.draw(self.screen)
		pygame.display.flip()
		time.sleep(0.5)

		copy_cards.remove(card1)

		card2 = copy_cards[random.choice(range(len(copy_cards)))]
		card2.turn()
		cards.draw(self.screen)
		pygame.display.flip()
		time.sleep(1)


		if card1.number == card2.number:
			cards.remove(card1)
			cards.remove(card2)
			self.cpu_number += 2

		else:	
			card1.turn()
			card2.turn()


	def _run(self):
	
		ss = spritesheet.spritesheet('../img/trump.png')
	        self.makeCards(ss)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
		
			self.screen.fill(self.black)
				
			text1 = Text('player '+str(self.player_number),[800,800])
			text1.draw(self.screen)

			text2 = Text('cpu '+str(self.cpu_number),[800,850])
			text2.draw(self.screen)


			cards.draw(self.screen)

			pygame.display.flip()
	
			self.player()	
			time.sleep(1)
			self.cpu()	

			if cards == False:
				break
def main():
	while 1:
        	Memory()._run()

main()
