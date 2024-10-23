class SpriteGroup(list):
    def __init__(self, name, *args):
        super().__init__(*args)
        self.name = name
    
    def update(self):
        for num, sprite in enumerate(self):
            sprite.update()
    

    


        

        
            



        