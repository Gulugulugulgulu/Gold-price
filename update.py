"""Fetch Mathura gold rates from Business Today and merge them into data.json."""
import json, re, sys, urllib.request
from datetime import datetime

URL = "https://www.businesstoday.in/commodity/gold-rate-in-mathura-today"

def num(s):
    return int(s.replace(",", ""))

def day(s):
    return datetime.strptime(s.replace("Sept", "Sep"), "%b %d, %Y").strftime("%Y-%m-%d")

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text.replace("|", " "))

found = {}

for d, k22, k24 in re.findall(
        r"([A-Z][a-z]{2,3} \d{1,2}, 20\d\d) ₹\s?([\d,]+) \d+ ₹\s?([\d,]+) \d+", text):
    found[day(d)] = {"date": day(d), "k24": num(k24), "k22": num(k22)}

m = re.search(r"on \w+, ([A-Z][a-z]{2,3} \d{1,2}, 20\d\d) ?: Today, the price of 24-carat "
              r"Gold in Mathura is ₹\s?([\d,]+)", text)
c = re.search(r"Mathura ₹\s?([\d,]+) ₹\s?([\d,]+)", text)
if m and c:
    found[day(m.group(1))] = {"date": day(m.group(1)), "k24": num(m.group(2)), "k22": num(c.group(1))}

if not found:
        raise SystemExit("Could not read any rates")
