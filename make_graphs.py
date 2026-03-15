import matplotlib.pyplot as plt
import sys
from datetime import datetime
import json

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def make_graph(x_list,y_list,name):

    # set Colors
    bg_color = '#2C2C2C' #background
    text_color = '#FFFFFF'
    bar_color = '#00D4FF'
    grid_color = '#555555'
    box_color='#444444'

    if(len(x_list) == 12): # stuff for Year Graph
        x_label = 'Month'
        x_ind = 1
        x_rot = 45
        graph_type = 'year'
    else: # stuff for Month Graph
        x_label = 'Day'
        x_ind = 6
        x_rot = 0
        graph_type = 'month'

    # Setup Figure (1080x1080)
    fig, ax = plt.subplots(figsize=(5.4, 5.4), dpi=200)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.bar(x_list, y_list, color=bar_color, edgecolor=bg_color, linewidth=1, width=0.8, zorder=3)
    ax.set_ylim(bottom=0)

    # Box with Total Hours
    fig.text(0.9, 0.9, f'Total: {(sum(y_list)):.1f} Hr', 
         fontsize=12, color=text_color, fontweight='bold', 
         ha='right', va='top', 
         bbox=dict(facecolor=box_color, alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))
    
    # Styling
    ax.set_title('Time Surfing: '+str(name), fontsize=16, fontweight='bold', color=text_color, pad=20, loc='left')
    ax.set_xlabel(x_label, fontsize=16, color=text_color)
    ax.set_ylabel('Hours', fontsize=16, color=text_color)

    ax.tick_params(axis='both', colors=text_color, labelsize=12)
    ax.grid(True, linestyle='--', color=grid_color, alpha=0.3, zorder=1)
    plt.subplots_adjust(left=0.13, right=0.87, top=0.85, bottom=0.15)

    ax.tick_params(axis='both', colors=text_color, labelsize=12)
    plt.xticks(range(0, len(x_list), x_ind), x_list[::x_ind],rotation=x_rot)

    for spine in ax.spines.values():
        spine.set_edgecolor(grid_color)

    # 4. Save
    plt.savefig('./instagram/to_upload/graph_'+graph_type+'.jpg', facecolor=fig.get_facecolor())


def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        match n % 10:
            case 1: suffix = 'st'
            case 2: suffix = 'nd'
            case 3: suffix = 'rd'
            case _: suffix = 'th'     
    return f"{n}{suffix}"
    
def month_graph(data,month):
    day_values = data[month]
    days = list(range(1, len(day_values) + 1))
    days = [get_ordinal(day) for day in days]
            
    make_graph(x_list= days, y_list= day_values, name= month)


def year_graph(data,year):
    months = list(data.keys())
    monthly_totals = [sum(values) for values in data.values()]
    months = [month[:3].upper() for month in months]

    make_graph(x_list= months, y_list= monthly_totals, name= year)




def main():
    try:
        date_obj = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        year = date_obj.year
        month_name = date_obj.strftime("%B")
    except ValueError:
        print("Error: Please provide the date in YYYY-MM-DD format.")

    data = load_data('./data/2026.json')

    month_graph(data,month_name)
    year_graph(data,year)

main()






