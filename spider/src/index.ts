// const puppeteer = require("puppeteer-core");
import { chromium } from 'playwright'

(async () => {
  // const browser = await chromium.launchPersistentContext(
  //   'C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\',
  //   {
  //     executablePath:
  //       'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  //     // executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  //     // headless: true,
  //   },
  // )
  const browser = await chromium.launch({
    headless: false,
  })

  // const browser = await chromium.launchPersistentContext('C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default',
  // {
  //   // executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  //   executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  //   headless: false,
  // })
  const page = await browser.newPage()
  await page.goto(
    'https://ber2f4zf62.feishu.cn/docs/doccnOAUJULcLNeWbdlC9KN4KEb',
  )
  await page.setViewportSize({ width: 1920, height: 1080 })
  const documentSize = await page.evaluate(() => {
    return {
      width: document.documentElement.clientWidth,
      height: document.body.clientHeight,
    }
  })
  // await page.waitForFunction(() => {
  //   const doc = document.getElementById('doc-container')
  //   return doc
  // })
  await page.screenshot({
    path: './example.png',
    clip: { x: 0, y: 0, width: 1920, height: documentSize.height || 1080 },
  })

  await browser.close()
})()
