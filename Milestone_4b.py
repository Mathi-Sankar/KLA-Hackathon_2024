import json

def make_lists(json_decode):
    step_list = {s['id']: [] for s in json_decode['steps']}
    step_dependencies = {s['id']: s['dependency'] for s in json_decode['steps']}
    for m in json_decode['machines']:
        step_list[m['step_id']].append(m['machine_id'])
    return step_list, step_dependencies

def count_quantity(json_decode):
    return sum(w['quantity'] for w in json_decode['wafers'])

def create_strings(json_decode):
    return [f"{w['type']}-{i}-{s[1:]}"
            for w in json_decode['wafers']
            for i in range(w['quantity'])
            for s in w['processing_times']]

def main():
    input_file_path = 'C:/Workshop_Problem/MilestoneInputs/Input/Milestone4b.json'
    output_file_path = 'C:/Workshop_Problem/Milestones_output/Output_4b.json'
    
    with open(input_file_path, 'r') as input_file:
        json_decode = json.load(input_file)
    
    step_list, step_dependencies = make_lists(json_decode)
    total_quantity = count_quantity(json_decode)
    str_list = create_strings(json_decode)
    
    w = [0] * total_quantity
    m = [0] * total_quantity
    i = 0
    schedule = []

    completed_steps = {}
    for wafer in json_decode['wafers']:
        for j in range(wafer['quantity']):
            completed_steps[f"{wafer['type']}-{j+1}"] = set()

    machine_available_time = {}
    machine_parameters = {}
    machine_step_count = {}
    for machine in json_decode['machines']:
        machine_available_time[machine['machine_id']] = 0
        machine_parameters[machine['machine_id']] = machine['initial_parameters']['P1']
        machine_step_count[machine['machine_id']] = 0

    while str_list:
        for s in str_list[:]:
            wafer_type, wafer_index, step_index = s.split('-')
            wafer_id = f'{wafer_type}-{int(wafer_index) + 1}'
            w_need = int(wafer_index)
            step_id = f'S{step_index}'

            if step_id not in step_list:
                continue

            valid_machines = step_list[step_id]
            assigned_machine = None

            # To avoid repetition
            if step_id in completed_steps[wafer_id]:
                continue
            
            if step_dependencies[step_id]:
                if not all(dep in completed_steps[wafer_id] for dep in step_dependencies[step_id]):
                    continue

            # Earliest end time
            earliest_end_time = float('inf')
            for machine_id in valid_machines:
                if machine_available_time[machine_id] < earliest_end_time:
                    assigned_machine = machine_id
                    earliest_end_time = machine_available_time[machine_id]

            if assigned_machine is None:
                continue

            wafer_data = next(w for w in json_decode['wafers'] if w['type'] == wafer_type)
            processing_time = wafer_data['processing_times'][step_id]

            if w[w_need] <= i and machine_available_time[assigned_machine] <= i:
                start_time = max(machine_available_time[assigned_machine], w[w_need])
                end_time = start_time + processing_time
                
                # Cooldown
                if not (json_decode['steps'][int(step_id[1:])-1]['parameters']['P1'][0] <= machine_parameters[assigned_machine] <= json_decode['steps'][int(step_id[1:])-1]['parameters']['P1'][1]):
                    start_time += json_decode['machines'][int(assigned_machine[1:])-1]['cooldown_time']
                    end_time += json_decode['machines'][int(assigned_machine[1:])-1]['cooldown_time']
                    machine_parameters[assigned_machine] = json_decode['machines'][int(assigned_machine[1:])-1]['initial_parameters']['P1']

                schedule.append({
                    'wafer_id': wafer_id,
                    'step': step_id,
                    'machine': assigned_machine,
                    'start_time': start_time,
                    'end_time': end_time
                })

                w[w_need] = end_time
                machine_available_time[assigned_machine] = end_time
                str_list.remove(s)
                completed_steps[wafer_id].add(step_id)

                machine_step_count[assigned_machine] += 1
                if machine_step_count[assigned_machine] >= json_decode['machines'][int(assigned_machine[1:])-1]['n']:
                    machine_parameters[assigned_machine] += json_decode['machines'][int(assigned_machine[1:])-1]['fluctuation']['P1']
                    machine_step_count[assigned_machine] = 0

        i += 1

    print(f"Time taken: {i - 1}")
    json_object = json.dumps({'schedule': schedule}, indent=4)

    with open(output_file_path, 'w') as output_file:
        output_file.write(json_object)

main()
