import { chromium } from 'playwright'
import { Browser, Page } from 'playwright'

import Log from './utils/log'
import { download } from './utils/AxiosUtil'
import FileUtil from './utils/FileUtil'
import retry from './utils/retry'

// TODO 配置 是否显示浏览器
// 拷贝漫画host
const host = 'https://www.copymanga.site'
let browser: Browser | null = null
let page: Page | null = null

interface Chapter {
  url: string
  title: string
}

/**
 * 初始化浏览器和page
 */
async function initBrowserAndPage () {
  if (browser && page) return

  try {
    browser = await chromium.launch({
    headless: false,
  })
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(30000)
    await page.setViewportSize({ width: 1920, height: 1080 })
  } catch (e) {
    Log.error(e)
    throw new Error('initBrowserAndPage err')
  }
}

const spiderComicAllChapter = async (comicName: string) => {
  const targetUrl = `${host}/comic/${comicName}`
  let chapters: Chapter[]
  try {
    await initBrowserAndPage()
  } catch (error) {
    Log.error(error)
    return
  }
  // await page.waitForNavigation();

  // 1. 请求漫画页面
  try {
    await page.goto(targetUrl, { waitUntil: 'load', timeout: 30000 })
  } catch (e) {
    Log.error(`请求超时！网站可能暂时无法访问！${targetUrl} `, e)
    await browser.close()
    return
  }

  // 2. 获取漫画名
  let comicTitle: string
  try {
    comicTitle =
      (await page.$eval(
        '.row > .col-9 > ul > li > h6',
        el => el.textContent
      )) || '暂无标题'
  } catch (e) {
    Log.error('获取漫画名失败！', e)
    await browser.close()
    return
  }
  Log.info(`当前漫画名：${comicTitle}`)

  // 3. 构建漫画章节数组
  try {
    chapters = await page.$$eval<Chapter[], HTMLElement>(
      '#default全部 ul:first-child a',
      (els, host) =>
        els.map(
          (el): Chapter => {
            return {
              url: host + el.getAttribute('href'),
              title: el.textContent || '暂无标题'
            }
          }
        ),
      host
    )
  } catch (e) {
    Log.error(`获取章节列表失败！${e}`)
    await browser.close()
    return
  }
  Log.info(`章节长度: ${chapters.length}`)

  // 4. 创建漫画名文件夹
  try {
    FileUtil.mkdir(`./caputer/${comicTitle}/`)
  } catch (e) {
    Log.error(`创建漫画文件夹失败：./caputer/${comicTitle}/`, e)
    await browser.close()
    return
  }

  // 5. goto每个章节链接 循环章节 下载图片
  try {
    for (let index = 0; index < chapters.length; index++) {
      await spiderChapter(chapters[index], comicTitle)
    }
  } catch (e) {
    Log.error('下载失败！', e)
  }
  Log.info(`漫画《${comicTitle}》下载成功！`)
  await browser.close()
}

/**
 * 循环每个章节链接，下载获取到的图片链接
 * TODO 拆解成几个模块，职责明确
 * @param chapter 章节数组
 * @param comic_title 漫画名
 */
const spiderChapter = async (
  chapter: Chapter,
  comic_title: string
) => {
  let imgs: string[]
  const chapter_title: string = chapter.title
  const chapter_link = chapter.url
  try {
    // await navigationPromise
    Log.info(`开始下载《${chapter_title}》的图片, 链接：${chapter_link} `)

    // TODO:更新策略
    const chapterIsExist = FileUtil.isExist(
      `./caputer/${comic_title}/${chapter_title}`
    )
    if (chapterIsExist) {
      let files: string[]
      try {
        files = FileUtil.getFiles(`./caputer/${comic_title}/${chapter_title}`)
        if (files && files.length !== 0) {
          Log.info(
            `./caputer/${comic_title}/${chapter_title} 该文件夹下已有文件，跳过下载`
          )
          return
        }
      } catch (e) {
        Log.error(e)
      }
    }
    FileUtil.mkdir(`./caputer/${comic_title}/${chapter_title}/`)

    imgs = await goToChapterPageAndGetImgs(chapter_link)

    // 防止被ban
    // await page.waitForTimeout(1000);
  } catch (error) {
    Log.error(`${comic_title} ${chapter_title} 爬取图片失败。`, error)
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
          `./caputer/${comic_title}/${chapter_title}/第${imgIndex + 1}页.png`
        )
      }).catch((e)=>{
        Log.error(
          `${comic_title} ${chapter_title} 下载第${imgIndex + 1}页图片失败`,
          e
        )
      })
    // } catch (e) {
      
    // }
  }
}

/**
 * 去指定的章节链接，获取图片链接
 * //TODO 下载完一话就关闭这一话的页面
 * @param url
 * @returns
 */
async function goToChapterPageAndGetImgs (
  url: string
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
      Log.error("等待元素：'body > div > .comicCount' 显示超时！")
      throw new Error('加载网页可能失败，漫画页数指示器未加载')
    }
    const comicCount = await (
      await chapterPage.$('body > div > .comicCount')
    ).textContent()
    Log.log(`本话共有 ${comicCount} 页`)

    // 3. 等待漫画内容容器的Dom节点加载
    try {
      await chapterPage.waitForSelector(
        '.container-fluid > .container > .comicContent-list'
      )
    } catch (e) {
      Log.error(
        "等待元素：'.container-fluid > .container > .comicContent-list' 显示超时！"
      )
      throw new Error('加载网页可能失败，漫画内容的容器未加载')
    }

    // 4. 滚动到底部，触发图片加载
    const scrollToBottom = async () => {
      await chapterPage.keyboard.press('PageDown')
      await chapterPage.waitForTimeout(100)
      // 默认如果漫画页数的Dom节点，那么这个节点也会加载
      const comicIndex = await (
        // FIXME: page.$: Target closed
        await chapterPage.$('body > div > .comicIndex')
      ).textContent()
      if (comicCount === comicIndex) {
        Log.log(`最后的漫画页数： ${comicIndex}`)
        return
      }
      await scrollToBottom()
    }
    await scrollToBottom()

    // 5. 获取图片链接
    imgs = await chapterPage.$$eval(
      '.container-fluid > .container > .comicContent-list > li > img',
      els => els.map(el => el.getAttribute('data-src'))
    )
    return imgs
  } catch (error) {
    Log.error(error)
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

// NOTE：这是下载某个漫画全部章节
spiderComicAllChapter('huayuanjiadeshuangzi')

// TODO： 单独下载某个章节
const main = async()=>{
  // await initBrowserAndPage()
  // await spiderChapter({
  //   url: "https://www.copymanga.site/comic/huayuanjiadeshuangzi/chapter/96cc7876-e815-11ea-9ecc-00163e0ca5bd",
  //   title:"第02话"
  // },'花園家的雙子')
  // retry(async () => {
  //   await download(
  //     "https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/943db/1647249390830041.jpg.c800x.jpg",
  //     `./第1页.png`
  //   )
  // }, 3)

}
main()

// TODO： 单独下载某张图片
