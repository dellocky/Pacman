from os import walk

def Normalize(file, path):
    num_list = []
    count_lines = 0
    with open(file) as mapfile:
        for line in mapfile:
            count_lines += 1
            reader = line.split(",")
            for I in reader:
                I = int(I.rstrip())
                num_list.append(I)

    for __,__,img_files  in walk(path):
        count_images = 1
        for image in img_files:
            count_images += 1
         
    init_num = -1  
    for I in range(count_images):
        for num in num_list:
            if init_num not in num_list:
                pass#test 
        
                
            
           

Normalize("Map Layout/PacMan Layout_Walls.csv", "gagag")

    