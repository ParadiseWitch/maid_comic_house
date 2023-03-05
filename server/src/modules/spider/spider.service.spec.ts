import { Test, TestingModule } from '@nestjs/testing'
import { SpiderService } from './spider.service'

describe('SpiderService', () => {
  let spiderService: SpiderService

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [SpiderService],
    }).compile()

    spiderService = module.get<SpiderService>(SpiderService)
  })

  it('should be defined', () => {
    expect(spiderService).toBeDefined()
  })
})
