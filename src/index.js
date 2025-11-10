#!/usr/bin/env node

import puppeteer from "puppeteer";
import fs from "fs";
import yaml from "js-yaml";

const CONFIG_FILE = "./config/dashboard.yml";
const DEFAULT_INTERVAL = 30_000; // ms

const config = yaml.load(fs.readFileSync(CONFIG_FILE, "utf8"));
const schedule = config.schedule || [];

function getCurrentPeriod() {
  const now = new Date();
  const hhmm = now.toTimeString().slice(0, 5);
  return schedule.find((p) => {
    const start = p.start;
    const end = p.end;
    if (start <= end) return hhmm >= start && hhmm < end;
    return hhmm >= start || hhmm < end; // période traversant minuit
  });
}

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--kiosk", "--disable-infobars"],
  });
  const page = await browser.newPage();

  let currentPeriod = null;
  let urls = [];
  let index = 0;

  while (true) {
    const period = getCurrentPeriod();

    if (!period) {
      console.log("No active period, waiting...");
      await new Promise((r) => setTimeout(r, DEFAULT_INTERVAL));
      continue;
    }

    if (period.name !== currentPeriod) {
      console.log(`Switching to period: ${period.name}`);
      currentPeriod = period.name;
      urls = period.urls || [];
      index = 0;
    }

    if (urls.length > 0) {
      console.log(`Displaying URL: ${urls[index]}`);
      await page.goto(urls[index], { waitUntil: "networkidle2" });
      index = (index + 1) % urls.length;
    }

    await new Promise((r) => setTimeout(r, (period.interval || 30) * 1000));
  }
})();
