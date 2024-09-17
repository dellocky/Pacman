class SpriteGroup(list):
    def __init__(self, *args) -> None:
        self.sprite_list = []
        for sprite in args:
            if type(sprite) is list:
                self.sprite_list += sprite
            else:
                self.sprite_list.append(sprite)

    def add(self, *args):
    
        for sprite in args:
            if type(sprite) is list:
                self.sprite_list += sprite
            else:
                self.sprite_list.append(sprite)
    
    def update(self):
        for sprite in self.sprite_list:
            sprite.update()
    

        

        
            



        