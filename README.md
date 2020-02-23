# COVID-19_RMDS

This module is to scrape media articles about Coronavirus disease 2019 (COVID-19).

I didn't find good free google news API, so currently I use a scraper to do this. As expected, the scraper is slower
and may crash at certain scenarios.

The module returns a list of dictionaries, including items:
source
title
content
url link
publish time
city