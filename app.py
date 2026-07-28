# ============================================================
# CHILD PROTECTION LEGAL MONITORING PLATFORM
#
# PART 1/3
#
# Purpose:
# This creates the foundation of the dashboard.
#
# It:
# - imports the tools we need
# - creates the page
# - creates country coordinates for map dots
# - fixes country naming differences from Excel
#
# The next parts will:
# PART 2:
# - load CAMT - Template.xlsx
# - keep only Active records
# - prepare the data
#
# PART 3:
# - create the interactive map
# - create clickable dots
# - display country profiles
# ============================================================



# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================


# Streamlit:
# Turns Python code into a website/dashboard.
import streamlit as st


# Pandas:
# Allows Python to read and manipulate Excel files.
import pandas as pd


# Folium:
# Creates interactive maps.
import folium


# Allows Streamlit to display Folium maps.
from streamlit_folium import st_folium


# Used for dates.
from datetime import datetime



# ============================================================
# 2. PAGE SETTINGS
# ============================================================


st.set_page_config(

    page_title="Care and Adoption Monitoring Tool",

    layout="wide"

)



st.title(
    "Care and Adoption Monitoring Tool"
)


st.caption(
    f"This tool seeks to track legal and policy reforms in the field of child protection with a particular focus on care and adoption • "
    f"{datetime.now().strftime('%d %B %Y')}"
)



st.markdown("---")



# ============================================================
# 3. COUNTRY COORDINATES
# ============================================================
#
# These numbers tell the map where each dot belongs.
#
# Format:
#
# Country:
# [latitude, longitude]
#
# Latitude  = north/south
# Longitude = east/west
#
# These are placed in the middle of countries
# to avoid dots appearing in oceans.
# ============================================================


COUNTRY_COORDS = {


    "South Korea":
        [35.9078, 127.7669],

    "Chile":
        [-35.6751, -71.5430],

    "Spain":
        [40.4637, -3.7492],

    "Denmark":
        [56.2639, 9.5018],

    "Brazil":
        [-14.2350, -51.9253],

    "Colombia":
        [4.5709, -74.2973],

    "Taiwan":
        [23.6978, 120.9605],

    "Nepal":
        [28.3949, 84.1240],

    "Bhutan":
        [27.5142, 90.4336],

    "Guatemala":
        [15.7835, -90.2308],


    "Cambodia":
        [12.5657, 104.9910],

    "Madagascar":
        [-18.7669, 46.8691],

    "Ivory Coast":
        [7.5399, -5.5471],

    "Vietnam":
        [14.0583, 108.2772],

    "Portugal":
        [39.3999, -8.2245],

    "France":
        [46.2276, 2.2137],

    "Cameroon":
        [7.3697, 12.3547],

    "Ethiopia":
        [9.1450, 40.4897],


    "China":
        [35.8617, 104.1954],

    "Mozambique":
        [-18.6657, 35.5296],

    "Guinea-Bissau":
        [11.8037, -15.1804],


    "United Kingdom":
        [55.3781, -3.4360],


    "Ireland":
        [53.1424, -7.6921],


    "Thailand":
        [15.8700,100.9925],


    "Nigeria":
        [9.0820,8.6753],


    "Tunisia":
        [33.8869,9.5375],


    "Ukraine":
        [48.3794,31.1656],


    "Russia":
        [61.5240,105.3188],


    "Haiti":
        [18.9712,-72.2852],


    "Germany":
        [51.1657,10.4515],


    "Italy":
        [41.8719,12.5674],


    "Montenegro":
        [42.7087,19.3744],


    "Armenia":
        [40.0691,45.0382],


    "Finland":
        [61.9241,25.7482],


    "Norway":
        [60.4720,8.4689],


    "Romania":
        [45.9432,24.9668],


    "South Africa":
        [-30.5595,22.9375],


    "Belgium":
        [50.5039,4.4699],


    "Netherlands":
        [52.1326,5.2913],


    "Angola":
        [-11.2027,17.8739],


    "Sweden":
        [60.1282,18.6435],


    "Mexico":
        [23.6345,-102.5528],


    "Peru":
        [-9.1900,-75.0152],


    "Rwanda":
        [-1.9403,29.8739],


    "Kenya":
        [-0.0236,37.9062],


    "Uganda":
        [1.3733,32.2903],


    "Philippines":
        [12.8797,121.774],


    "Hungary":
        [47.1625,19.5033],


    "India":
        [20.5937,78.9629],


    "Morocco":
        [31.7917,-7.0926],


    "Switzerland":
        [46.8182,8.2275],


}



# ============================================================
# 4. COUNTRY NAME CLEANING
# ============================================================
#
# Excel files often contain different names
# for the same country.
#
# Example:
#
# Belgium (Flemish community)
#
# should still appear on the Belgium dot.
#
# This changes ONLY the map name.
# The original Excel information stays unchanged.
# ============================================================


COUNTRY_FIXES = {


    "Belgium (Flemish community)":
        "Belgium",


    "Belgium(Flemish community)":
        "Belgium",


    "The Netherlands":
        "Netherlands",


    "England":
        "United Kingdom",


    "Wales":
        "United Kingdom",


    "Scotland":
        "United Kingdom",


    "Guinea Bissau":
        "Guinea-Bissau",


}



def clean_country_name(country):


    return COUNTRY_FIXES.get(

        country,

        country

    )



# ============================================================
# END OF PART 1/3
# ============================================================

# ============================================================
# CHILD PROTECTION LEGAL MONITORING PLATFORM
#
# PART 2/3
#
# Purpose:
#
# This part connects the dashboard to your Excel file.
#
# It:
# - opens CAMT - Template.xlsx
# - cleans the column names
# - keeps only Active records
# - fixes country names
# - prepares the data for the map
#
# ============================================================



# ============================================================
# 5. LOAD EXCEL DATA
# ============================================================


@st.cache_data
def load_excel():

    """
    Reads the Excel file.

    st.cache_data means:
    Streamlit remembers the file,
    so it does not reload it every time
    you click something.
    """

    df = pd.read_excel(
        "CAMT - Template.xlsx"
    )


    # Remove accidental spaces
    # Example:
    # " Country " becomes "Country"

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )


    return df



df = load_excel()



# ============================================================
# 6. CHECK REQUIRED COLUMN
# ============================================================
#
# Your Excel uses:
#
# Record Status
#
# NOT:
#
# Status
#
# This prevents the KeyError problem.
# ============================================================


if "Record Status" not in df.columns:


    st.error(
        "The Excel file does not contain 'Record Status'."
    )


    st.write(
        "Columns found:"
    )


    st.write(
        list(df.columns)
    )


    st.stop()



# ============================================================
# 7. KEEP ONLY ACTIVE RECORDS
# ============================================================
#
# The dashboard should only display
# current active reforms.
#
# Anything marked:
# - Closed
# - Archived
# - Inactive
#
# will disappear from the dashboard.
# ============================================================


df = df[
    df["Record Status"]
    .astype(str)
    .str.strip()
    .str.lower()
    == "active"
].copy()



# ============================================================
# 8. CLEAN COUNTRY NAMES
# ============================================================
#
# This creates a second country column.
#
# Original Excel:
# stays untouched.
#
# Map_Country:
# is only used for dots and filtering.
# ============================================================


df["Map_Country"] = (
    df["Country"]
    .astype(str)
    .str.strip()
    .apply(clean_country_name)
)



# ============================================================
# 9. REMOVE INVALID COUNTRY ENTRIES
# ============================================================
#
# Sometimes Excel contains placeholders
# like:
#
# "e.g. Germany"
#
# These are not real countries.
#
# We remove them silently so they
# do not create fake map dots.
# ============================================================


INVALID_COUNTRIES = [

    "e.g. Germany",

    "example",

    "test",

    "nan",

    ""

]


df = df[
    ~df["Map_Country"]
    .isin(INVALID_COUNTRIES)
].copy()



# ============================================================
# 10. REMOVE COUNTRIES WITHOUT COORDINATES
# ============================================================
#
# If someone adds a new country later,
# the dashboard will ignore it instead
# of placing a dot in the ocean.
# ============================================================


df = df[
    df["Map_Country"]
    .isin(COUNTRY_COORDS.keys())
].copy()


# ============================================================
# 10 b. CREATE MAP COORDINATES
# ============================================================
#
# This takes:
#
# Belgium
#
# and finds:
#
# [50.5039, 4.4699]
#
# ============================================================



df["Latitude"] = (
    df["Map_Country"]
    .apply(
        lambda x:
        COUNTRY_COORDS[x][0]
    )
)



df["Longitude"] = (
    df["Map_Country"]
    .apply(
        lambda x:
        COUNTRY_COORDS[x][1]
    )
)



# ============================================================
# 11. SHOW LOADING CHECK
# ============================================================
#
# You can delete this later.
# It is useful while building.
# ============================================================


st.success(
    f"Active records loaded: {len(df)}"
)



# ============================================================
# 12. AVAILABLE COUNTRIES
# ============================================================
#
# Stores the countries available in the dashboard.
# ============================================================


AVAILABLE_COUNTRIES = sorted(

    df["Map_Country"]
    .unique()

)



# ============================================================
# END OF PART 2/3
#
# Next:
#
# PART 3/3
#
# - create world map
# - coloured dots
# - clickable popups
# - country profile cards
# - reform timeline
#
# ============================================================

# ============================================================
# CHILD PROTECTION LEGAL MONITORING PLATFORM
#
# PART 3/3
#
# Purpose:
#
# Creates the interactive map and country profiles.
#
# Features:
#
# - clickable country dots
# - hover shows country name
# - popup shows only reform summary
# - click country -> detailed country section below
# - supports multiple reforms per country
# - flags displayed
# - sources displayed as bullet points
# - hides empty Adoption Status
#
# ============================================================

# ============================================================
# COUNTRY FLAGS
# ============================================================
#
# These are emojis.
# They display automatically next to countries.
#
# ============================================================


COUNTRY_FLAGS = {

    "South Korea": "🇰🇷",
    "Chile": "🇨🇱",
    "Spain": "🇪🇸",
    "Denmark": "🇩🇰",
    "Brazil": "🇧🇷",
    "Colombia": "🇨🇴",
    "Taiwan": "🇹🇼",
    "Nepal": "🇳🇵",
    "Bhutan": "🇧🇹",
    "Guatemala": "🇬🇹",

    "Cambodia": "🇰🇭",
    "Madagascar": "🇲🇬",
    "Ivory Coast": "🇨🇮",
    "Vietnam": "🇻🇳",
    "Portugal": "🇵🇹",
    "France": "🇫🇷",
    "Cameroon": "🇨🇲",
    "Ethiopia": "🇪🇹",

    "China": "🇨🇳",
    "Mozambique": "🇲🇿",
    "Guinea-Bissau": "🇬🇼",

    "United Kingdom": "🇬🇧",
    "Ireland": "🇮🇪",
    "Thailand": "🇹🇭",
    "Nigeria": "🇳🇬",
    "Tunisia": "🇹🇳",
    "Ukraine": "🇺🇦",
    "Russia": "🇷🇺",
    "Haiti": "🇭🇹",

    "Germany": "🇩🇪",
    "Italy": "🇮🇹",
    "Montenegro": "🇲🇪",
    "Armenia": "🇦🇲",
    "Finland": "🇫🇮",
    "Norway": "🇳🇴",
    "Romania": "🇷🇴",

    "South Africa": "🇿🇦",
    "Belgium": "🇧🇪",
    "Netherlands": "🇳🇱",
    "Angola": "🇦🇴",
    "Sweden": "🇸🇪",
    "Mexico": "🇲🇽",
    "Peru": "🇵🇪",
    "Rwanda": "🇷🇼",
    "Kenya": "🇰🇪",
    "Uganda": "🇺🇬",

    "Philippines": "🇵🇭",
    "Hungary": "🇭🇺",
    "India": "🇮🇳",
    "Morocco": "🇲🇦",
    "Switzerland": "🇨🇭"

}



# ============================================================
# CREATE MAP
# ============================================================


world_map = folium.Map(

    location=[20,0],

    zoom_start=2,

    min_zoom=2,

    max_zoom=6,

    tiles="CartoDB positron"

)


# ============================================================
# REFORM STATUS COLOUR LOGIC
# ============================================================


def get_country_dot_colour(group):


    statuses = (

        group["Reform Status"]

        .dropna()

        .astype(str)

        .str.strip()

        .str.lower()

        .tolist()

    )


    years = (

        group["Year"]

        .dropna()

        .astype(str)

        .tolist()

    )


    current_year = datetime.now().year



    # ==========================================
    # RED = ONGOING REFORM
    # ==========================================

    for status in statuses:

        if any(word in status for word in [

            "ongoing",
            "in progress",
            "underway",
            "draft",
            "review",
            "revision",
            "developing"

        ]):

            return "#DC2626"



    # ==========================================
    # BLUE = ANTICIPATED REFORM
    # ==========================================

    for status in statuses:

        if any(word in status for word in [

            "anticipated",
            "planned",
            "expected",
            "proposed",
            "upcoming",
            "future"

        ]):

            return "#2563EB"



    # ==========================================
    # ORANGE = RECENT REFORM
    # ==========================================

    for year in years:

        if (
            str(current_year) in year
            or
            str(current_year-1) in year
            or
            str(current_year-2) in year
        ):

            return "#F97316"



    # ==========================================
    # GREY = UNKNOWN
    # ==========================================

    return "#9CA3AF"

# ============================================================
# ADD COUNTRY DOTS
# ============================================================
#
# Each country gets one dot.
#
# If a country has 5 reforms,
# it still only gets one dot.
#
# ============================================================


for country, group in df.groupby("Map_Country"):


    coords = COUNTRY_COORDS[country]

    # Count how many reforms this country has
    number_of_reforms = len(group)



    popup_text = f"""

    <div style="
    width:300px;
    max-height:300px;
    overflow-y:auto;
    font-family:Arial;
    ">

    <h3>
    {COUNTRY_FLAGS.get(country,"🌍")}
    {country}
    </h3>

    <hr>

    <b>
    Active reforms:
    </b>

    {number_of_reforms}

    <br><br>

    """



    counter = 1


    for _, row in group.iterrows():


        popup_text += f"""

        <hr>

        <b>
        Reform {counter}
        </b>

        <br><br>


        <b>
        Reform Type:
        </b>

        {row.get("Reform Type","")}


        <br><br>


        <b>
        Reform Status:
        </b>

        {row.get("Reform Status","")}


        <br><br>


        <b>
        Year:
        </b>

        {row.get("Year","")}

        """


        counter += 1



    popup_text += "</div>"

    dot_colour = get_country_dot_colour(group)

    marker = folium.CircleMarker(

        location=coords,

        radius=10,

        color=dot_colour,

        fill=True,

        fill_color=dot_colour,

        fill_opacity=1,

        weight=2,

        tooltip=f"{COUNTRY_FLAGS.get(country, '🌍')} {country} ({number_of_reforms} reforms)"

    )


    marker.add_child(

        folium.Popup(

            popup_text,

            max_width=350

        )

    )



    marker.add_to(world_map)



# ============================================================
# REFORM STATUS LEGEND
# ============================================================


legend_html = """

<div style="

position: fixed;

bottom:30px;

left:30px;

width:240px;

background:white;

border:2px solid #999;

z-index:9999;

padding:12px;

border-radius:10px;

font-family:Arial;

font-size:14px;

">


<b>
Reform Status
</b>


<br><br>


<span style="color:#DC2626;font-size:22px;">
●
</span>

Ongoing reform


<br>


<span style="color:#F97316;font-size:22px;">
●
</span>

Recent reform (1–2 years)


<br>


<span style="color:#2563EB;font-size:22px;">
●
</span>

Anticipated reform


<br>


<span style="color:#9CA3AF;font-size:22px;">
●
</span>

Unknown status


</div>

"""


world_map.get_root().html.add_child(

    folium.Element(
        legend_html
    )

)



map_data = st_folium(

    world_map,

    width=1200,

    height=650,

    returned_objects=[
        "last_object_clicked"
    ],

    key="main_map"

)



# ============================================================
# DETECT CLICKED COUNTRY
# ============================================================


if "selected_country" not in st.session_state:

    st.session_state.selected_country = None



if map_data:


    clicked = map_data.get(
        "last_object_clicked"
    )


    if clicked:


        lat = clicked.get("lat")

        lng = clicked.get("lng")


        for country, coords in COUNTRY_COORDS.items():


            if (

                round(coords[0],2)
                ==
                round(lat,2)

                and

                round(coords[1],2)
                ==
                round(lng,2)

            ):

                st.session_state.selected_country = country



# ============================================================
# COUNTRY DETAILS SECTION
# ============================================================



st.markdown("---")



if st.session_state.selected_country is None:


    st.info(
        "🌍 Click on a country dot to see what reforms are happening."
    )



else:


    country = st.session_state.selected_country



    country_data = df[

        df["Map_Country"]

        == country

    ]



    st.header(

        f"{COUNTRY_FLAGS.get(country,'🌍')} {country}"

    )



    st.subheader(

        f"Active reforms: {len(country_data)}"

    )




    # ========================================================
    # DISPLAY EACH REFORM
    # ========================================================



    for number, (_, row) in enumerate(

        country_data.iterrows(),

        start=1

    ):



        st.markdown("---")



        st.subheader(

            f"Reform {number}"

        )



        st.write(

            "**Reform Type**"

        )

        st.write(

            row.get(
                "Reform Type",
                "Not provided"
            )

        )



        st.write(

            "**Reform Status**"

        )

        st.write(

            row.get(
                "Reform Status",
                "Not provided"
            )

        )



        st.write(

            "**Year**"

        )

        st.write(

            str(
                row.get(
                    "Year",
                    ""
                )
            )

        )



        st.write(

            "**Description**"

        )

        st.write(

            row.get(

                "Description - info that will be displayed",

                "No description available."

            )

        )



        # ---------------------------------------------
        # ADOPTION STATUS
        # ---------------------------------------------


        adoption = row.get(
            "Adoption Status"
        )


        if pd.notna(adoption) and str(adoption).strip() != "":


            st.write(

                "**Adoption Status**"

            )


            st.write(

                adoption

            )



        # ---------------------------------------------
        # SOURCES
        # ---------------------------------------------


        sources = row.get(

            "Source(s) - info that will be displayed"

        )


        if pd.notna(sources) and str(sources).strip() != "":


            st.write(

                "**Sources**"

            )

            # ============================================================
            # CLEAN SOURCES DISPLAY
            # ============================================================
            #
            # Removes:
            # - empty lines
            # - empty bullet points
            # - accidental spaces
            #
            # Keeps only real sources.
            #
            # ============================================================

            source_list = str(sources).split("\n")

            clean_sources = []

            for source in source_list:

                # Remove spaces and bullet symbols
                cleaned = (
                    source
                    .replace("•", "")
                    .strip()
                )

                # Only keep real text
                if cleaned != "":
                    clean_sources.append(cleaned)

            # Display sources neatly

            for source in clean_sources:
                st.write(

                    "• " + source
                 )

