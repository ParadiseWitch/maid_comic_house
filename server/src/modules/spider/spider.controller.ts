import { Body, Controller, Get, Post } from '@nestjs/common';
import { SpiderService } from './spider.service';

@Controller('spider')
export class SpiderController {
  constructor(private readonly spiderService: SpiderService) { }

  @Get('test')
  test() {
    return this.spiderService.test()
  }
}
