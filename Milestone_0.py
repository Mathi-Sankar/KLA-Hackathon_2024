import json

def make_list():
    global step_list
    step_list = {}
    global free 
    free = {}
    for s in json_decode['steps']:
        step_list[s['id']] = []

    for m in json_decode['machines']:
        step_list[m['step_id']].append(m['machine_id'])
        free[m['step_id']] = m['machine_id']
    return free

def count_quantity():
    total = 0
    for w in json_decode['wafers']:
        total = total + w['quantity']
    return total

def create_string():
    stri = []
    for w in json_decode['wafers']:
        for i in range(w['quantity']):
            for s in w['processing_times']:
                if(s == 'S1'):
                    val = 0
                else:
                    val = 1
                stri.append(str(w['type'] + "-" + str(i) + '-' + str(val)))
    return stri

def main():
    input_file=open('C:/Workshop_Problem/MilestoneInputs/Input/Milestone0.json', 'r')
    output_file=open('C:/Workshop_Problem/Milestones_output/Output_1.json', 'w')
    global json_decode
    json_decode = json.load(input_file)
   
    count = count_quantity()
    str_list = create_string()
    w = [0,0]
    m = [0,0]
    i = 0
    dictt = {'schedule' : []}

    #print(json_decode['wafers'][0]['processing_times'])
    while str_list:
        dictt2 = {}
        for s in str_list:
            ss = s.split('-')
            w_need = int(ss[1])
            m_need = int(ss[2])
            if(w[w_need] <= i and m[m_need] <= i):
                dictt2 = {}
                #print(f"w1-{w_need+1}, S{m_need+1}, {max(m[m_need],w[w_need])}, {max(m[m_need],w[w_need]) + json_decode['wafers'][0]['processing_times']['S'+ str(m_need + 1)]}")
                #dicts['schedule'].append()
                dictt2['wafer_id'] = 'W' + '1' + '-' + str(w_need + 1)
                #print(str(w_need + 1))
                dictt2['step'] = "S" + str(m_need + 1)
                dictt2['machine'] = "M" + str(m_need + 1)
                dictt2['start_time'] = int(max(m[m_need],w[w_need]))
                dictt2['end_time'] = int(max(m[m_need],w[w_need]) + json_decode['wafers'][0]['processing_times']['S'+ str(m_need + 1)])

                dictt['schedule'].append(dictt2)
                print(dictt)
                w[w_need] = w[w_need] +  int(json_decode['wafers'][0]['processing_times']['S'+ str(w_need + 1)])              
                m[m_need] = m[m_need] +  int(json_decode['wafers'][0]['processing_times']['S'+ str(m_need + 1)])    
                #print(s)
                str_list.remove(s)   
        i = i+1

    json_object = json.dumps(dictt, indent=4)
 
    with open("C:\Workshop_Problem\Milestones_output\Output_1.json", "w") as outfile:
        outfile.write(json_object)
 





main()