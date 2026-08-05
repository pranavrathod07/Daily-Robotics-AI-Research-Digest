# 🤖 Daily Autonomous Robotics & AI Research Scraper

[![Robotics Research Pipeline](https://github.com/pranavrathod07/Daily-Robotics-AI-Research-Digest/actions/workflows/daily_digest.yml/badge.svg)](https://github.com/pranavrathod07/Daily-Robotics-AI-Research-Digest/actions/workflows/daily_digest.yml)
![Python Version](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Automation Engine](https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Domain](https://img.shields.io/badge/Domain-Robotics_%26_AI-FF6F00?style=flat)
![License](https://img.shields.io/badge/License-MIT-green.style=flat)

An automated, cloud-based research pipeline that continuously scrapes, parses, and logs the latest pre-print papers in **Robotics (`cs.RO`)** and **Artificial Intelligence (`cs.AI`)** directly from the **ArXiv API**. 

Powered by **Python** and scheduled via **GitHub Actions CI/CD workflows**, this engine executes 3 times daily to generate monthly research logs without human intervention or dedicated server overhead.

---

## ⚡ Architectural Overview

                  +----------------------------------+
                  |    GitHub Actions Cloud Runner   |
                  |    (Triggered 3x Daily via CRON) |
                  +----------------------------------+
                                   |
                                   v
                  +----------------------------------+
                  |        `scraper.py` Script       |
                  |   - Sends HTTPS Request          |
                  |   - Custom User-Agent Header     |
                  |   - Exponential Backoff / Retry  |
                  +----------------------------------+
                                   |
                                   v
                  +----------------------------------+
                  |            ArXiv API             |
                  | (Fetch cs.RO & cs.AI Papers Data)|
                  +----------------------------------+
                                   |
                                   v
                  +----------------------------------+
                  |      Markdown Data Formatting    |
                  |  - XML Parsing & Text Clean-up   |
                  |  - Appends to Monthly Log File   |
                  +----------------------------------+
                                   |
                                   v
                  +-----------------------------------+
                  |   Automated Git Push Engine       |
                  | (Updates Repository Automatically)|
                  +-----------------------------------+


                ---

## ✨ Key Features

* ⏱️ **Fully Autonomous Execution:** Runs thrice daily at `08:00 AM`, `02:00 PM`, and `08:00 PM IST` via UTC scheduled CRON triggers.
* 🛡️ **Fault-Tolerant Engine:** Built-in exponential backoff and retry mechanisms to handle API rate limiting (HTTP 503) seamlessly.
* 📂 **Structured Monthly Logging:** Automatically aggregates daily paper summaries into clean, month-wise Markdown archives (e.g., `Daily_Robotics_Paper_Aug_2026.md`).
* 🌐 **Zero Server Infrastructure:** Runs 100% on cloud-native GitHub Actions runners with no local hardware dependency.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Core Libraries:** `urllib.request` (Networking), `xml.etree.ElementTree` (XML Parsing), `datetime` (IST Sync), `time` (Backoff logic)
* **Automation & CI/CD:** GitHub Actions Workflows (`cron` triggers)
* **Data Format:** Markdown (`.md`)

---

## 📅 Schedule Configuration

The pipeline is governed by the following CRON schedule inside `.github/workflows/daily_digest.yml`:

| Time (IST) | CRON Schedule (UTC) | Action |
| :--- | :--- | :--- |
| **08:00 AM IST** | `30 2 * * *` | Fetch Morning Research Digest |
| **02:00 PM IST** | `30 8 * * *` | Fetch Afternoon Research Digest |
| **08:00 PM IST** | `30 14 * * *` | Fetch Evening Research Digest |

---

## 🚀 Local Installation & Manual Run

To execute the pipeline locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/pranavrathod07/Daily-Robotics-AI-Research-Digest.git](https://github.com/pranavrathod07/Daily-Robotics-AI-Research-Digest.git)
   cd Daily-Robotics-AI-Research-Digest
