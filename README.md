# MyBrain: AI-Powered Second Memory Project for Note-Keeping

MyBrain is the solution we proposed and developed during the [Winter School Generative AI Hackathon](https://midas.centrale-casablanca.net/winter-school-2024-generative-ai/).

The project's goal is to host the user's saved notes from various sources and different formats, organize them, enable interaction, generate insights, and cluster notes with similar relevance into semantic spaces.

## MyBrain Architecture
![MyBrain Architecture](https://github.com/khoubrane-yousef/MyBrain/blob/main/Architecture.png)

This repository contains two files:

- [Extracting_bookmarks_from_Reddit.py](https://github.com/khoubrane-yousef/MyBrain/blob/main/Extracting_bookmarks_from_Reddit.py): An example of using a website's API to retrieve the user's saved bookmarks. The code was adapted from this [repo](https://github.com/AlkTheOrg/reddit-saved-to-csv/).

- [Insight_generation.ipynb](https://github.com/khoubrane-yousef/MyBrain/blob/main/Insight_generation.ipynb): Generates insights from bookmarks extracted from Reddit and other notes issued from additional URLs. (This covers the upper block in the previous architecture graph).
