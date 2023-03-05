import { Module } from '@nestjs/common'
import { CopyComicSpiderService } from 'src/site/copycomic.service'
import { SpiderController } from './spider.controller'
import { SpiderService } from './spider.service'

@Module({
  controllers: [SpiderController],
  providers: [SpiderService, CopyComicSpiderService],
})
export class SpiderModule {}
