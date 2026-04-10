# Curated regions with per-region event counts.
# Civilizations with longer/richer recorded history get higher counts.

MAJOR_REGIONS: list[tuple[str, str, str, int]] = [
    # Europe
    ("Ancient Greece",          "600 BCE - 146 BCE",  "Ancient Greece",        10),
    ("Roman Empire",            "500 BCE - 476 CE",   "Roman Empire",          16),
    ("Byzantine Empire",        "330 CE - 1453 CE",   "Byzantine Empire",      10),
    ("Medieval Western Europe", "600 CE - 1500 CE",   "Medieval Europe",       10),
    ("British History",         "600 CE - 2026 CE",   "Britain",               24),
    ("French History",          "600 CE - 2026 CE",   "France",                22),
    ("German History",          "800 CE - 2026 CE",   "Germany",               22),
    ("Spanish History",         "700 CE - 2026 CE",   "Spain",                 18),
    ("Portuguese History",      "1100 CE - 2026 CE",  "Portugal",              10),
    ("Italian History",         "1300 CE - 2026 CE",  "Italy",                 12),
    ("Russian History",         "800 CE - 2026 CE",   "Russia",                22),
    ("Scandinavian History",    "793 CE - 2026 CE",   "Scandinavia",           10),
    ("Polish History",          "966 CE - 2026 CE",   "Poland",                10),
    ("Dutch History",           "1500 CE - 2026 CE",  "Netherlands",            8),
    ("Modern Europe",           "1800 CE - 2026 CE",  "Modern Europe",         12),

    # Middle East & North Africa
    ("Ancient Egypt",           "600 BCE - 30 BCE",   "Ancient Egypt",          8),
    ("Persian Empire",          "600 BCE - 330 BCE",  "Persian Empire",         8),
    ("Iran History",            "330 BCE - 2026 CE",  "Iran/Persia",           20),
    ("Arabian Peninsula",       "600 CE - 2026 CE",   "Arabia & Saudi Arabia", 10),
    ("Islamic Caliphates",      "622 CE - 1258 CE",   "Islamic Caliphates",    10),
    ("Ottoman Empire",          "1299 CE - 1922 CE",  "Ottoman Empire",        12),
    ("Modern Turkey",           "1923 CE - 2026 CE",  "Turkey",                 8),
    ("Modern Middle East",      "1900 CE - 2026 CE",  "Modern Middle East",    12),
    ("Egypt Modern History",    "600 CE - 2026 CE",   "Egypt",                 14),

    # South Asia
    ("Classical India",         "600 BCE - 550 CE",   "Classical India",       10),
    ("Medieval India",          "550 CE - 1526 CE",   "Medieval India",        10),
    ("Mughal Empire",           "1526 CE - 1857 CE",  "Mughal Empire",         10),
    ("Modern India",            "1857 CE - 2026 CE",  "Modern India",          18),
    ("Pakistan & Bangladesh",   "1947 CE - 2026 CE",  "Pakistan & Bangladesh",  8),

    # East Asia
    ("Ancient China",           "600 BCE - 221 BCE",  "Ancient China",         10),
    ("Imperial China Early",    "221 BCE - 618 CE",   "Imperial China I",      12),
    ("Tang & Song Dynasties",   "618 CE - 1279 CE",   "Tang & Song",           12),
    ("Ming & Qing Dynasties",   "1368 CE - 1912 CE",  "Ming & Qing",           18),
    ("Modern China",            "1912 CE - 2026 CE",  "Modern China",          18),
    ("Feudal Japan",            "600 CE - 1868 CE",   "Feudal Japan",          12),
    ("Modern Japan",            "1868 CE - 2026 CE",  "Modern Japan",          16),
    ("Korean History",          "600 BCE - 2026 CE",  "Korea",                 10),
    ("Vietnam History",         "200 BCE - 2026 CE",  "Vietnam",               10),

    # Southeast Asia
    ("Khmer Empire",            "802 CE - 1431 CE",   "Khmer Empire",           8),
    ("Southeast Asia",          "1400 CE - 2026 CE",  "Southeast Asia",        10),
    ("Indonesia History",       "600 CE - 2026 CE",   "Indonesia",             10),
    ("Philippines History",     "900 CE - 2026 CE",   "Philippines",            8),

    # Central Asia
    ("Mongol Empire",           "1206 CE - 1368 CE",  "Mongol Empire",          8),
    ("Silk Road Civilizations", "600 BCE - 1450 CE",  "Silk Road",              8),

    # Sub-Saharan Africa
    ("Ethiopian History",       "100 CE - 2026 CE",   "Ethiopia",              10),
    ("West African Empires",    "600 CE - 1600 CE",   "West Africa",            8),
    ("Nigeria History",         "1000 CE - 2026 CE",  "Nigeria",                8),
    ("East Africa",             "600 CE - 2026 CE",   "East Africa",            8),
    ("South Africa History",    "1652 CE - 2026 CE",  "South Africa",          10),
    ("Modern Africa",           "1800 CE - 2026 CE",  "Modern Africa",         10),

    # Americas
    ("Mesoamerica",             "600 BCE - 900 CE",   "Mesoamerica",            8),
    ("Aztec Empire",            "1300 CE - 1521 CE",  "Aztec Empire",           8),
    ("Inca Empire",             "1438 CE - 1572 CE",  "Inca Empire",            8),
    ("United States History",   "1600 CE - 2026 CE",  "United States",         28),
    ("Canadian History",        "1534 CE - 2026 CE",  "Canada",                 8),
    ("Brazilian History",       "1500 CE - 2026 CE",  "Brazil",                10),
    ("Argentine History",       "1516 CE - 2026 CE",  "Argentina",              8),
    ("Latin America",           "1500 CE - 2026 CE",  "Latin America",         10),

    # Oceania
    ("Polynesian Expansion",    "600 CE - 1300 CE",   "Polynesian Expansion",   6),
    ("Australia & Pacific",     "1788 CE - 2026 CE",  "Australia & Pacific",    8),

    # Global
    ("World Wars & Cold War",   "1900 CE - 1991 CE",  "World Wars & Cold War", 16),
    ("Contemporary World",      "1991 CE - 2026 CE",  "Contemporary World",    12),
    ("Global Pandemics",        "541 CE - 2026 CE",   "Pandemics",             10),
    ("Natural Disasters",       "600 BCE - 2026 CE",  "Natural Disasters",     10),
]
