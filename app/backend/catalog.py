"""Product-owned restaurant and table catalog for GlobalBites."""

RESTAURANTS = {
    1: {"name": "Swiss Butter", "cuisine": "Lebanese", "location": "Jal El Dib Main Road, Jal el Dib"},
    2: {"name": "Al Shams", "cuisine": "Lebanese", "location": "Haouch Moussa, Anjar, Bekaa Valley"},
    3: {"name": "Amaleen", "cuisine": "Lebanese", "location": "Cascada Mall Lakeside, Taanayel"},
    4: {"name": "Totori", "cuisine": "Chinese", "location": "513, Mir Omar, Clemenceau, Beirut"},
    5: {"name": "Chop Suey", "cuisine": "Chinese", "location": "Jounieh - Beirut Hwy, Dbayeh"},
    6: {"name": "Alma Beirut", "cuisine": "Mexican", "location": "Bossa Nova Hotel, Charles Helou, Beirut"},
    7: {"name": "Papa's Mia Tacos", "cuisine": "Mexican", "location": "Beirut"},
    8: {"name": "Momaki", "cuisine": "Japanese", "location": "Dbayeh"},
    9: {"name": "Kami", "cuisine": "Japanese", "location": "Main Road, Byblos"},
    10: {"name": "Appetito Trattoria", "cuisine": "Italian", "location": "Pasteur Street, Beirut"},
    11: {"name": "Pertutti", "cuisine": "Italian", "location": "Martakla, Baabda"},
}

TABLES = {
    "T1": {"seating_type": "indoor", "capacity": 2},
    "T2": {"seating_type": "indoor", "capacity": 4},
    "T3": {"seating_type": "indoor", "capacity": 4},
    "T4": {"seating_type": "indoor", "capacity": 2},
    "O1": {"seating_type": "outdoor", "capacity": 2},
    "O2": {"seating_type": "outdoor", "capacity": 4},
}

ALLOWED_TIMES = {
    "12:00", "12:30", "13:00", "13:30", "14:00",
    "18:00", "18:30", "19:00", "19:30", "20:00",
    "20:30", "21:00", "21:30", "22:00",
}

ACTIVE_RESERVATION_STATUSES = {"PENDING", "CONFIRMED"}
ALL_RESERVATION_STATUSES = {"PENDING", "CONFIRMED", "COMPLETED", "CANCELLED"}
