import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Calculator",
    page_icon="🪴",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px;
        color: #0e1117;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00cc66;
        color: white;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #00cc66;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
# Carbon Calculator Class
class CarbonCalculator:
    # Carbon emission factors (adjusted for kilometers)
    FACTORS = {
        'car_per_km': 404 / 1.60934,  # grams CO2 per km
        'public_transit_per_hour': 140,  # grams CO2 per hour
        'flight_per_trip': 900000,  # grams CO2 per flight
        'electricity_per_kwh': 430,  # grams CO2 per kWh
        'electronic_gadgets_per_day': 3600,  # grams CO2 per day
        'lpg_per_kg': 224.78,  # grams CO2 per kg
        'diet_factors': {
            'vegetarian': 1800,  # grams CO2 per day
            'Non-vegetarian': 2500  # grams CO2 per day
        }
    }
    
    @staticmethod
    def calculate_transportation_footprint(car_km, transit_hours, flights):
        car = car_km * CarbonCalculator.FACTORS['car_per_km']
        transit = transit_hours * CarbonCalculator.FACTORS['public_transit_per_hour']
        flight = flights * CarbonCalculator.FACTORS['flight_per_trip']
        return (car + transit + flight) / 1000  # Convert to kg
    
    @staticmethod
    def calculate_home_energy_footprint(electricity_kwh, gadget_hour, gas_kg, renewable):
        electricity = electricity_kwh * CarbonCalculator.FACTORS['electricity_per_kwh']
        gadgets = CarbonCalculator.FACTORS['electronic_gadgets_per_day'] * (gadget_hour / 24) * 365
        gas = gas_kg * CarbonCalculator.FACTORS['lpg_per_kg']
        total = electricity + gadgets + gas
        return (total * (0.5 if renewable else 1)) / 1000  # Convert to kg
    
    @staticmethod
    def calculate_lifestyle_footprint(diet_type, recycling, composting):
        diet = CarbonCalculator.FACTORS['diet_factors'][diet_type] * 365
        recycling_factor = 0.8 if recycling else 1
        composting_factor = 0.9 if composting else 1
        return (diet * recycling_factor * composting_factor) / 1000  # Convert to kg
# Initialize session state
def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'results' not in st.session_state:
        st.session_state.results = None
# Create visualization functions
import plotly.graph_objects as go
def create_gauge_chart(value, title, max_value=20000):
    """
    Create a clean and aesthetic gauge chart with improved colors and layout.
    Parameters:
        value (float): The value to display on the gauge chart.
        title (str): Title of the gauge chart.
        max_value (int, optional): Maximum value for the gauge. Defaults to 20000.
    Returns:
        go.Figure: A Plotly figure object for the gauge chart.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18, 'color': 'darkgreen'}},  # Changed text color to dark green
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 2, 'tickcolor': "darkgreen"},  # Changed tick color to dark green
            'bar': {'color': "#4CAF50"},  # Dark green for the needle bar
            'steps': [
                {'range': [0, max_value * 0.25], 'color': "#A7F3D0"},  # Soft green
                {'range': [max_value * 0.25, max_value * 0.5], 'color': "#FFECA9"},  # Soft yellow
                {'range': [max_value * 0.5, max_value * 0.75], 'color': "#FFD6A5"},  # Soft orange
                {'range': [max_value * 0.75, max_value], 'color': "#FCA5A5"}  # Soft red
            ],
            'borderwidth': 0,  # Removes outer border
            'bordercolor': "white"
        }
    ))
    # Remove background color for a cleaner look
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkgreen", 'family': "Arial"}  # Changed overall font color to dark green
    )
    return fig
def create_pie_chart(results):
    labels = ['Transportation', 'Home Energy', 'Lifestyle']
    values = [results['transportation'], results['home_energy'], results['lifestyle']]
    
    fig = px.pie(
        values=values,
        names=labels,
        title='Carbon Footprint Breakdown',
        color_discrete_sequence=px.colors.sequential.Greens
    )
    return fig
# Page functions
def show_home_page():
    st.markdown("<h2 style='font-size: 32px;'>Welcome to Carbon Footprint Calculator 🌏👣</h2>", unsafe_allow_html=True)
    
    # Hero section with image
    st.image("https://www.greenyellow.vn/wp-content/uploads/2023/02/Reducing-our-personal-carbon-footprint.webp", use_container_width=True)
    # Introduction
    st.markdown("""
    ## Calculate Your Environmental Impact
    
    Understanding your carbon footprint is the first step towards a more sustainable lifestyle. 
    This calculator helps you:
    
    - 📊 Measure your carbon emissions
    - 🔍 Identify areas for improvement
    - 💡 Get personalized recommendations
    - 🌱 Track your progress towards sustainability
    
    ### How it works
    1. Enter your daily activities and consumption patterns
    2. Get instant calculations of your carbon footprint
    3. Receive tailored suggestions to reduce your impact
    """)
    st.markdown("---")
    st.markdown('<h3 style="text-align: center;">🌸🍉 Seasonal Tips 🍂☃️</h3>', unsafe_allow_html=True)
    # Create two columns for text content
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color: #e7f5e6; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <strong>Spring/Summer Tips</strong><br>
            • Use natural ventilation<br>
            • Start a home garden<br>
            • Use a clothesline instead of a dryer
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color: #f7f7f7; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <strong>Fall/Winter Tips</strong><br>
            • Seal drafts around windows<br>
            • Use LED holiday lights<br>
            • Lower thermostat at night
        </div>
        """, unsafe_allow_html=True)
    # Now center the image below the text columns
    st.markdown("<br>", unsafe_allow_html=True)  # Adding some spacing between text and image
    st.image("https://facts.net/wp-content/uploads/2023/07/20-facts-about-season-1689740634.jpg", use_container_width=True)
def show_calculator_page():
    st.title("📝 Carbon Footprint Calculator")
    
    # Create tabs for different sections
    tabs = st.tabs(["🚗 Transportation", "🏠 Home Energy", "🌱 Lifestyle"])
    
    # Transportation tab
    with tabs[0]:
        st.subheader("Transportation")
        col1, col2 = st.columns(2)
        
        with col1:
            car_km = st.number_input(
                "Kilometers driven per week",
                min_value=0.0,
                help="Enter the average number of kms you drive per week"
            )
            
            transit_hours = st.number_input(
                "Public transit hours per week",
                min_value=0.0,
                help="Enter the average hours spent on public transit per week"
            )
        
        with col2:
            flights = st.number_input(
                "Flights per year",
                min_value=0,
                help="Enter the number of flights you take per year"
            )
        st.image("https://www.jeunes-bfc.fr/wp-content/uploads/2020/11/Transport.jpg", use_container_width=True)
    
    # Home Energy tab
    with tabs[1]:
        st.subheader("Home Energy")
        col1, col2 = st.columns(2)
        
        with col1:
            electricity = st.number_input(
                "Monthly electricity usage (kWh)",
                min_value=0.0,
                help="Enter your average monthly electricity consumption"
            )
            gadgets = st.number_input(
                "Daily electronic gadget usage (hours)",
                min_value=0.0,
                help="Enter your average daily usage of electronic gadgets"
            )
        
        with col2:
            gas = st.number_input(
                "Monthly LPG usage (Kg)",
                min_value=0.0,
                help="Enter your average monthly LPG consumption"
            )
        
            renewable = st.checkbox(
                "I use renewable energy",
                help="Check if you use renewable energy sources"
            )
        st.image("https://d33v4339jhl8k0.cloudfront.net/docs/assets/627afc47b51f9b2b2d459d04/images/62ebeb535e08866388c2f720/file-fRLKOOxgBW.png", use_container_width=True)
    
    # Lifestyle tab
    with tabs[2]:
        st.subheader("Lifestyle")
        col1, col2 = st.columns(2)
        
        with col1:
            diet_type = st.selectbox(
                "Diet type",
                options=['vegetarian', 'Non-vegetarian'],
                help="Select your primary diet type"
            )
        
        with col2:
            recycling = st.checkbox(
                "I regularly recycle",
                help="Check if you regularly recycle materials"
            )
            composting = st.checkbox(
                "I regularly compost",
                help="Check if you regularly compost organic waste"
            )
        st.image("https://static.vecteezy.com/system/resources/previews/041/416/672/non_2x/sustainable-diet-scenes-collection-people-buy-local-reduce-waste-eat-eco-friendly-food-ecology-compositions-set-with-lettering-illustrations-of-green-lifestyle-and-sustainability-vector.jpg", use_container_width=True)
    
    # Calculate button
    if st.button("Calculate My Footprint", type="primary"):
        # Calculate footprints
        transportation = CarbonCalculator.calculate_transportation_footprint(
            car_km, transit_hours, flights
        )
        
        home_energy = CarbonCalculator.calculate_home_energy_footprint(
            electricity, gadgets, gas, renewable
        )
        
        lifestyle = CarbonCalculator.calculate_lifestyle_footprint(
            diet_type, recycling, composting
        )
        
        # Store results in session state
        st.session_state.results = {
            'transportation': transportation,
            'home_energy': home_energy,
            'lifestyle': lifestyle,
            'total': transportation + home_energy + lifestyle
        }
        
        # Update page state to 'results'
        st.session_state.page = 'results'
def show_results_page():
    st.title("📊 Your Carbon Footprint Results")
    
    if st.session_state.results is None:
        st.info("Please complete the calculator first!")
        st.session_state.page = 'calculator'  # Navigate back to the calculator page
        return
    
    results = st.session_state.results
    
    # Display total footprint with gauge chart
    st.subheader("Total Annual Carbon Footprint")
    total_gauge = create_gauge_chart(
        results['total'],
        "Total CO₂ Emissions (kg/year)"
    )
    st.plotly_chart(total_gauge, use_container_width=True)
    # Display breakdown
    st.subheader("Detailed Breakdown")
    col1, col2 = st.columns([2, 1])
    with col1:
        # Pie chart
        pie_chart = create_pie_chart(results)
        st.plotly_chart(pie_chart, use_container_width=True)
    with col2:
        # Numeric breakdown with yearly and monthly values
        st.markdown(f"""
        ### By Category
        1. 🚗 **Transportation**: 
        - {results['transportation']:.2f} kg CO₂/year, 
        - {results['transportation'] / 12:.2f} kg CO₂/month
        2. 🏠 **Home Energy**: 
        - {results['home_energy']:.2f} kg CO₂/year, 
        - {results['home_energy'] / 12:.2f} kg CO₂/month
        3. 🌱 **Lifestyle**: 
        - {results['lifestyle']:.2f} kg CO₂/year, 
        - {results['lifestyle'] / 12:.2f} kg CO₂/month
        """)
    # Display total monthly footprint
    total_monthly = results['total'] / 12
    st.markdown(f"""
    ### Total Carbon Footprint:
    - **Yearly**: {results['total']:.2f} kg CO₂/year
    - **Monthly**: {total_monthly:.2f} kg CO₂/month
    """)
  
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Personalized Recommendations")
    recommendations = []
    if results['transportation'] > 5000:
        recommendations.append("- Consider carpooling or using public transportation more frequently")
        recommendations.append("- Look into electric or hybrid vehicle options")
    
    if results['home_energy'] > 3000:
        recommendations.append("- Install LED bulbs and energy-efficient appliances")
        recommendations.append("- Consider switching to renewable energy sources")
    
    if results['lifestyle'] > 2000:
        recommendations.append("- Try incorporating more plant-based meals into your diet")
        recommendations.append("- Start composting organic waste")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(rec)
    else:
        st.success("Great job! Your carbon footprint is relatively low. Keep up the good work!")
    st.markdown("---")
    st.image("https://images.squarespace-cdn.com/content/v1/5463e0f8e4b03bb31b0b0605/2d329c8f-1715-484f-a66c-322898d14b18/Labconscious_GreenhouseGasEmissions_OffsetFootprint_infographic_0123+%282%29.png", use_container_width=True)
    
    # Action plan
    st.markdown("---")
    st.subheader("📋 Your Action Plan")
    st.markdown("""
    1. Set a goal to reduce your carbon footprint by 10% in the next 3 months
    2. Track your progress monthly using this calculator
    3. Implement the recommendations above one at a time
    4. Share your journey with friends and family to inspire change
    """)
    # Reset button
    if st.button("Calculate Again"):
        st.session_state.results = None
        st.session_state.page = 'calculator'  # Reset to calculator page 
    #st.image("https://otegotextile.com/wp-content/uploads/2021/01/shutterstock_1851755698.png", use_container_width=True)
# Main function
def main():
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.image("https://images.unsplash.com/photo-1544945582-3b466d874eac?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fHNlYSUyMGlzbGFuZHxlbnwwfHwwfHx8MA%3D%3D", use_container_width=True)
    st.sidebar.title("Navigation")
    
    pages = {
        "Home": "home",
        "Calculator": "calculator",
        "Results": "results"
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    st.session_state.page = pages[selection]
    
    # Display the selected page
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'calculator':
        show_calculator_page()
    elif st.session_state.page == 'results':
        show_results_page()
    # Footer
    st.sidebar.markdown("---")
    # Add the following CSS to center the leaf icon
    st.markdown("""<style>
        .leaf-animation { font-size: 80px; text-align: center; color: #4CAF50; animation: leafAnimation 3s ease-in-out infinite; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        @keyframes leafAnimation { 0% { transform: translate(-50%, -50%) translateY(0); opacity: 1; } 50% { transform: translate(-50%, -50%) translateY(-30px); opacity: 1; } 100% { transform: translate(-50%, -50%) translateY(0); opacity: 0; } }
        </style>""", unsafe_allow_html=True)
    # Display only the leaf icon with animation centered
    st.markdown(f"<div class='leaf-animation'>☘️</div>", unsafe_allow_html=True)
if __name__ == "__main__":
    main()