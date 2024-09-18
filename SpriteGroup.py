class SpriteGroup(list):
    def __init__(self, *args):
        super().__init__(*args)
        for arg, val in  enumerate(args):
            print(f"{val} = {arg}")
    
    def update(self):
        for num, sprite in enumerate(self):
            sprite.update()
    

    


        

        
            



        