# encoding=UTF-8
#import jieba
import argparse
import csv
import time

if __name__ == '__main__':
    # You should not modify this part.    
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()

    # Please implement your algorithm below
    
    # TODO load source data, build search engine
    dict = {}
    cache = {}
    with open(args.source, 'r') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            try: 
                dict[row[1]].append(row[0])
            except:
                dict[row[1]] = [row[0]]
    print("build search engine --- %s seconds ---" % (time.time() - start_time))        
    start_time = time.time()
    # TODO compute query result
    #jieba.set_dictionary('dict.txt.big.txt')
    querys = []    
    with open(args.query, 'r') as csvfile:
        data = csv.reader(csvfile)
        querys = sum(list(data), [])
    
    # TODO output result
    with open(args.output, 'w') as output_file:
        for i in range(len(querys)):
            result = querys[i].split()
            
            if(len(result) == 3):
                try:
                    a = cache[result[0]]
                except:
                    a = [value for key, value in dict.items() if result[0] in key]
                    a = sum(a, [])
                    cache[result[0]] = a
                
                try:
                    b = cache[result[2]]
                except:
                    b = [value for key, value in dict.items() if result[2] in key]                       
                    b = sum(b, [])
                    cache[result[2]] = b
    
                if(result[1] == 'and'):
                    ans = list(set(a) & set(b))
                elif(result[1] == 'or'):
                    ans = list(set(a) | set(b))
                elif(result[1] == 'not'):
                    ans = list(set(a) - (set(a) & set(b)))
            
            elif(len(result) == 5):
                try:
                    a = cache[result[0]]
                except:
                    a = [value for key, value in dict.items() if result[0] in key]
                    a = sum(a, [])
                    cache[result[0]] = a
                
                try:
                    b = cache[result[2]]
                except:
                    b = [value for key, value in dict.items() if result[2] in key]                       
                    b = sum(b, [])
                    cache[result[2]] = b
                    
                try:
                    c = cache[result[4]]
                except:
                    c = [value for key, value in dict.items() if result[4] in key]                       
                    c = sum(c, [])
                    cache[result[4]] = c
                
                if(result[1] == 'and'):
                    tmp = set(a) & set(b)
                elif(result[1] == 'or'):
                    tmp = set(a) | set(b)
                elif(result[1] == 'not'):
                    tmp = set(a) - (set(a) & set(b))
            
                if(result[3] == 'and'):
                    ans = tmp & set(c)
                elif(result[3] == 'or'):
                    ans = tmp | set(c)
                elif(result[3] == 'not'):
                    ans = tmp - (tmp & set(c))

            
            if len(ans) == 0:
                output_file.write("0")
            else:
                output_file.write(str(','.join(sorted(ans,  key=lambda x: int(x)))))
    
            if i != len(querys) - 1:
                output_file.write("\n")
                
    print("query --- %s seconds ---" % (time.time() - start_time))
