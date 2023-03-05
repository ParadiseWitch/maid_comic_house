import { Injectable, Logger } from '@nestjs/common'
import { Browser, chromium, Page } from 'playwright'
import { download } from 'src/utils/AxiosUtil'
import FileUtil from 'src/utils/FileUtil'
import retry from 'src/utils/retry'
import { BaseSpiderService } from './basespider.service'
// TODO crawler

const host: string = 'https://www.copymanga.site'

interface Chapter {
  url: string
  title: string
}

interface BrowserAndPage {
  browser: Browser
  page: Page
}

@Injectable()
export class CopyComicSpiderService extends BaseSpiderService {
  private readonly logger = new Logger(CopyComicSpiderService.name)

  constructor () {
    super()
  }
  /**
   * 初始化浏览器和page
   */
  async initBrowserAndPage (): Promise<BrowserAndPage> {
    let browser = null
    let page = null

    // if (browser && page) return

    try {
      browser = await chromium.launch({
        headless: true,
      })
      page = await browser.newPage()
      page.setDefaultNavigationTimeout(30000)
      await page.setViewportSize({ width: 1920, height: 1080 })
    } catch (e) {
      this.logger.error('初始化browser和page失败！\n' + e)
      throw new Error('initBrowserAndPage err')
    }
    return { browser, page }
  }

  /**
   *
   */
  async spiderComicAllChapter (
    comicName: string,
    { browser, page }: BrowserAndPage,
  ) {
    const targetUrl = `${host}/comic/${comicName}`
    let chapters: Chapter[]
    // await page.waitForNavigation();

    // 1. 请求漫画页面
    try {
      await page.goto(targetUrl, { waitUntil: 'load', timeout: 30000 })
    } catch (e) {
      this.logger.error(`请求超时！网站可能暂时无法访问！${targetUrl} `, e)
      await browser.close()
      return
    }

    // 2. 获取漫画名
    let comicTitle: string
    try {
      comicTitle =
        (await page.$eval(
          '.row > .col-9 > ul > li > h6',
          el => el.textContent,
        )) || '暂无标题'
    } catch (e) {
      this.logger.error('获取漫画名失败！', e)
      await browser.close()
      return
    }
    this.logger.debug(`当前漫画名：${comicTitle}`)

    // 3. 构建漫画章节数组
    try {
      chapters = await page.$$eval<Chapter[], HTMLElement>(
        '#default全部 ul:first-child a',
        (els, host) =>
          els.map((el): Chapter => {
            return {
              url: host + el.getAttribute('href'),
              title: el.textContent || '暂无标题',
            }
          }),
        host,
      )
    } catch (e) {
      this.logger.error(`获取章节列表失败！${e}`)
      await browser.close()
      return
    }
    this.logger.debug(`章节长度: ${chapters.length}`)

    // 4. 创建漫画名文件夹
    try {
      FileUtil.mkdir(`./caputer/${comicTitle}/`)
    } catch (e) {
      this.logger.error(`创建漫画文件夹失败：./caputer/${comicTitle}/`, e)
      await browser.close()
      return
    }

    // 5. goto每个章节链接 循环章节 下载图片
    try {
      for (let index = 0; index < chapters.length; index++) {
        await this.spiderChapter(chapters[index], comicTitle, { browser, page })
      }
    } catch (e) {
      this.logger.error('下载失败！', e)
    }
    this.logger.debug(`漫画《${comicTitle}》下载成功！`)
    await browser.close()
  }

  /**
   * 循环每个章节链接，下载获取到的图片链接
   * TODO 拆解成几个模块，职责明确
   * @param chapter 章节数组
   * @param comic_title 漫画名
   */
  async spiderChapter (
    chapter: Chapter,
    comic_title: string,
    { browser, page }: BrowserAndPage,
  ) {
    let imgs: string[]
    const chapter_title: string = chapter.title
    const chapter_link = chapter.url
    try {
      // await navigationPromise
      this.logger.debug(
        `开始下载《${chapter_title}》的图片, 链接：${chapter_link} `,
      )

      // TODO:更新策略
      const chapterIsExist = FileUtil.isExist(
        `./caputer/${comic_title}/${chapter_title}`,
      )
      if (chapterIsExist) {
        let files: string[]
        try {
          files = FileUtil.getFiles(`./caputer/${comic_title}/${chapter_title}`)
          if (files && files.length !== 0) {
            this.logger.debug(
              `./caputer/${comic_title}/${chapter_title} 该文件夹下已有文件，跳过下载`,
            )
            return
          }
        } catch (e) {
          this.logger.error(e)
        }
      }
      FileUtil.mkdir(`./caputer/${comic_title}/${chapter_title}/`)

      imgs = await this.goToChapterPageAndGetImgs(chapter_link, {
        browser,
        page,
      })

      // 防止被ban
      // await page.waitForTimeout(1000);
    } catch (error) {
      this.logger.error(`${comic_title} ${chapter_title} 爬取图片失败。`, error)
      return
    }

    // 循环图片
    for (let imgIndex = 0; imgIndex < imgs.length; imgIndex++) {
      const link = imgs[imgIndex]
      // try {
      // TODO 注意复制后缀
      retry(async () => {
        await download(
          link,
          `./caputer/${comic_title}/${chapter_title}/第${imgIndex + 1}页.png`,
        )
      }).catch(e => {
        this.logger.error(
          `${comic_title} ${chapter_title} 下载第${imgIndex + 1}页图片失败`,
          e,
        )
      })
    }
  }

  /**
   * 去指定的章节链接，获取图片链接
   * //TODO 下载完一话就关闭这一话的页面
   * @param url
   * @returns
   */
  async goToChapterPageAndGetImgs (
    url: string,
    { browser, page }: BrowserAndPage,
  ): Promise<string[]> {
    // page.setDefaultNavigationTimeout(30000)
    // await page.waitForNavigation()
    const chapterPage: Page = await browser.newPage()
    let imgs: string[]
    try {
      // 1. 跳转章节链接
      try {
        await chapterPage.goto(url)
      } catch (e) {
        // Log.error(`加载章节失败：${url}`)
        throw new Error(`加载章节失败：${url}`)
      }
      await chapterPage.setViewportSize({ width: 500, height: 637 })

      // 2. 等待漫画页数的Dom节点加载
      try {
        await chapterPage.waitForSelector('body > div > .comicCount')
      } catch (e) {
        this.logger.error("等待元素：'body > div > .comicCount' 显示超时！")
        throw new Error('加载网页可能失败，漫画页数指示器未加载')
      }
      const comicCount = await (
        await chapterPage.$('body > div > .comicCount')
      ).textContent()
      this.logger.debug(`本话共有 ${comicCount} 页`)

      // 3. 等待漫画内容容器的Dom节点加载
      try {
        await chapterPage.waitForSelector(
          '.container-fluid > .container > .comicContent-list',
        )
      } catch (e) {
        this.logger.error(
          "等待元素：'.container-fluid > .container > .comicContent-list' 显示超时！",
        )
        throw new Error('加载网页可能失败，漫画内容的容器未加载')
      }

      // 4. 滚动到底部，触发图片加载
      const scrollToBottom = async () => {
        await chapterPage.keyboard.press('PageDown')
        await chapterPage.waitForTimeout(100)
        // 默认如果漫画页数的Dom节点，那么这个节点也会加载
        const comicIndex = await // FIXME: page.$: Target closed
        (await chapterPage.$('body > div > .comicIndex')).textContent()
        if (comicCount === comicIndex) {
          this.logger.debug(`最后的漫画页数： ${comicIndex}`)
          return
        }
        await scrollToBottom()
      }
      await scrollToBottom()

      // 5. 获取图片链接
      imgs = await chapterPage.$$eval(
        '.container-fluid > .container > .comicContent-list > li > img',
        els => els.map(el => el.getAttribute('data-src')),
      )
      return imgs
    } catch (error) {
      this.logger.error(error)
      await chapterPage.close()
      throw new Error(`获取图片链接失败: ${url}`)
    }

    // const items = await page.$$('.container-fluid > .container > .comicContent-list');
    // const lastItemRendered = items[items.length - 1];
    // 等到图片加载完毕后截图
    // let complete;
    // await page.waitForFunction((complete) => {
    //   const lastImg = document.querySelector('.container-fluid > .container > .comicContent-list > li:nth-last-child(1) > img');
    //   complete = (lastImg as HTMLImageElement).complete;
    //   return (lastImg as HTMLImageElement).complete;
    // }, complete, {timeout:30000});
    // Log.log(`${complete}`);
    // await lastItemRendered.screenshot({path: './caputer/comic.png'});
  }
}
