import { Body, Controller, Post } from '@nestjs/common'
import { UserService } from './user.service'

class LoginVo {
  name: string
  password: string
}

@Controller()
export class UserController {
  constructor(private readonly userService: UserService) { }

  @Post('login')
  login(@Body() vo: LoginVo) {
    return this.userService.login(vo.name, vo.password)
  }

  @Post('regist')
  regist(@Body() vo: LoginVo) {
    return this.userService.regist(vo.name, vo.password)
  }
}
