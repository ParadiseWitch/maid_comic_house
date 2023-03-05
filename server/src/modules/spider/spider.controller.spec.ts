import { Test, TestingModule } from '@nestjs/testing'
import { SpiderController } from './spider.controller'
import { SpiderService } from './spider.service'

describe('SpiderController', () => {
  let controller: SpiderController

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [SpiderController],
      providers: [SpiderService],
    }).compile()

    controller = module.get<SpiderController>(SpiderController)
  })

  it('should be defined', () => {
    expect(controller).toBeDefined()
  })

  // it('test spider', async () => {
  //   const ret = await controller.spider()
  //   expect(ret).toBe('test')
  // })
})
