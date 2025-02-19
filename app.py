from flask import Flask, render_template
import folium
from folium import plugins

app = Flask(__name__)

def create_map():
    # Create a base world map
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Add legend
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: 120px; 
                    border:2px solid grey; z-index:9999; background-color:white;
                    padding: 10px;
                    font-size: 14px;">
            <p><strong>Study Distribution</strong></p>
            <p>🔴 Large circle: >30% studies</p>
            <p>🔵 Medium circle: 10-30% studies</p>
            <p>⚪ Small circle: <10% studies</p>
        </div>
        '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Global data with extended information
    global_data = {
        'Americas': {
            'lat': 40, 'lon': -100, 'percentage': 6.5,
            'details': {
                'North America': 4.5,
                'South America': 2.0,
                'Key Findings': 'Limited studies on environmental impacts on ocular health'
            }
        },
        'Europe': {
            'lat': 50, 'lon': 10, 'percentage': 6.5,
            'details': {
                'Western Europe': 4.0,
                'Eastern Europe': 2.5,
                'Key Findings': 'Focus on air pollution and urban environment effects'
            }
        },
        'Asia': {
            'lat': 34, 'lon': 100, 'percentage': 42.8,
            'details': {
                'East Asia': 25.0,
                'South Asia': 12.8,
                'Southeast Asia': 5.0,
                'Key Findings': 'Extensive research on myopia and air pollution impacts'
            }
        },
        'Africa': {
            'lat': 0, 'lon': 20, 'percentage': 22.1,
            'details': {
                'North Africa': 11.8,
                'West Africa': 17.6,
                'East Africa': 29.4,
                'Central Africa': 5.9,
                'Southern Africa': 35.3,
                'Key Findings': 'Focus on UV exposure and indoor air pollution effects'
            }
        }
    }

    # Add circles for global distribution with interactive popups
    for region, data in global_data.items():
        # Determine circle size and color based on percentage
        radius = data['percentage'] * 100000
        if data['percentage'] > 30:
            color = 'red'
        elif data['percentage'] > 10:
            color = 'blue'
        else:
            color = 'lightgray'
            
        # Create detailed HTML popup content
        popup_content = f"""
        <div style="width:300px;">
            <h4>{region}</h4>
            <p><strong>Total Studies:</strong> {data['percentage']}%</p>
            <hr>
            <h5>Regional Breakdown:</h5>
            <ul>
        """
        for sub_region, sub_percentage in data['details'].items():
            if sub_region != 'Key Findings':
                popup_content += f"<li>{sub_region}: {sub_percentage}%</li>"
        
        popup_content += f"""
            </ul>
            <hr>
            <p><strong>Key Findings:</strong> {data['details']['Key Findings']}</p>
        </div>
        """
        
        # Add circle with popup
        folium.Circle(
            location=[data['lat'], data['lon']],
            radius=radius,
            popup=folium.Popup(popup_content, max_width=300),
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # Add search functionality
    m.add_child(plugins.Search(
        layer=None,
        geom_type='Point',
        placeholder='Search regions...',
        collapsed=False,
        search_label='name'
    ))
    
    return m

@app.route('/')
def index():
    m = create_map()
    return m.get_root().render()

if __name__ == '__main__':
    app.run(debug=True)
