import pygame
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__() 
        img = pygame.image.load(filename).convert_alpha()
        self.original_image = pygame.Surface((60, 60))
        self.original_image.blit(img, img.get_rect(center = self.original_image.fill((127, 127, 127)).center))
        self.hover_image = pygame.Surface((60, 60))
        self.hover_image.blit(img, img.get_rect(center = self.hover_image.fill((228, 228, 228)).center))
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = (x, y))
        self.hover = False

    def update(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        self.image = self.hover_image if self.hover else self.original_image
	
class Level(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__() 
        img = pygame.image.load(filename).convert_alpha()
        self.original_image = pygame.Surface((70, 70))
        self.original_image.blit(img, img.get_rect(center = self.original_image.fill((127, 127, 127)).center))
        self.hover_image = pygame.Surface((70, 70))
        self.hover_image.blit(img, img.get_rect(center = self.hover_image.fill((228, 228, 228)).center))
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = (x, y))
        self.hover = False

    def update(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        self.image = self.hover_image if self.hover else self.original_image	