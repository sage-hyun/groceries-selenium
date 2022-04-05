from datetime import datetime

def calc_count(elem):
    return len(elem['date_list'])

def calc_cycle(elem):
    gaps = []
    for i in range(len(elem['date_list']) - 1):
        date_1 = datetime.strptime(elem['date_list'][i], '%Y.%m.%d')
        date_2 = datetime.strptime(elem['date_list'][i+1], '%Y.%m.%d')
        gap =  date_1 - date_2
        gaps.append(gap.days)
    return sum(gaps)/len(gaps) if gaps else 0


def calculate_values(db):
    groceries_data = db.recipt.find()
    
    for elem in groceries_data:

        db.recipt.update_one({'_id': elem['_id']}, {'$set': {
            'count': calc_count(elem),
            'cycle': calc_cycle(elem),
        }},
        upsert=True)