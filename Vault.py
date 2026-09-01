import streamlit as st
from google import genai
from supabase import create_client

# =========================================================
# TRADING VAULT V3.4
# =========================================================

st.set_page_config(
    page_title="Trading Vault",
    page_icon="🏦",
    layout="wide"
)

# =========================================================
# FORMAT FUNCTIONS
# =========================================================

def format_value(value):
    if value is None:
        return "N/A"

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if value >= 1_000:
        return f"{value / 1_000:.2f}K"

    return str(value)


def format_demand(value):
    if value is None:
        return "N/A"

    return f"{value:g}/10"


# =========================================================
# REGULAR FRUITS
# =========================================================

FRUITS = [

    {"name": "Rocket", "value": 5_000, "demand": 1,
     "rarity": "Common", "type": "Natural", "role": "Starter"},

    {"name": "Spin", "value": 7_500, "demand": 1,
     "rarity": "Common", "type": "Natural", "role": "Starter"},

    {"name": "Blade", "value": 20_000, "demand": 3,
     "rarity": "Common", "type": "Natural", "role": "PvP"},

    {"name": "Spring", "value": 60_000, "demand": 1,
     "rarity": "Common", "type": "Natural", "role": "Mobility"},

    {"name": "Bomb", "value": 80_000, "demand": 1,
     "rarity": "Common", "type": "Natural", "role": "PvP"},

    {"name": "Smoke", "value": 100_000, "demand": 1,
     "rarity": "Common", "type": "Elemental", "role": "Grinding"},

    {"name": "Spike", "value": 180_000, "demand": 1,
     "rarity": "Common", "type": "Natural", "role": "PvP"},

    {"name": "Flame", "value": 450_000, "demand": 2,
     "rarity": "Uncommon", "type": "Elemental", "role": "Grinding / PvP"},

    {"name": "Eagle", "value": 520_000, "demand": 3,
     "rarity": "Uncommon", "type": "Beast", "role": "PvP"},

    {"name": "Ice", "value": 640_000, "demand": 6,
     "rarity": "Uncommon", "type": "Elemental", "role": "PvP"},

    {"name": "Sand", "value": 720_000, "demand": 2,
     "rarity": "Uncommon", "type": "Elemental", "role": "PvP"},

    {"name": "Dark", "value": 800_000, "demand": 3,
     "rarity": "Uncommon", "type": "Elemental", "role": "PvP"},

    {"name": "Diamond", "value": 840_000, "demand": 3,
     "rarity": "Uncommon", "type": "Natural", "role": "Defense"},

    {"name": "Light", "value": 950_000, "demand": 2,
     "rarity": "Rare", "type": "Elemental", "role": "Grinding / Mobility"},

    {"name": "Rubber", "value": 700_000, "demand": 1,
     "rarity": "Rare", "type": "Natural", "role": "PvP"},

    {"name": "Ghost", "value": 1_140_000, "demand": 2,
     "rarity": "Rare", "type": "Natural", "role": "PvP"},

    {"name": "Magma", "value": 1_150_000, "demand": 5,
     "rarity": "Rare", "type": "Elemental", "role": "Sea Events / Grinding"},

    {"name": "Quake", "value": 1_000_000, "demand": 2,
     "rarity": "Legendary", "type": "Natural", "role": "PvP"},

    {"name": "Buddha", "value": 10_000_000, "demand": 10,
     "rarity": "Legendary", "type": "Beast", "role": "Grinding / Raids"},

    {"name": "Love", "value": 1_500_000, "demand": 3,
     "rarity": "Legendary", "type": "Natural", "role": "PvP / Support"},

    {"name": "Creation", "value": 2_500_000, "demand": 2,
     "rarity": "Legendary", "type": "Natural", "role": "PvP"},

    {"name": "Spider", "value": 1_500_000, "demand": 2,
     "rarity": "Legendary", "type": "Natural", "role": "PvP"},

    {"name": "Sound", "value": 2_500_000, "demand": 4,
     "rarity": "Legendary", "type": "Natural", "role": "Support / Raids"},

    {"name": "Phoenix", "value": 2_750_000, "demand": 3,
     "rarity": "Legendary", "type": "Beast", "role": "Healing / Support"},

    {"name": "Portal", "value": 10_000_000, "demand": 10,
     "rarity": "Legendary", "type": "Natural", "role": "Mobility / PvP"},

    {"name": "Blizzard", "value": 5_000_000, "demand": 5,
     "rarity": "Legendary", "type": "Elemental", "role": "Grinding / Sea Events"},

    {"name": "Lightning", "value": 40_000_000, "demand": 6,
     "rarity": "Legendary", "type": "Elemental", "role": "PvP"},

    {"name": "Pain", "value": 10_000_000, "demand": 5,
     "rarity": "Legendary", "type": "Natural", "role": "PvP"},

    {"name": "Mammoth", "value": 10_000_000, "demand": 5,
     "rarity": "Mythical", "type": "Beast", "role": "Sea Events / PvP"},

    {"name": "T-Rex", "value": 20_000_000, "demand": 8,
     "rarity": "Mythical", "type": "Beast", "role": "PvP / Grinding"},

    {"name": "Dough", "value": 30_000_000, "demand": 9,
     "rarity": "Mythical", "type": "Logia", "role": "PvP / Grinding"},

    {"name": "Shadow", "value": 10_000_000, "demand": 5,
     "rarity": "Mythical", "type": "Natural", "role": "PvP"},

    {"name": "Venom", "value": 20_000_000, "demand": 7,
     "rarity": "Mythical", "type": "Natural", "role": "PvP / Grinding"},

    {"name": "Control", "value": 170_000_000, "demand": 8,
     "rarity": "Mythical", "type": "Natural", "role": "Tactical PvP"},

    {"name": "Spirit", "value": 10_000_000, "demand": 7,
     "rarity": "Mythical", "type": "Natural", "role": "PvP"},

    {"name": "Gravity", "value": 10_000_000, "demand": 5,
     "rarity": "Mythical", "type": "Natural", "role": "Niche PvP"},

    {"name": "Tiger", "value": 140_000_000, "demand": 8,
     "rarity": "Mythical", "type": "Beast", "role": "PvP"},

    {"name": "Yeti", "value": 130_000_000, "demand": 7,
     "rarity": "Mythical", "type": "Beast", "role": "PvP / Grinding"},

    {"name": "Kitsune", "value": 660_000_000, "demand": 10,
     "rarity": "Mythical", "type": "Beast", "role": "All-Rounder"},

    {"name": "East Dragon", "value": 2_910_000_000, "demand": 7,
     "rarity": "Mythical", "type": "Beast", "role": "PvP"},

    {"name": "West Dragon", "value": 3_430_000_000, "demand": 9,
     "rarity": "Mythical", "type": "Beast", "role": "PvP"},

    {"name": "Gas", "value": 60_000_000, "demand": 8,
     "rarity": "Mythical", "type": "Elemental", "role": "PvP / Grinding"},
]


# =========================================================
# PERMANENTS
# =========================================================

PERMANENTS = [

    {"name": "Perm Dragon", "value": 10_240_000_000, "demand": 10, "robux": 5000},
    {"name": "Perm Kitsune", "value": 6_240_000_000, "demand": 10, "robux": 4000},
    {"name": "Perm Tiger", "value": 4_230_000_000, "demand": 9, "robux": 3000},
    {"name": "Perm Control", "value": 4_980_000_000, "demand": 8, "robux": 4000},
    {"name": "Perm Dough", "value": 4_755_000_000, "demand": 9.8, "robux": 2400},
    {"name": "Perm T-Rex", "value": 4_350_000_000, "demand": 9.2, "robux": 2350},
    {"name": "Perm Mammoth", "value": 3_330_000_000, "demand": 6, "robux": 2350},
    {"name": "Perm Spirit", "value": 3_410_000_000, "demand": 8, "robux": 2550},
    {"name": "Perm Venom", "value": 3_355_000_000, "demand": 7, "robux": 2450},
    {"name": "Perm Gravity", "value": 3_910_000_000, "demand": 8, "robux": 2300},
    {"name": "Perm Shadow", "value": 2_580_000_000, "demand": 6, "robux": 2425},
    {"name": "Perm Portal", "value": 2_900_000_000, "demand": 10, "robux": 2000},
    {"name": "Perm Buddha", "value": 2_800_000_000, "demand": 10, "robux": 1650},
    {"name": "Perm Rumble", "value": 2_000_000_000, "demand": 8.5, "robux": 2100},
    {"name": "Perm Magma", "value": 1_800_000_000, "demand": 8, "robux": 1300},
    {"name": "Perm Blizzard", "value": 1_500_000_000, "demand": 7.5, "robux": 2250},
    {"name": "Perm Sound", "value": 1_200_000_000, "demand": 6.5, "robux": 1900},
    {"name": "Perm Phoenix", "value": 1_100_000_000, "demand": 6, "robux": 2000},
    {"name": "Perm Quake", "value": 800_000_000, "demand": 3, "robux": 1500},
    {"name": "Perm Spider", "value": 800_000_000, "demand": 3, "robux": 1800},
]


# =========================================================
# LIMITEDS
# =========================================================

LIMITEDS = [

    {"name": "Galaxy Empyrean Kitsune", "value": 9_960_000_000, "demand": 10},
    {"name": "Purple Lightning", "value": 4_680_000_000, "demand": 8},
    {"name": "Super Spirit Pain", "value": 2_910_000_000, "demand": 8},
    {"name": "Red Lightning", "value": 2_610_000_000, "demand": 8},
    {"name": "Ember West Dragon", "value": 6_240_000_000, "demand": 9},
    {"name": "Fiend Yeti", "value": 990_000_000, "demand": 9},
    {"name": "Werewolf", "value": 1_110_000_000, "demand": 10},
    {"name": "Divine Portal", "value": 1_560_000_000, "demand": 10},
    {"name": "Dog Blade", "value": 750_000_000, "demand": 10},
    {"name": "Green Lightning", "value": 410_000_000, "demand": 7},
    {"name": "Yellow Lightning", "value": 770_000_000, "demand": 10},
    {"name": "Celestial Pain", "value": 930_000_000, "demand": 7},
    {"name": "Frustration Pain", "value": 980_000_000, "demand": 8},
    {"name": "Sadness Pain", "value": 860_000_000, "demand": 7},
    {"name": "Torment Pain", "value": 150_000_000, "demand": 6},
    {"name": "Thermite Bomb", "value": 540_000_000, "demand": 6},
    {"name": "Nuclear Bomb", "value": 600_000_000, "demand": 6},
    {"name": "Azura Bomb", "value": 220_000_000, "demand": 7},
    {"name": "Celebration Bomb", "value": 10_000_000, "demand": 4},
    {"name": "Rose Quartz Diamond", "value": 300_000_000, "demand": 7},
    {"name": "Emerald Diamond", "value": 220_000_000, "demand": 5},
    {"name": "Eagle Matrix", "value": 240_000_000, "demand": 5},
    {"name": "Eagle Requiem", "value": 150_000_000, "demand": 4},
    {"name": "Eagle Glacier", "value": 15_000_000, "demand": None},
    {"name": "Parrot Eagle", "value": 120_000_000, "demand": None},
    {"name": "Ruby Diamond", "value": 76_000_000, "demand": None},
    {"name": "Topaz Diamond", "value": 190_000_000, "demand": None},
    {"name": "Meme", "value": 741_000_000, "demand": None},
    {"name": "Eclipse", "value": 28_080_000_000, "demand": 10},
    {"name": "Matrix Eagle", "value": 640_000_000, "demand": None},
    {"name": "Requiem Eagle", "value": 150_000_000, "demand": 4},
    {"name": "Empyrean Kitsune", "value": 10_450_000_000, "demand": None},
]


# =========================================================
# GAMEPASSES
# =========================================================

GAMEPASSES = [

    {
        "name": "Extra Fruit Storage",
        "value": 490_000_000,
        "robux": 400,
        "demand": 9.8,
        "worthit": 10.0
    },

    {
        "name": "2x money",
        "value": 510_000_000,
        "robux": 450,
        "demand": 9.1,
        "worthit": 10
    },

    {
        "name": "2x Mastery",
        "value": 510_000_000,
        "robux": 450,
        "demand": 9.1,
        "worthit": 10
    },

    {
        "name": "Fruit Notifier",
        "value": 2_650_000_000,
        "robux": 2700,
        "demand": 8.7,
        "worthit": 4.0
    },

    {
        "name": "Dark Blade",
        "value": 985_000_000,
        "robux": 1300,
        "demand": 8.4,
        "worthit": 6.0
    },

    {
        "name": "2x Boss Drops",
        "value": 379_000_000,
        "robux": 350,
        "demand": 7.0,
        "worthit": 9.0
    },

    {
        "name": "Fast Boats",
        "value": 289_000_000,
        "robux": 350,
        "demand": 6.9,
        "worthit": 7.0
    }
]


# =========================================================
# COMBINE ITEMS
# =========================================================

def get_all_items():

    all_items = []

    for item in FRUITS:
        new_item = item.copy()
        new_item["category"] = "Fruit"
        all_items.append(new_item)

    for item in PERMANENTS:
        new_item = item.copy()
        new_item["category"] = "Permanent"
        all_items.append(new_item)

    for item in LIMITEDS:
        new_item = item.copy()
        new_item["category"] = "Limited"
        all_items.append(new_item)

    for item in GAMEPASSES:
        new_item = item.copy()
        new_item["category"] = "Gamepass"
        all_items.append(new_item)

    return all_items


# =========================================================
# SAFE FORMAT
# =========================================================

def safe_format_value(value):
    return format_value(value)


def safe_format_demand(value):
    return format_demand(value)


# =========================================================
# ORIGINAL VALUES BACKUP
# =========================================================

if "original_values" not in st.session_state:

    st.session_state.original_values = {}

    for item in FRUITS + PERMANENTS + LIMITEDS + GAMEPASSES:

        st.session_state.original_values[
            item["name"].lower()
        ] = {
            "value": item.get("value"),
            "demand": item.get("demand"),
            "worthit": item.get("worthit"),
            "robux": item.get("robux")
        }


# =========================================================
# SUPABASE
# =========================================================

def get_supabase_client():

    try:

        return create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    except Exception as e:

        st.error(
            "❌ Supabase is not configured.\n\n"
            "Add SUPABASE_URL and SUPABASE_KEY to Streamlit Secrets."
        )

        st.code(str(e))
        st.stop()


supabase = get_supabase_client()


# =========================================================
# DATABASE HELPERS
# =========================================================

def all_vault_items():
    return FRUITS + PERMANENTS + LIMITEDS + GAMEPASSES


def db_category(item):

    if item in FRUITS:
        return "fruit"

    if item in PERMANENTS:
        return "permanent"

    if item in LIMITEDS:
        return "limited"

    if item in GAMEPASSES:
        return "gamepass"

    return "unknown"


def seed_database_if_empty():

    try:

        result = (
            supabase
            .table("trading_items")
            .select("name")
            .execute()
        )

        existing_names = {
            str(row["name"]).strip().lower()
            for row in (result.data or [])
        }

        rows = []

        for item in all_vault_items():

            item_name = item["name"].strip().lower()

            if item_name not in existing_names:

                rows.append({
                    "name": item["name"],
                    "category": db_category(item),
                    "value": item.get("value"),
                    "demand": item.get("demand")
                })

        if rows:

            supabase \
                .table("trading_items") \
                .insert(rows) \
                .execute()

    except Exception as e:

        st.error(
            "❌ Could not initialize Trading Vault database."
        )

        st.code(str(e))
        st.stop()


def load_database_values():

    try:

        result = (
            supabase
            .table("trading_items")
            .select("name,value,demand")
            .execute()
        )

        rows = result.data or []

        db_items = {
            str(row["name"]).strip().lower(): row
            for row in rows
        }

        for item in all_vault_items():

            row = db_items.get(
                item["name"].strip().lower()
            )

            if row:

                if row.get("value") is not None:
                    item["value"] = row.get("value")

                item["demand"] = row.get("demand")

    except Exception as e:

        st.error(
            "❌ Could not load Trading Vault database."
        )

        st.code(str(e))
        st.stop()


def save_item_permanently(item):

    """
    Permanently save value and demand to Supabase.
    """

    result = (
        supabase
        .table("trading_items")
        .update({
            "value": item.get("value"),
            "demand": item.get("demand")
        })
        .eq("name", item["name"])
        .execute()
    )

    if not result.data:

        raise RuntimeError(
            f"No Supabase row was updated for '{item['name']}'. "
            f"Check that the item exists and your Supabase permissions allow UPDATE."
        )

    return True


def save_full_item_permanently(item):

    """
    Save all supported database fields.
    """

    data = {
        "value": item.get("value"),
        "demand": item.get("demand")
    }

    result = (
        supabase
        .table("trading_items")
        .update(data)
        .eq("name", item["name"])
        .execute()
    )

    if not result.data:

        raise RuntimeError(
            f"No Supabase row was updated for '{item['name']}'."
        )

    return True


def restore_original_permanently(item, original):

    item["value"] = original.get("value")
    item["demand"] = original.get("demand")

    save_item_permanently(item)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

seed_database_if_empty()
load_database_values()


# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.radio(
    "Category",
    [
        "🍎 Fruits",
        "♾️ Permanents",
        "🎟️ Gamepasses",
        "🏷️ Limiteds",
        "🤝 Trade Calculator",
        "📈 Market",
        "🤖 AI Assistant",
        "🔐 Admin Panel"
    ]
)

search = st.sidebar.text_input("🔎 Search")

sort_by = st.sidebar.selectbox(
    "Sort By",
    [
        "Highest Value",
        "Lowest Value",
        "Name"
    ]
)


# =========================================================
# SORT
# =========================================================

def sort_items(items, sort_by):

    if sort_by == "Highest Value":

        return sorted(
            items,
            key=lambda x: x.get("value") or 0,
            reverse=True
        )

    if sort_by == "Lowest Value":

        return sorted(
            items,
            key=lambda x: x.get("value") or 0
        )

    return sorted(
        items,
        key=lambda x: x.get("name", "").lower()
    )


# =========================================================
# FRUITS
# =========================================================

if page == "🍎 Fruits":

    st.header("🍎 Regular Fruits")

    items = FRUITS.copy()

    if search:

        items = [
            x for x in items
            if search.lower() in x["name"].lower()
        ]

    items = sort_items(items, sort_by)

    st.success(f"{len(items)} fruits loaded")

    for item in items:

        with st.container(border=True):

            c1, c2, c3 = st.columns([4, 2, 2])

            with c1:

                st.subheader(
                    f'🍎 {item["name"]}'
                )

                st.caption(
                    f'{item.get("rarity", "Unknown")} • '
                    f'{item.get("type", "Unknown")} • '
                    f'{item.get("role", "Unknown")}'
                )

            with c2:

                st.metric(
                    "Value",
                    format_value(item.get("value"))
                )

            with c3:

                st.metric(
                    "Demand",
                    format_demand(item.get("demand"))
                )


# =========================================================
# PERMANENTS
# =========================================================

elif page == "♾️ Permanents":

    st.header("♾️ Permanent Fruits")

    items = PERMANENTS.copy()

    if search:

        items = [
            x for x in items
            if search.lower() in x["name"].lower()
        ]

    items = sort_items(items, sort_by)

    st.success(
        f"{len(items)} permanent fruits loaded"
    )

    for item in items:

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(
                [4, 2, 2, 2]
            )

            with c1:

                st.subheader(
                    f'♾️ {item["name"]}'
                )

                st.caption("Permanent Fruit")

            with c2:

                st.metric(
                    "Perm Value",
                    format_value(item.get("value"))
                )

            with c3:

                st.metric(
                    "Demand",
                    format_demand(item.get("demand"))
                )

            with c4:

                robux = item.get("robux")

                st.metric(
                    "Robux",
                    f"{robux:,} R$"
                    if robux is not None
                    else "N/A"
                )


# =========================================================
# GAMEPASSES
# =========================================================

elif page == "🎟️ Gamepasses":

    st.header("🎟️ Gamepasses")

    st.caption(
        "Gamepass values, demand, Robux price and Worth It rating."
    )

    items = GAMEPASSES.copy()

    if search:

        items = [
            x for x in items
            if search.lower() in x["name"].lower()
        ]

    items = sort_items(items, sort_by)

    st.success(
        f"{len(items)} gamepasses loaded"
    )

    for item in items:

        with st.container(border=True):

            c1, c2, c3, c4, c5 = st.columns(
                [3.5, 1.5, 1.5, 1.5, 1.5]
            )

            with c1:

                st.subheader(
                    f'🎟️ {item["name"]}'
                )

                st.caption("Gamepass")

            with c2:

                st.metric(
                    "💎 Value",
                    format_value(item.get("value"))
                )

            with c3:

                st.metric(
                    "🔥 Demand",
                    format_demand(item.get("demand"))
                )

            with c4:

                st.metric(
                    "⭐ Worth It",
                    f'{item.get("worthit", "N/A")}/10'
                )

            with c5:

                st.metric(
                    "💰 Robux",
                    f'{item.get("robux", 0):,} R$'
                )


# =========================================================
# LIMITEDS
# =========================================================

elif page == "🏷️ Limiteds":

    st.header("🏷️ Limiteds")

    items = LIMITEDS.copy()

    if search:

        items = [
            x for x in items
            if search.lower() in x["name"].lower()
        ]

    items = sort_items(items, sort_by)

    st.success(
        f"{len(items)} limiteds loaded"
    )

    for item in items:

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(
                [4, 2, 2, 2]
            )

            with c1:

                st.subheader(
                    f'🏷️ {item["name"]}'
                )

                st.caption("Limited")

            with c2:

                st.metric(
                    "Value",
                    format_value(item.get("value"))
                )

            with c3:

                st.metric(
                    "Demand",
                    format_demand(item.get("demand"))
                )

            with c4:

                st.metric(
                    "Status",
                    "✅ Tradeable"
                )


# =========================================================
# TRADE CALCULATOR
# =========================================================

elif page == "🤝 Trade Calculator":

    st.header("🤝 Trade Calculator")

    st.caption(
        "Compare the total value of both sides of a trade."
    )

    if "your_trade" not in st.session_state:
        st.session_state.your_trade = []

    if "their_trade" not in st.session_state:
        st.session_state.their_trade = []

    trade_items = get_all_items()

    trade_options = [
        f'{item["name"]} • '
        f'{item["category"]} • '
        f'{format_value(item.get("value"))}'
        for item in trade_items
    ]

    left, right = st.columns(2)

    with left:

        st.subheader("🟦 Your Offer")

        your_selection = st.selectbox(
            "Select item",
            trade_options,
            key="your_trade_selection"
        )

        if st.button(
            "➕ Add to Your Offer",
            use_container_width=True
        ):

            index = trade_options.index(
                your_selection
            )

            st.session_state.your_trade.append(
                trade_items[index].copy()
            )

            st.rerun()

    with right:

        st.subheader("🟥 Their Offer")

        their_selection = st.selectbox(
            "Select item",
            trade_options,
            key="their_trade_selection"
        )

        if st.button(
            "➕ Add to Their Offer",
            use_container_width=True
        ):

            index = trade_options.index(
                their_selection
            )

            st.session_state.their_trade.append(
                trade_items[index].copy()
            )

            st.rerun()

    def trade_total(items):

        return sum(
            item.get("value") or 0
            for item in items
        )

    your_total = trade_total(
        st.session_state.your_trade
    )

    their_total = trade_total(
        st.session_state.their_trade
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🟦 Your Items")

        if not st.session_state.your_trade:

            st.info("No items added.")

        else:

            for i, item in enumerate(
                st.session_state.your_trade
            ):

                c1, c2 = st.columns([5, 1])

                with c1:

                    st.write(
                        f'**{item["name"]}**'
                    )

                    st.caption(
                        f'{item["category"]} • '
                        f'{format_value(item.get("value"))}'
                    )

                with c2:

                    if st.button(
                        "❌",
                        key=f"your_remove_{i}"
                    ):

                        st.session_state.your_trade.pop(i)
                        st.rerun()

        st.metric(
            "Your Total",
            format_value(your_total)
        )

    with right:

        st.subheader("🟥 Their Items")

        if not st.session_state.their_trade:

            st.info("No items added.")

        else:

            for i, item in enumerate(
                st.session_state.their_trade
            ):

                c1, c2 = st.columns([5, 1])

                with c1:

                    st.write(
                        f'**{item["name"]}**'
                    )

                    st.caption(
                        f'{item["category"]} • '
                        f'{format_value(item.get("value"))}'
                    )

                with c2:

                    if st.button(
                        "❌",
                        key=f"their_remove_{i}"
                    ):

                        st.session_state.their_trade.pop(i)
                        st.rerun()

        st.metric(
            "Their Total",
            format_value(their_total)
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🗑️ Clear Your Offer",
            use_container_width=True
        ):

            st.session_state.your_trade = []
            st.rerun()

    with c2:

        if st.button(
            "🗑️ Clear Their Offer",
            use_container_width=True
        ):

            st.session_state.their_trade = []
            st.rerun()

    if your_total > 0 and their_total > 0:

        difference = their_total - your_total

        percentage = (
            abs(difference) / your_total
        ) * 100

        st.divider()

        st.subheader("⚖️ Trade Result")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🟦 Your Value",
                format_value(your_total)
            )

        with c2:

            st.metric(
                "🟥 Their Value",
                format_value(their_total)
            )

        with c3:

            st.metric(
                "Difference",
                format_value(abs(difference))
            )

        if their_total > your_total:

            ratio = their_total / your_total

            if ratio >= 1.15:

                st.success(
                    "🏆 BIG WIN — You are receiving significantly more value!"
                )

            else:

                st.info(
                    "🟢 WIN — You are receiving more value."
                )

        elif your_total > their_total:

            ratio = your_total / their_total

            if ratio >= 1.15:

                st.error(
                    "❌ BIG LOSS — You are giving significantly more value!"
                )

            else:

                st.warning(
                    "🟡 SLIGHT LOSS — You are giving slightly more value."
                )

        else:

            st.success(
                "⚖️ FAIR TRADE — Both sides are equal!"
            )

        st.caption(
            f"Value difference: {percentage:.1f}%"
        )

    else:

        st.info(
            "Add at least one item to both sides."
        )


# =========================================================
# MARKET
# =========================================================

elif page == "📈 Market":

    st.header("📈 Market")

    st.caption(
        "Trading Vault market intelligence — value, demand and market signals."
    )

    market_items = get_all_items()

    valued_items = [
        x for x in market_items
        if x.get("value") is not None
    ]

    demanded_items = [
        x for x in market_items
        if x.get("demand") is not None
    ]

    st.subheader("📊 Market Overview")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Items Tracked",
            len(market_items)
        )

    with m2:

        st.metric(
            "Items With Values",
            len(valued_items)
        )

    with m3:

        if valued_items:

            highest = max(
                valued_items,
                key=lambda x: x["value"]
            )

            st.metric(
                "Highest Value",
                format_value(highest["value"])
            )

            st.caption(
                highest["name"]
            )

    with m4:

        if demanded_items:

            highest_demand = max(
                demanded_items,
                key=lambda x: x["demand"]
            )

            st.metric(
                "Highest Demand",
                format_demand(
                    highest_demand["demand"]
                )
            )

            st.caption(
                highest_demand["name"]
            )

    st.divider()

    st.subheader("💎 Highest Value Items")

    top_value = sorted(
        valued_items,
        key=lambda x: x["value"],
        reverse=True
    )[:10]

    for rank, item in enumerate(
        top_value,
        1
    ):

        c1, c2, c3 = st.columns([1, 5, 2])

        with c1:
            st.write(f"**#{rank}**")

        with c2:

            st.write(
                f'**{item["name"]}**'
            )

            st.caption(
                item["category"]
            )

        with c3:

            st.write(
                f'💰 **{format_value(item["value"])}**'
            )

    st.divider()

    st.subheader("🔥 Highest Demand")

    top_demand = sorted(
        demanded_items,
        key=lambda x: x["demand"],
        reverse=True
    )[:10]

    for rank, item in enumerate(
        top_demand,
        1
    ):

        c1, c2, c3 = st.columns([1, 5, 2])

        with c1:
            st.write(f"**#{rank}**")

        with c2:

            st.write(
                f'**{item["name"]}**'
            )

            st.caption(
                item["category"]
            )

        with c3:

            st.write(
                f'🔥 **{format_demand(item["demand"])}**'
            )

    st.divider()

    st.subheader("🔮 Market Signals")

    st.info(
        "These signals are based on current value and demand data. "
        "They are NOT historical price predictions."
    )

    potential_risers = [
        x for x in demanded_items
        if x["demand"] >= 8
    ]

    potential_risers = sorted(
        potential_risers,
        key=lambda x: (
            x["demand"],
            x.get("value") or 0
        ),
        reverse=True
    )[:10]

    potential_fallers = [
        x for x in demanded_items
        if x["demand"] <= 3
    ]

    potential_fallers = sorted(
        potential_fallers,
        key=lambda x: (
            x["demand"],
            -(x.get("value") or 0)
        )
    )[:10]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📈 Potential Risers")

        for item in potential_risers:

            st.write(
                f'🟢 **{item["name"]}**'
            )

            st.caption(
                f'Demand {format_demand(item["demand"])} • '
                f'Value {format_value(item["value"])}'
            )

    with col2:

        st.markdown("### 📉 Potential Fallers")

        for item in potential_fallers:

            st.write(
                f'🔴 **{item["name"]}**'
            )

            st.caption(
                f'Demand {format_demand(item["demand"])} • '
                f'Value {format_value(item["value"])}'
            )

    st.divider()

    st.subheader("⚠️ High Value / Low Demand")

    risky_items = [
        x for x in demanded_items
        if x["demand"] <= 4
    ]

    risky_items = sorted(
        risky_items,
        key=lambda x: x.get("value") or 0,
        reverse=True
    )[:10]

    if risky_items:

        for item in risky_items:

            st.write(
                f'⚠️ **{item["name"]}** — '
                f'{format_value(item["value"])} • '
                f'Demand {format_demand(item["demand"])}'
            )

    else:

        st.success(
            "No high-value / low-demand items detected."
        )

    st.divider()

    st.subheader("💎 High Demand / Lower Value")

    opportunity_items = [
        x for x in demanded_items
        if x["demand"] >= 7
    ]

    opportunity_items = sorted(
        opportunity_items,
        key=lambda x: x.get("value") or 0
    )[:10]

    for item in opportunity_items:

        st.write(
            f'💎 **{item["name"]}** — '
            f'{format_value(item["value"])} • '
            f'Demand {format_demand(item["demand"])}'
        )


# =========================================================
# AI ASSISTANT
# =========================================================

elif page == "🤖 AI Assistant":

    st.header("🤖 Trading Vault AI")

    st.caption(
        "Your Blox Fruits trading assistant — powered by your Vault data."
    )

    ai_items = []

    for item in FRUITS:

        ai_items.append({
            "name": item.get("name"),
            "category": "Regular Fruit",
            "value": item.get("value"),
            "demand": item.get("demand"),
            "rarity": item.get("rarity"),
            "type": item.get("type"),
            "role": item.get("role")
        })

    for item in PERMANENTS:

        ai_items.append({
            "name": item.get("name"),
            "category": "Permanent",
            "value": item.get("value"),
            "demand": item.get("demand"),
            "robux": item.get("robux")
        })

    for item in LIMITEDS:

        ai_items.append({
            "name": item.get("name"),
            "category": "Limited",
            "value": item.get("value"),
            "demand": item.get("demand")
        })

    for item in GAMEPASSES:

        ai_items.append({
            "name": item.get("name"),
            "category": "Gamepass",
            "value": item.get("value"),
            "demand": item.get("demand"),
            "robux": item.get("robux"),
            "worthit": item.get("worthit")
        })

    database_text = ""

    for item in ai_items:

        database_text += f"""
Name: {item.get("name")}
Category: {item.get("category")}
Value: {safe_format_value(item.get("value"))}
Demand: {safe_format_demand(item.get("demand"))}
"""

        if item.get("rarity"):
            database_text += f"Rarity: {item.get('rarity')}\n"

        if item.get("type"):
            database_text += f"Type: {item.get('type')}\n"

        if item.get("role"):
            database_text += f"Role: {item.get('role')}\n"

        if item.get("robux") is not None:
            database_text += f"Robux: {item.get('robux')}\n"

        if item.get("worthit") is not None:
            database_text += f"Worth It: {item.get('worthit')}/10\n"

        database_text += "\n"

    api_key = None

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

    except Exception:

        try:

            api_key = st.secrets["gemini"]["api_key"]

        except Exception:

            api_key = None

    if not api_key:

        st.error(
            "❌ Gemini API key is not configured."
        )

        st.info(
            "Add GEMINI_API_KEY to your Streamlit secrets."
        )

        st.code(
            'GEMINI_API_KEY = "YOUR_API_KEY_HERE"',
            language="toml"
        )

        st.stop()

    try:

        client = genai.Client(
            api_key=api_key
        )

    except Exception as e:

        st.error(
            f"❌ Could not connect to the AI service:\n\n{e}"
        )

        st.stop()

    if "ai_messages" not in st.session_state:

        st.session_state.ai_messages = []

    if not st.session_state.ai_messages:

        st.session_state.ai_messages.append({
            "role": "assistant",
            "content": (
                "👋 **Welcome to Trading Vault AI!**\n\n"
                "I can help you with:\n\n"
                "• 💰 Item values\n"
                "• 🔥 Demand\n"
                "• ⚖️ Trade advice\n"
                "• 📈 Market questions\n"
                "• 🔎 Finding items\n"
                "• 🤝 W/F/L analysis\n"
                "• 🧠 Trading strategies\n\n"
                "Ask me anything about your Vault!"
            )
        })

    for message in st.session_state.ai_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    user_prompt = st.chat_input(
        "Ask Trading Vault AI..."
    )

    if user_prompt:

        st.session_state.ai_messages.append({
            "role": "user",
            "content": user_prompt
        })

        with st.chat_message("user"):

            st.markdown(
                user_prompt
            )

        conversation = ""

        for message in st.session_state.ai_messages[-12:]:

            conversation += (
                f'{message["role"].upper()}: '
                f'{message["content"]}\n\n'
            )

        system_instruction = f"""
You are Trading Vault AI.

You are an expert assistant for Roblox Blox Fruits trading.

IMPORTANT RULES:

1. Use the Trading Vault database below for item values and demand.

2. NEVER invent an item's value if it exists in the database.

3. If an item is not in the database, clearly say:
"I don't have that item in the current Vault database."

4. Values are trading values, not Robux prices.

5. Demand is represented from 0 to 10.

6. When analyzing trades:
- Calculate total value of each side.
- Compare both sides.
- Explain whether the trade is WIN, FAIR, or LOSS.
- Mention demand when relevant.

7. Do not claim predictions are guaranteed.

8. Market predictions are estimates based on current data.

9. Do not pretend the Vault has historical prices unless historical data exists.

10. You are NOT the official Blox Fruits developer.

TRADING VAULT DATABASE:

{database_text}

CURRENT CONVERSATION:

{conversation}
"""

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 Trading Vault AI is thinking..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=(
                            system_instruction
                            + "\n\nUSER'S NEW QUESTION:\n"
                            + user_prompt
                        )
                    )

                    answer = response.text

                    st.markdown(
                        answer
                    )

            st.session_state.ai_messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error(
                "❌ AI request failed."
            )

            st.code(
                str(e)
            )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.ai_messages = []

            st.rerun()

    with c2:

        st.metric(
            "📦 Items Available to AI",
            len(ai_items)
        )


# =========================================================
# ADMIN PANEL
# =========================================================

elif page == "🔐 Admin Panel":

    st.header("🔐 Admin Panel")

    st.caption(
        "Trading Vault administrator controls."
    )

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:

        st.subheader("🔑 Administrator Login")

        password = st.text_input(
            "Admin Password",
            type="password",
            key="admin_password_input"
        )

        if st.button(
            "🔓 Login",
            use_container_width=True,
            key="admin_login_button"
        ):

            try:

                correct_password = st.secrets[
                    "ADMIN_PASSWORD"
                ]

                if password == correct_password:

                    st.session_state.admin_logged_in = True

                    st.session_state.pop(
                        "admin_password_input",
                        None
                    )

                    st.success(
                        "✅ Admin login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Incorrect admin password."
                    )

            except Exception:

                st.error(
                    "⚠️ ADMIN_PASSWORD is not configured "
                    "in Streamlit Secrets."
                )

    else:

        st.success(
            "🟢 Access Granted"
        )

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="admin_logout_button"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()

        st.divider()

        all_items = (
            FRUITS
            + PERMANENTS
            + LIMITEDS
            + GAMEPASSES
        )

        st.subheader("💻 Command Center")

        st.markdown(
            """
### Available commands

`/set ITEM VALUE`

`/set ITEM demand NUMBER`

`/set ITEM worthit NUMBER`

`/set ITEM robux NUMBER`

`/reset ITEM`

`/reset all`

### Examples

`/set Kitsune 700M`

`/set Kitsune demand 9`

`/set Extra Fruit Storage 500M`

`/set Extra Fruit Storage demand 9.8`

`/set Extra Fruit Storage worthit 10`

`/set Extra Fruit Storage robux 400`

`/reset Kitsune`

`/reset all`
"""
        )

        command = st.text_input(
            "Enter admin command",
            placeholder="/set Kitsune 700M",
            key="admin_command_input"
        )

        if st.button(
            "⚡ Execute Command",
            use_container_width=True,
            key="execute_admin_command"
        ):

            command = command.strip()

            if not command:

                st.warning(
                    "Enter a command first."
                )

            else:

                parts = command.split()

                command_name = parts[0].lower()

                # =================================================
                # SET COMMAND
                # =================================================

                if command_name == "/set":

                    if len(parts) < 3:

                        st.error(
                            "❌ Invalid command."
                        )

                    else:

                        property_name = None

                        if (
                            len(parts) >= 4
                            and parts[-2].lower()
                            in [
                                "demand",
                                "worthit",
                                "robux"
                            ]
                        ):

                            property_name = (
                                parts[-2].lower()
                            )

                            item_name = " ".join(
                                parts[1:-2]
                            ).strip()

                            value_text = parts[-1].strip()

                        else:

                            property_name = "value"

                            item_name = " ".join(
                                parts[1:-1]
                            ).strip()

                            value_text = parts[-1].strip()

                        item = None

                        for x in all_items:

                            if (
                                x.get("name", "").lower()
                                == item_name.lower()
                            ):

                                item = x
                                break

                        if item is None:

                            st.error(
                                f"❌ Item not found: {item_name}"
                            )

                        else:

                            item_key = item["name"].lower()

                            if property_name == "demand":

                                try:

                                    new_demand = float(
                                        value_text
                                    )

                                    if not (
                                        0 <= new_demand <= 10
                                    ):

                                        st.error(
                                            "❌ Demand must be between 0 and 10."
                                        )

                                    else:

                                        old_demand = item.get(
                                            "demand"
                                        )

                                        item["demand"] = new_demand

                                        # SAVE TO SUPABASE
                                        save_item_permanently(item)

                                        st.success(
                                            f"✅ {item['name']} demand permanently "
                                            f"changed from {format_demand(old_demand)} "
                                            f"to {format_demand(new_demand)}."
                                        )

                                        st.rerun()

                                except ValueError:

                                    st.error(
                                        "❌ Demand must be a number from 0 to 10."
                                    )

                                except Exception as e:

                                    st.error(
                                        "❌ Demand was NOT saved to Supabase."
                                    )

                                    st.code(str(e))

                            elif property_name == "worthit":

                                try:

                                    new_worthit = float(
                                        value_text
                                    )

                                    if not (
                                        0 <= new_worthit <= 10
                                    ):

                                        st.error(
                                            "❌ Worth It must be between 0 and 10."
                                        )

                                    else:

                                        # NOTE:
                                        # Current trading_items table does not
                                        # contain a worthit column.
                                        #
                                        # We update the local app value here.
                                        # To make worthit permanent, add a
                                        # worthit column to Supabase.

                                        item["worthit"] = new_worthit

                                        st.success(
                                            f"✅ {item['name']} Worth It updated "
                                            f"for this app session."
                                        )

                                        st.info(
                                            "ℹ️ Worth It is not stored in the "
                                            "current trading_items table."
                                        )

                                        st.rerun()

                                except ValueError:

                                    st.error(
                                        "❌ Worth It must be a number from 0 to 10."
                                    )

                            elif property_name == "robux":

                                try:

                                    new_robux = int(
                                        float(value_text)
                                    )

                                    if new_robux < 0:

                                        st.error(
                                            "❌ Robux price cannot be negative."
                                        )

                                    else:

                                        # NOTE:
                                        # Current trading_items table does not
                                        # contain a robux column.

                                        item["robux"] = new_robux

                                        st.success(
                                            f"✅ {item['name']} Robux updated "
                                            f"for this app session."
                                        )

                                        st.info(
                                            "ℹ️ Robux is not stored in the "
                                            "current trading_items table."
                                        )

                                        st.rerun()

                                except ValueError:

                                    st.error(
                                        "❌ Robux price must be a number."
                                    )

                            else:

                                try:

                                    value_text = (
                                        value_text
                                        .upper()
                                        .replace(",", "")
                                        .strip()
                                    )

                                    multiplier = 1

                                    if value_text.endswith("B"):

                                        multiplier = 1_000_000_000
                                        number = value_text[:-1]

                                    elif value_text.endswith("M"):

                                        multiplier = 1_000_000
                                        number = value_text[:-1]

                                    elif value_text.endswith("K"):

                                        multiplier = 1_000
                                        number = value_text[:-1]

                                    else:

                                        number = value_text

                                    new_value = int(
                                        float(number)
                                        * multiplier
                                    )

                                    if new_value < 0:

                                        st.error(
                                            "❌ Value cannot be negative."
                                        )

                                    else:

                                        old_value = item.get(
                                            "value"
                                        )

                                        item["value"] = new_value

                                        # =====================================
                                        # PERMANENT SUPABASE SAVE
                                        # =====================================

                                        save_item_permanently(item)

                                        st.success(
                                            f"✅ {item['name']} value PERMANENTLY "
                                            f"saved to Supabase!"
                                        )

                                        st.write(
                                            f"Old Value: "
                                            f"**{safe_format_value(old_value)}**"
                                        )

                                        st.write(
                                            f"New Value: "
                                            f"**{safe_format_value(new_value)}**"
                                        )

                                        st.rerun()

                                except ValueError:

                                    st.error(
                                        "❌ Invalid value."
                                    )

                                    st.info(
                                        "Examples: `700M`, `2.5B`, `500K`"
                                    )

                                except Exception as e:

                                    st.error(
                                        "❌ VALUE WAS NOT SAVED TO SUPABASE."
                                    )

                                    st.code(str(e))

                # =================================================
                # RESET COMMAND
                # =================================================

                elif command_name == "/reset":

                    if len(parts) < 2:

                        st.error(
                            "❌ Usage: /reset ITEM or /reset all"
                        )

                    elif (
                        len(parts) == 2
                        and parts[1].lower() == "all"
                    ):

                        reset_errors = []

                        for item in all_items:

                            original = (
                                st.session_state.original_values
                                .get(item["name"].lower())
                            )

                            if original:

                                item["value"] = original.get("value")
                                item["demand"] = original.get("demand")

                                try:

                                    save_item_permanently(item)

                                except Exception as e:

                                    reset_errors.append(
                                        f"{item['name']}: {e}"
                                    )

                        if reset_errors:

                            st.error(
                                "❌ Some items could not be reset."
                            )

                            st.code(
                                "\n".join(reset_errors)
                            )

                        else:

                            st.success(
                                "✅ ALL values and demand have been "
                                "PERMANENTLY reset in Supabase."
                            )

                        st.rerun()

                    else:

                        item_name = " ".join(
                            parts[1:]
                        ).strip()

                        item = None

                        for x in all_items:

                            if (
                                x.get("name", "").lower()
                                == item_name.lower()
                            ):

                                item = x
                                break

                        if item is None:

                            st.error(
                                f"❌ Item not found: {item_name}"
                            )

                        else:

                            item_key = item["name"].lower()

                            original = (
                                st.session_state.original_values
                                .get(item_key)
                            )

                            if original is None:

                                st.error(
                                    "❌ No original backup exists."
                                )

                            else:

                                try:

                                    old_value = item.get("value")
                                    old_demand = item.get("demand")

                                    item["value"] = original.get(
                                        "value"
                                    )

                                    item["demand"] = original.get(
                                        "demand"
                                    )

                                    # =====================================
                                    # PERMANENT RESET
                                    # =====================================

                                    save_item_permanently(item)

                                    st.success(
                                        f"✅ {item['name']} has been "
                                        f"PERMANENTLY reset in Supabase!"
                                    )

                                    st.write(
                                        f"Value: "
                                        f"**{safe_format_value(old_value)}** "
                                        f"→ "
                                        f"**{safe_format_value(item['value'])}**"
                                    )

                                    st.write(
                                        f"Demand: "
                                        f"**{safe_format_demand(old_demand)}** "
                                        f"→ "
                                        f"**{safe_format_demand(item['demand'])}**"
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"❌ {item['name']} was NOT reset "
                                        f"in Supabase."
                                    )

                                    st.code(str(e))

                else:

                    st.error(
                        f"❌ Unknown command: {command_name}"
                    )

                    st.info(
                        "Available commands: `/set` and `/reset`"
                    )

        # =====================================================
        # DATABASE TEST
        # =====================================================

        st.divider()

        st.subheader("🗄️ Database Status")

        if st.button(
            "🔄 Test Supabase Connection",
            use_container_width=True
        ):

            try:

                test = (
                    supabase
                    .table("trading_items")
                    .select("name,value,demand")
                    .limit(1)
                    .execute()
                )

                if test.data:

                    st.success(
                        "🟢 Supabase connected successfully."
                    )

                    st.json(test.data[0])

                else:

                    st.warning(
                        "⚠️ Supabase connected, but the table is empty."
                    )

            except Exception as e:

                st.error(
                    "🔴 Supabase connection/query failed."
                )

                st.code(str(e))

        # =====================================================
        # STATUS
        # =====================================================

        st.divider()

        st.subheader("📊 Admin Status")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Items",
                len(all_items)
            )

        with c2:

            valued = [
                x for x in all_items
                if x.get("value") is not None
            ]

            st.metric(
                "With Values",
                len(valued)
            )

        with c3:

            demanded = [
                x for x in all_items
                if x.get("demand") is not None
            ]

            st.metric(
                "With Demand",
                len(demanded)
            )

        # =====================================================
        # ACTIVE CHANGES
        # =====================================================

        st.divider()

        st.subheader("📝 Database Values")

        try:

            db_result = (
                supabase
                .table("trading_items")
                .select("name,category,value,demand")
                .order("name")
                .execute()
            )

            db_rows = db_result.data or []

            st.caption(
                f"{len(db_rows)} items currently stored in Supabase."
            )

            for row in db_rows:

                st.write(
                    f'**{row["name"]}** — '
                    f'{row.get("category", "N/A")} • '
                    f'💰 {safe_format_value(row.get("value"))} • '
                    f'🔥 {safe_format_demand(row.get("demand"))}'
                )

        except Exception as e:

            st.error(
                "Could not read database values."
            )

            st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Trading Vault V3.4 • Values are market estimates and can change."
)