import json

def make_lists(json_decode):
    step_list = {s['id']: [] for s in json_decode['steps']}
    free = {m['step_id']: m['machine_id'] for m in json_decode['machines']}

    for m in json_decode['machines']:
        step_list[m['step_id']].append(m['machine_id'])
    
    return step_list, free

def count_quantity(json_decode):
    return sum(w['quantity'] for w in json_decode['wafers'])

def create_strings(json_decode):
    return [f"{w['type']}-{i}-{0 if s == 'S1' else 1}"
            for w in json_decode['wafers']
            for i in range(w['quantity'])
            for s in w['processing_times']]

def main():
    input_file_path = 'C:/Workshop_Problem/MilestoneInputs/Input/Milestone1.json'
    output_file_path = 'C:/Workshop_Problem/Milestones_output/Output_1.json'
    
    with open(input_file_path, 'r') as input_file:
        json_decode = json.load(input_file)
    
    step_list, free = make_lists(json_decode)
    total_quantity = count_quantity(json_decode)
    str_list = create_strings(json_decode)
    
    w = [0] * total_quantity
    m = [0] * total_quantity
    i = 0
    schedule = []

    while str_list:
        for s in str_list[:]:
            wafer_id, wafer_index, step_index = s.split('-')
            w_need, m_need = int(wafer_index), int(step_index)
            
            if w[w_need] <= i and m[m_need] <= i:
                start_time = max(m[m_need], w[w_need])
                end_time = start_time + json_decode['wafers'][0]['processing_times'][f'S{m_need + 1}']
                
                schedule.append({
                    'wafer_id': f'W1-{w_need + 1}',
                    'step': f'S{m_need + 1}',
                    'machine': f'M{m_need + 1}',
                    'start_time': start_time,
                    'end_time': end_time
                })
                
                w[w_need] += json_decode['wafers'][0]['processing_times'][f'S{m_need + 1}']
                m[m_need] += json_decode['wafers'][0]['processing_times'][f'S{m_need + 1}']
                str_list.remove(s)

        i += 1

    json_object = json.dumps({'schedule': schedule}, indent=4)

    with open(output_file_path, 'w') as output_file:
        output_file.write(json_object)

main()
