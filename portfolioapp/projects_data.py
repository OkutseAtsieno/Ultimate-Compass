"""
Content for the three Projects pages.

To add a project: copy one of the dicts below into the right list (cv / ml / apps) and fill it in.
Nothing else needs to change, the page picks it up automatically.

Videos
------
Put the file in  portfolioapp/static/videos/  and set  'video': 'videos/yourfile.mp4'
(MP4 / H.264 plays everywhere. Keep each clip under ~20 MB, see the README note).
Or, for a long video, upload it to YouTube (unlisted is fine) and set
'youtube_id': 'XXXXXXXXXXX'  (the part after v= in the URL) instead of 'video'.
If the video file is not found yet, the page shows the poster image with a
"demo coming soon" label instead of a broken player.

Screenshot ('screenshot': 'file.png') shows one full-width image, best for dashboards.
Gallery images (e.g. more Power BI screenshots)
-----------------------------------------
Put the files in  portfolioapp/static/  and list them in 'images', e.g.
'images': ['sales_dashboard_1.png', 'sales_dashboard_2.png']
"""

# ---------------------------------------------------------------------------
# Sections of the single Projects page, in the order they appear.
# 'key' must match a key in PROJECTS below. 'anchor' is the #link used in the URL.
# ---------------------------------------------------------------------------
SECTIONS = [
    {
        "key": "cv",
        "anchor": "cv",
        "title": "Computer Vision",
        "intro": (
            "Detection, tracking and analysis of objects in images and video, "
            "from sports analytics to automated inspection."
        ),
    },
    {
        "key": "ml",
        "anchor": "predictive",
        "title": "Machine Learning",
        "intro": (
            "Predictive models for forecasting, classification and risk scoring, "
            "built to be accurate and explainable."
        ),
    },
    {
        "key": "apps",
        "anchor": "dashboards",
        "title": "Dashboards & Web Apps",
        "intro": (
            "Full-stack web platforms and interactive dashboards that turn "
            "raw data into something people can use every day."
        ),
    },
]

PAGE_INTRO = (
    "Selected work across computer vision, machine learning and analytics."
)

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
PROJECTS = {
    # ----------------------------- Computer Vision -----------------------------
    "cv": [
        {
            "title": "AI Football Coach",
            "tagline": "Match video turned into coach-ready insight",
            "status": "Working demo",
            "summary": (
                "A computer-vision pipeline that watches match video, tracks "
                "every player and the ball, converts positions to real pitch "
                "metres, and turns the movement into coach-ready insight: "
                "distance and high-speed running, team shape, heat maps, "
                "passes, duels and turnovers, and written coach notes whose "
                "every number is checked against the data. The goal is an "
                "affordable tool for academies and clubs that cannot pay for "
                "international analysis platforms, working on ordinary "
                "footage. The demo analyses a 30-second clip; positions are "
                "accurate to roughly 1 m."
            ),
            "tags": [
                "YOLOv8x", "ByteTrack", "OpenCV", "Python",
                "Django", "Plotly", "Sports Analytics",
            ],
            "highlights": [],
            "metrics": [
                {"label": "Position accuracy", "value": "~1 m"},
                {"label": "Demo clip analysed", "value": "30 s"},
            ],
            # Progress shown as a pipeline. state: done | progress | planned
            "pipeline": [
                {"step": "Player and ball detection (YOLOv8x)", "state": "done"},
                {"step": "Multi-object tracking (ByteTrack)", "state": "done"},
                {"step": "Team assignment from kit colour", "state": "done"},
                {"step": "Pitch calibration (pixels to metres)", "state": "done"},
                {"step": "Metrics: distance, speed, heat maps, team shape", "state": "done"},
                {"step": "Passes, duels and turnovers from ball possession", "state": "done"},
                {"step": "Coach notes with every number checked against the data", "state": "done"},
                {"step": "Interactive web dashboard (live demo)", "state": "done"},
                {"step": "Detector fine-tuned on local match footage", "state": "planned"},
                {"step": "Power BI report", "state": "planned"},
                {"step": "Full-match processing and video upload", "state": "planned"},
                {"step": "Swahili coach notes", "state": "planned"},
            ],
            # Drop your clip in portfolioapp/static/videos/ with this name,
            # or change the name here.
            "video": "videos/football_tracking.mp4",
            "poster": "thumbs/football.jpg",
            "youtube_id": "",
            "images": [],
            "links": [{"label": "Open the live demo", "url": "/football/"}],
        },
        {
            "title": "Maize Leaf Disease Detection",
            "tagline": "Upload a leaf photo, get the disease and a recommendation",
            "status": "Completed",
            "summary": (
                "A web app where a farmer uploads a photo of a maize leaf and "
                "the model classifies it as leaf rust, leaf spot, leaf blight or "
                "healthy. It shows a confidence score for every class, then "
                "gives a recommendation and seasonal context for what to do "
                "next. Built for smallholder farming, where catching disease "
                "early protects the harvest and an agronomist is not always "
                "within reach."
            ),
            "tags": ["Computer Vision", "Deep Learning", "Django", "Python", "Agriculture"],
            "metrics": [{"label": "Accuracy", "value": "81%"}],
            "highlights": [],
            "pipeline": [],
            "video": "videos/maize_leaf_disease.mp4",
            "poster": "",
            "youtube_id": "",
            "images": [],
            "links": [],
        },
    ],

    # ------------------------------ Machine Learning ---------------------------
    # Add your predictive-modelling projects here. Example (delete the leading #):
    #
    # {
    #     "title": "Customer Churn Prediction",
    #     "tagline": "Which customers are likely to leave, and why",
    #     "status": "Completed",
    #     "summary": "One short paragraph: the problem, your approach, the result.",
    #     "tags": ["scikit-learn", "XGBoost", "SHAP"],
    #     "highlights": ["What you built", "How well it performed", "What changed because of it"],
    #     "pipeline": [],
    #     "video": "",
    #     "poster": "",
    #     "youtube_id": "",
    #     "images": ["churn_results.png"],
    #     "links": [{"label": "GitHub", "url": "https://github.com/..."}],
    # },
    "ml": [
        {
            "title": "House Price Prediction (Kenya)",
            "tagline": "Estimate a property's price from location, size and type",
            "status": "Completed",
            "summary": (
                "A machine-learning model, served through a Django web app, "
                "that predicts a property's price in Kenya shillings. The user "
                "picks a location, the number of bedrooms and the property "
                "type (villa or townhouse) and gets an instant estimate. "
                "Locations are encoded by their average price, and unseen "
                "locations fall back to the overall average."
            ),
            "tags": ["Regression", "Django", "Feature Engineering", "Python", "Real Estate"],
            "metrics": [{"label": "R² score", "value": "0.79"}],
            "highlights": [],
            "pipeline": [],
            "video": "videos/house_price_prediction.mp4",
            "poster": "",
            "youtube_id": "",
            "images": [],
            "links": [],
        },
    ],

    # --------------------------- Power BI & Dashboards -------------------------
    # Same format as above. Use 'images' for dashboard screenshots.
    "apps": [
        {
            "title": "Athlete Tracker",
            "tagline": "Discover talent. Track progress.",
            "status": "Working prototype",
            "summary": (
                "A full-stack Django platform for scouting and monitoring "
                "athlete development, from a first assessment to the next "
                "level. Coaches sign in, create teams, search for or register "
                "athletes, and record physical assessments: body measurements "
                "with automatic BMI, power and strength tests, and performance "
                "remarks calculated for them. Three workspaces keep the work "
                "organised: Scouting, Performance and Coaches."
            ),
            "tags": ["Django", "Python", "Authentication", "Database design", "Sports Analytics"],
            "highlights": [],
            "pipeline": [],
            "video": "videos/athlete_tracker.mp4",
            "poster": "",
            "youtube_id": "",
            "images": [],
            "links": [],
        },
        {
            "title": "Athlete Performance Dashboard",
            "tagline": "A coach's one-page view of a squad's fitness",
            "status": "Completed",
            "summary": (
                "A Power BI dashboard that summarises fitness assessments for a "
                "squad of 20 athletes. The top row profiles the group (age, "
                "weight, height). Below it, tests are grouped into Strength and "
                "Balance (push-ups, pull-ups, vertical jump, stork stand) and "
                "Speed and Agility (T-test, beep test, 30 m sprint), and a chart "
                "shows how many athletes fall into each overall result band. A "
                "gender and athlete slicer lets a coach drill down to one "
                "athlete's overall score. Athlete names are removed for privacy."
            ),
            "tags": ["Power BI", "DAX", "Data Modelling", "KPI Cards", "Sports Analytics"],
            "metrics": [
                {"label": "Athletes", "value": "20"},
                {"label": "Avg overall score", "value": "66.66"},
            ],
            "highlights": [],
            "pipeline": [],
            "video": "",
            "poster": "",
            "youtube_id": "",
            "screenshot": "powerbi_athlete_dashboard.png",
            "images": [],
            "links": [],
        },
    ],
}