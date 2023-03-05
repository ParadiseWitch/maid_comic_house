import { Inject, Injectable, Logger } from '@nestjs/common'
import { CopyComicSpiderService } from 'src/site/copycomic.service'

@Injectable()
export class SpiderService {
  private readonly logger = new Logger(SpiderService.name)
  @Inject()
  private copycomicService: CopyComicSpiderService

  constructor () {}

  async spider () {
    const bp = await this.copycomicService.initBrowserAndPage()
    await this.copycomicService.spiderComicAllChapter(
      'huayuanjiadeshuangzi',
      bp,
    )
  }
}
