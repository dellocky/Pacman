#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <mem.h>

void maze_visualizer(int height, int width, bool flags[height][width]) //BEAUTIUL KEEP THIS, DO NOT TOUCH!!
{
   int i2 = 0;
   for (int i = 0; i < height; i++){
       printf("(");
       for (int i2 = 0; i2 < width; i2++){
       if (i2 == width -1){
       printf("%d", flags[i][i2]);
       }
       else{
       printf("%d, ", flags[i][i2]);
       }
       }
   printf(")\n");
   i2 = 0;
   }
}

void debug(int height, int width, int end_coordinate_number, bool flags[height][width], int start_coordinates[2], int end_coordinates[end_coordinate_number][2]){

   printf("Width = %d\n", width);
   printf("Height = %d\n", height);
   printf("Flag = ");
   maze_visualizer(height, width, flags);
   printf("Start Coordinates = (%d, ", start_coordinates[0]);
   printf("%d)\n", start_coordinates[1]);
   for(int i = 0; i<end_coordinate_number; i++){
   printf("End Coordinates %d", i + 1);
   printf(" = (%d, ", end_coordinates[i][0]);
   printf("%d)\n", end_coordinates[i][1]);
   }
   printf("End_coordinate_number = %d\n",  end_coordinate_number);
   } //function close tag


void path_finder(int width, int height, int end_coordinate_number, bool flags[height][width], int start_coordinates[2], int end_coordinates[end_coordinate_number][2]){
   int maze_size = width * height;
   int ***path_map = (int ***)malloc(maze_size * sizeof(int**)); //allocating space for the chain based of the side of the board
   int ***path_map_old = (int ***)malloc(maze_size * sizeof(int**)); 
   for (int i = 0; i < maze_size; i++)
   {
      path_map[i] = (int **)malloc(maze_size * sizeof(int*));
      path_map_old[i] = (int **)malloc(maze_size * sizeof(int*));
      for (int i2 = 0; i2 < maze_size; i2++)
      {
         path_map[i][i2] = (int *)malloc(2 * sizeof(int));
         path_map_old[i][i2] = (int *)malloc(2 * sizeof(int));
      }
   }
   path_map[0][0][0] = start_coordinates[0];
   path_map[0][0][1] = start_coordinates[1];
   flags[start_coordinates[1]][start_coordinates[0]] = 1;
   int path_amount = 1; //number should be the equivelent to length of first dimension
   int path_length = 1; //number should be the equivelent to length of second dimension
   int count_iteration = 0;
   int count_iteration_final = 0;
   int test_iteration = 0;
   while(true){

      for (int i1 = 0; i1 < path_amount; i1++){
      for (int i2 = 0; i2 < path_length; i2++){
         path_map_old[i1][i2][0] = path_map[i1][i2][0];
         path_map_old[i1][i2][1] = path_map[i1][i2][1];
      }
      }

      for (int i1 = 0; i1 < path_amount; i1++){
      count_iteration = 0;
      int path_new_array[4][path_length+1][2];
      int current_path[path_length][2];
      //printf("I1 = %d\n", i1);

      
      for (int i2 = 0; i2 < path_length; i2++){
         current_path[i2][0] = path_map_old[i1][i2][0];
         current_path[i2][1] = path_map_old[i1][i2][1];
      
         //printf("(%d, ", path_map[i1][i2][0]);
         //printf("%d)\n", path_map[i1][i2][1]);
       
      } //for loop close tag
      //printf("\n");
      if (path_map_old[i1][path_length - 1][0] + 1 < width && flags[path_map_old[i1][path_length - 1][1]][path_map_old[i1][path_length - 1][0] + 1] != 1)
      {
         for (int i2 = 0; i2 < path_length ; i2++){
            path_new_array[count_iteration][i2][0] = current_path[i2][0];
            path_new_array[count_iteration][i2][1] = current_path[i2][1];
         } //for loop close tag
            path_new_array[count_iteration][path_length][0] = current_path[path_length - 1][0] + 1;
            path_new_array[count_iteration][path_length][1] = current_path[path_length - 1][1];
            count_iteration += 1;
            flags[path_map_old[i1][path_length - 1][1]][path_map_old[i1][path_length - 1][0] + 1] = 1;
          
      } //if statement close tag
      if (path_map_old[i1][path_length - 1][0] - 1 >= 0 && flags[path_map_old[i1][path_length - 1][1]][path_map_old[i1][path_length - 1][0] - 1] != 1)
      {
          for (int i2 = 0; i2 < path_length ; i2++){
            path_new_array[count_iteration][i2][0] = current_path[i2][0];
            path_new_array[count_iteration][i2][1] = current_path[i2][1];
         } //for loop close tag
            path_new_array[count_iteration][path_length][0] = current_path[path_length-1][0] - 1;
            path_new_array[count_iteration][path_length][1] = current_path[path_length-1][1];
            count_iteration += 1;
            flags[path_map_old[i1][path_length - 1][1]][path_map_old[i1][path_length - 1][0] - 1] = 1; 
      } //if statement close tag
      if (path_map_old[i1][path_length - 1][1] + 1 < height && flags[path_map_old[i1][path_length - 1][1] + 1][path_map_old[i1][path_length - 1][0]] != 1)
      {
        for (int i2 = 0; i2 < path_length ; i2++){
            path_new_array[count_iteration][i2][0] = current_path[i2][0];
            path_new_array[count_iteration][i2][1] = current_path[i2][1];
         } //for loop close tag
            path_new_array[count_iteration][path_length][0] = current_path[path_length-1][0];
            path_new_array[count_iteration][path_length][1] = current_path[path_length-1][1] + 1;
            count_iteration += 1;
            flags[path_map_old[i1][path_length - 1][1] + 1][path_map_old[i1][path_length - 1][0]] = 1;
      } //if statement close tag
      if (path_map_old[i1][path_length - 1][1] - 1 >= 0 && flags[path_map_old[i1][path_length - 1][1] - 1][path_map_old[i1][path_length - 1][0]] != 1)
      {
         for (int i2 = 0; i2 < path_length ; i2++){
            path_new_array[count_iteration][i2][0] = current_path[i2][0];
            path_new_array[count_iteration][i2][1] = current_path[i2][1];
         } //for loop close tag
            path_new_array[count_iteration][path_length][0] = current_path[path_length - 1][0];
            path_new_array[count_iteration][path_length][1] = current_path[path_length - 1][1] - 1;
            count_iteration += 1;
            flags[path_map_old[i1][path_length - 1][1] - 1][path_map_old[i1][path_length - 1][0]] = 1;
            
      } //if statement close tag
            for (int i2 = 0; i2 < count_iteration; i2++){
               for (int i3 = 0; i3 < path_length + 1; i3++){
               printf("(%d, ", path_new_array[i2][i3][0]);
               printf("%d)\n", path_new_array[i2][i3][1]);
               path_map[i2 + count_iteration_final][i3][0]= path_new_array[i2][i3][0];
               path_map[i2 + count_iteration_final][i3][1]= path_new_array[i2][i3][1];
               }//nested for loop close test tag
               printf("\n");
            }//for loop close test tag
      count_iteration_final += count_iteration;
      count_iteration = 0;
      } //main for loop close tag
            
            for (int i1 = 0; i1 < count_iteration_final; i1++){
               //printf("%d = \n", i1);
               for ( int i2 = 0; i2 < path_length + 1; i2++){
               //printf("(%d, ", path_map[i1][i2][0]);
               //printf("%d)\n", path_map[i1][i2][1]);
               }
               //printf("\n");
               }
      path_length += 1;
      path_amount = count_iteration_final;
      test_iteration += 1;
      
      //printf("Clear\n");
      if (count_iteration_final == 0){
      break;
      }
      count_iteration_final = 0;
   } //main loop close tag

   free(path_map);
   free(path_map_old);
   } //function close tag


void free_array(int** array){
  free(array);
}
   
    int main(){
    //int test_coordinates[][2]= {{0, 0}, {0, 1}, {0, 2}, {1, 0}, {1, 1},{1, 2},{2, 0}, {2, 1},{2, 2}, {-1, -1}};
    int width = 4;
    int height = 3;
    bool test_flags[3][4] = {{0, 0, 0, 0}, {0, 0, 0 ,0} ,{0, 0 ,0 ,0}};
    int startpoint[2] = {2, 1};
    int endpoint[][2] = {{3, 2}};
    int endlength = 2;
    path_finder(width, height, endlength, test_flags, startpoint, endpoint);
    }
   
   

   /* 
   void path_finder(bool flags[], int start_coordinates[2], int end_coordinates[][2], int width, int height){
    int current_cascade = 0;
    int itteration_cascade = 0;
    int total_cascade = 2;
    int total_path_size = 2;
    int chain[total_cascade][total_path_size+1][2];
    //int new_chain[cascade_size][path_size][2];
    //int current_value[2] = {-1, -1};
    bool loop1 = true;
    flags[(start_coordinates[0] * width) + start_coordinates[1]] = 1;

    chain[0][0][0] = start_coordinates[0];
    chain[0][0][1] = start_coordinates[1];
    chain[0][1][0] = 2;
    chain[0][1][1] = 1;
    //termination characters
    chain[0][2][0] = -1; 
    chain[0][2][1] = -1;
    chain[1][0][0] = start_coordinates[0];
    chain[1][0][1] = start_coordinates[1];
    chain[1][1][0] = 0;
    chain[1][1][1] = 1;
    //termination characters
    chain[1][2][0] = -1; 
    chain[1][2][1] = -1;
    int test_itteration = 0;
    int **pTest = (int**) malloc(sizeof(int)*width*width*height*height*2);
 
    while (true)
    {
       //if (test_itteration == 1){
        // int test = *pTest[0][0][0];
         //printf("%d", test);
         //printf("%d",test + 1);
       //}
       //int *pTest;
       int new_chain[width*height][width*height][2];
       int i1 = 0;
       int i2 = 0;
       bool loop2 = true;
       int old_chain[width*height][width*height][2];
       if (test_itteration == 1){
         //printf("(%d, ", *pTest[itteration_cascade-1][total_path_size][0]);
         //printf("%d)\n", *pTest[itteration_cascade-1][total_path_size][1]);
       }
       //First loop duplicates the old chain values
       if (test_itteration == 0){
       while (loop2 = true)
       {
         old_chain[i1][i2][0] = chain[i1][i2][0];
         old_chain[i1][i2][1] = chain[i1][i2][1];
         //]]printf("%d", chain[i1][i2][0]);
         //printf("%d", chain[i1][i2][1]);
         //printf("%d", i1);
         //printf("%d", i2);

         if(chain[i1][i2][0] == -1 && chain[i1][i2][1] == -1)
         {
         i1 += 1;
         i2 = 0;
         }
         else
         {
         i2 += 1;
         }
         if(i1 == total_cascade)
         {
            break;
         }
       }
       }


       else{
         i1 = 0;
         i2 = 0;
         for(i1; i1 < itteration_cascade; i1++){
         for(i2; i2 < total_path_size + 1; i2++){
         old_chain[i1][i2][0] =  *pTest[(i1 * ((total_path_size+1) * 2)) + (i2 * 2)];
         //printf("(%d, ", old_chain[i1][i2][0]);
         old_chain[i1][i2][1] =  *pTest[(i1 * ((total_path_size+1) * 2)) + (i2 * 2) + 1];
         //printf("%d)\n", old_chain[i1][i2][1]);
         }
         //printf("\n");
         i2 = 0;
         }
         free(pTest);
       }
       i1 = 0;
       i2 = 0;
       total_path_size += 1;
       int new_paths[4][width*height][2];
       int current_path[width*height][2];
       itteration_cascade = 0;
       for (i1; i1 < total_cascade; i1++) //Loop through path values
         {
         i2 = 0;
         for(i2; i2 < total_path_size; i2++)
         {
            current_path[i2][0] = old_chain[i1][i2][0];
            current_path[i2][1] = old_chain[i1][i2][1];
         
            //printf("(%d, ", old_chain[i1][i2][0]);
            //printf("%d)\n", old_chain[i1][i2][1]);
         }
         i2 = 0;
         if(current_path[total_path_size-2][0] + 1 < width){
         if(flags[current_path[total_path_size-2][0] + (current_path[total_path_size-2][1] * width) + 1] == 0)
         {  
            //printf("Flag 1!\n");
            for (int i3 = 0; i3 < total_path_size ; i3++)
            { //loop through the path
            new_paths[current_cascade][i3][0] = current_path[i3][0];
            new_paths[current_cascade][i3][1] = current_path[i3][1];
            }
            // add the new coordinate
            new_paths[current_cascade][total_path_size - 1][0] = new_paths[current_cascade][total_path_size - 2][0] + 1;
            new_paths[current_cascade][total_path_size - 1][1] = new_paths[current_cascade][total_path_size - 2][1];
            // add the terminator char
            new_paths[current_cascade][total_path_size][0] = -1;
            new_paths[current_cascade][total_path_size][1] = -1;
            current_cascade += 1;

         }
         }
         if(current_path[total_path_size-2][0] - 1 >= 0){
         if(flags[current_path[total_path_size-2][0] + (current_path[total_path_size-2][1] * width) - 1] == 0)
         {  
            //printf("Flag 2!\n");
            for (int i3 = 0; i3 < total_path_size ; i3++)
            { //loop through the path
            new_paths[current_cascade][i3][0] = current_path[i3][0];
            new_paths[current_cascade][i3][1] = current_path[i3][1];
            }
            // add the new coordinate
            new_paths[current_cascade][total_path_size - 1][0] = new_paths[current_cascade][total_path_size - 2][0] - 1;
            new_paths[current_cascade][total_path_size - 1][1] = new_paths[current_cascade][total_path_size - 2][1];
            // add the terminator char
            new_paths[current_cascade][total_path_size][0] = -1;
            new_paths[current_cascade][total_path_size][1] = -1;
            current_cascade += 1;
         }
         }
         if(current_path[total_path_size-2][1] + 1 < height){
         if(flags[current_path[total_path_size-2][0] + (current_path[total_path_size-2][1] * width) + width] == 0)
         {  
            //printf("Flag 3!\n");
            for (int i3 = 0; i3 < total_path_size ; i3++)
            { //loop through the path
            new_paths[current_cascade][i3][0] = current_path[i3][0];
            new_paths[current_cascade][i3][1] = current_path[i3][1];
            }
            // add the new coordinate
            new_paths[current_cascade][total_path_size - 1][0] = new_paths[current_cascade][total_path_size - 2][0];
            new_paths[current_cascade][total_path_size - 1][1] = new_paths[current_cascade][total_path_size - 2][1] + 1;
            // add the terminator char
            new_paths[current_cascade][total_path_size][0] = -1;
            new_paths[current_cascade][total_path_size][1] = -1;
            current_cascade += 1;
         }
         }
         if(current_path[total_path_size-2][1] - 1 >= 0){
         if(flags[current_path[total_path_size-2][0] + (current_path[total_path_size-2][1] * width) - width] == 0)
         { 
            //printf("Flag 4!\n");
            for (int i3 = 0; i3 < total_path_size ; i3++)
            { //loop through the path
            new_paths[current_cascade][i3][0] = current_path[i3][0];
            new_paths[current_cascade][i3][1] = current_path[i3][1];
            }
            // add the new coordinate
            new_paths[current_cascade][total_path_size - 1][0] = new_paths[current_cascade][total_path_size - 2][0];
            new_paths[current_cascade][total_path_size - 1][1] = new_paths[current_cascade][total_path_size - 2][1] - 1;
            // add the terminator char
            new_paths[current_cascade][total_path_size][0] = -1;
            new_paths[current_cascade][total_path_size][1] = -1;
            current_cascade += 1;
         }
         }

         /*
         //TEST FOR LOOP
         if (test_itteration ==1) {
         i2 = 0;
         int i3 = 0;
            for (i2; i2 < current_cascade; i2++){
               for (i3; i3 < total_path_size + 1; i3++){
               printf("(%d, ", new_paths[i2][i3][0]);
               printf("%d)\n", new_paths[i2][i3][1]);
               }
               i3 = 0;
               printf("\n");
               }
         }
         /star
      
         i2 = 0;
         int i3 = 0;
            for (i2; i2 < current_cascade; i2++){
               for (i3; i3 < total_path_size + 1; i3++){
               printf("(%d, ",  new_paths[i2][i3][0]);
               printf("%d)\n",  new_paths[i2][i3][1]);
               new_chain[i2+itteration_cascade][i3][0] = new_paths[i2][i3][0];
               new_chain[i2+itteration_cascade][i3][1] = new_paths[i2][i3][1];
               }
               i3 = 0;
               printf("\n");
               }

      itteration_cascade += current_cascade;
      current_cascade = 0;

      //total_cascade += current_cascade;
      }
      i2 = 0;
      int i3 = 0;
            for (i2; i2 < itteration_cascade; i2++){
               for (i3; i3 < total_path_size + 1; i3++){
               printf("(%d, ", new_chain[i2][i3][0]);
               printf("%d)\n", new_chain[i2][i3][1]);
               pTest[(i2 * ((total_path_size+1) * 2)) + (i3 * 2)] = &new_chain[i2][i3][0];
               pTest[(i2 * ((total_path_size+1) * 2)) + (i3 * 2) + 1] = &new_chain[i2][i3][1];
               }
               printf("\n");
               i3 = 0;
               }

      total_cascade += itteration_cascade;
      test_itteration += 1;
      i2 = 0;
      i3 = 0;
      
      /*
      for (i2; i2 < itteration_cascade * (total_path_size + 1) * 2; i2++){
                  printf("(%d, ", *pTest[i2]);
                  i2++;
                  printf("%d)\n", *pTest[i2]);
                  }
                  
      star/
      
      if (test_itteration != 1){
      break;
      }
      }
    }
    */