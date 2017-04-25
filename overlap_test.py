from collections import Counter
import pickle


dataset_1 = '/Volumes/Shared/shared/amarcozzi/manuscript_2015_11_08/cleaned_dataset_exact_breaks_only_2015-10-29_correct_cancertype.txt'
##chr1	break1	o1	chr2	break2	o2	source	sample_name	sv_type	cancer_type

samples = {}
with open(dataset_1, 'r') as f:
	for line in f:
		if line[0] not in ['\n','#','',' ']:
			data = line.split('\t')

			chr1 = data[0]
			brk1 = int(data[1])
			o1   = data[2]
			chr2 = data[3]
			brk2 = int(data[4])
			o2   = data[5]

			src  = data[6].strip()
			sample = data[7].strip()
			sv_type = data[8].strip()
			cancer_type = data[9].strip()

			if sample not in samples:
				samples.update({sample:[]})
				
			samples[sample].append([chr1,brk1,o1,chr2,brk2,o1,src,sv_type,cancer_type])


limit = 10 #max difference in bp between an two events
to_compare = [sample for sample in samples] #list of all the samples
sim_table = Counter() #keep track of the common events among samples
duplicates = []
for sample in samples:
	to_compare.remove(sample) #do not compare with itself
	for event in samples[sample]:
		for s in to_compare:
			for e in samples[s]:
				if event[0] == e[0] and event[3] == e[3]: #it the event is in the same chromosomes
					if abs(event[1] - e[1]) <= limit and abs(event[4] - e[4]) <= limit: #if the breaks are very similar
						sim_table.update({'{}:{}'.format(sample,s)}) #count how many breaks are in common
						duplicates.append((event[0],event[1],event[3],event[4],e[0],e[1],e[3],e[4])

with open('/Volumes/Shared/shared/amarcozzi/manuscript_2015_11_08/sim_table.txt','wb') as f:
	pickle.dump(sim_table, f)
with open('/Volumes/Shared/shared/amarcozzi/manuscript_2015_11_08/samples.txt','wb') as f:
	pickle.dump(samples, f)
with open('/Volumes/Shared/shared/amarcozzi/manuscript_2015_11_08/duplicates.txt','wb') as f:
	pickle.dump(duplicates, f)
	
# total_count = 0
# for sample in sim_table.most_common():
# 	id1,id2 = sample[0].split(':')
# 	len1 = len(samples[id1])
# 	len2 = len(samples[id2])
# 	total_count += sim_table[sample[0]]
# 	print(len1,len2,sim_table[sample[0]],sample[0])