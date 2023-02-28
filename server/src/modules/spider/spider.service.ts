import { Injectable, Logger } from '@nestjs/common';
import { chromium } from 'playwright'

@Injectable()
export class SpiderService {

  private readonly logger = new Logger(SpiderService.name)

  constructor() { }

  async test() {
    const browser = await chromium.launch({
      headless: false,
    })

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
    await page.screenshot({
      path: './example.png',
      clip: { x: 0, y: 0, width: 1920, height: documentSize.height || 1080 },
    })
    await browser.close()
    return "test"
  }

}
