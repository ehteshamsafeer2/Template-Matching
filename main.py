import cv2 
import numpy as np
import random
import matplotlib.pyplot as plt

group_img = cv2.imread("groupGray.jpg")
baba_img = cv2.imread("babaG.jpg")

group_arr = np.array(group_img)
baba_arr = np.array(baba_img)
baba_dimen = baba_img.shape
rows = baba_dimen[0]
cols = baba_dimen[1]
threshold = 0.8
plot_fitness = []
plot_avg = []

def current_generation(group_rows,group_columns,population_size):	
	print("Step 1")
	row = []
	column = []
	for i in range(population_size):
		row.append(random.randint(0,group_rows-baba_dimen[0]))
		column.append(random.randint(0,group_columns-baba_dimen[1]))
	return tuple(zip(row, column)) 
first_gen = current_generation(512,1024,100)

def correlation_coefficient(patch1, patch2):
    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product
	
def image_fetch(r,c):
	r_end = r +  rows
	c_end = c + cols
	fetch_img = group_img[r:r_end,c:c_end]
	if fetch_img.shape != baba_dimen:
		return group_img[0:35,0:29]
	return fetch_img

def fitness_eval(current_generation, bari_img, choti_img):
	print("Step 2")
	
	fitness_level = []
	print("T	e	s	t	i	n	g",current_generation)
	for i in current_generation:
		sample = image_fetch(i[0],i[1])
		corr = correlation_coefficient(sample, choti_img)
		fitness_level.append(corr)
#	print(fitness_level,"\n",len(fitness_level))
	return fitness_level

def selection(curr_gen, fitness_level):
	print("Step 3")
	zipped_lists = zip(fitness_level, curr_gen)
	sorted_pairs = sorted(zipped_lists)
	avg = sum(fitness_level)/len(fitness_level)
	plot_avg.append(avg)
	tuples = zip(*sorted_pairs)
	fitness_level, curr_gen = [ list(tuple) for tuple in  tuples]
	keys = curr_gen
			#	print(curr_gen)
#	print(fitness_level)
#	values = fitness_level[0]
	last_key = keys[-1]
	last_value = fitness_level[-1]
	plot_fitness.append(last_value)
	if last_value >= threshold:
		fitness_arr = np.array(plot_fitness)
		plt.plot(fitness_arr, label="Fitness Values")
		plt.plot(plot_avg, label="Avg")
		plt.legend()
		plt.show()
		r = last_key[0]
		c = last_key[1]
		cv2.rectangle(img=group_img, pt1=(c,r), pt2=(c+29,r+35), color=(0,0,255), thickness=1)
		cv2.imshow("babaG",group_img)
		cv2.waitKey(0)
		exit()
	return keys	

def new_generation(curr_gen,group_rows,group_cols):
	print("Step 4")
	parent_list = []
	new_gen = ()
	for parents in curr_gen:
		p = str(format(parents[0], "09b")) + str(format(parents[1], "010b"))
		parent_list.append(p)
	
	i=0
	j=1
	st = False
	while st==False:
		if j > 100:
			break;
		p1 = parent_list[i]
		p2 = parent_list[j]
		cut = random.randint(0,19)
		p1_c = p1[:cut]+p2[cut:]
		p2_c = p2[:cut]+p1[cut:] 
	
		p1_row = int(p1_c[:9],2)			
		p1_column = int(p1_c[9:],2)
		p2_row = int(p2_c[:9],2)
		p2_column = int(p2_c[9:],2)
		new_gen = new_gen+((p1_row,p1_column),(p2_row,p2_column))
		i+=2
		j+=2
	print(len(new_gen),)
	return new_gen
a = 1
st = False
fitness_lev = fitness_eval(first_gen,group_img,baba_img)
s = selection(first_gen, fitness_lev)
new = new_generation(s,512,1024)
while st==False:
    a+=1
    fitness = fitness_eval(new,group_img,baba_img)
    curr2 = selection(new, fitness)
    new = new_generation(curr2,512,1024)
    print("Generation:", a)