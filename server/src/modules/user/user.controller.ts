import { Body, Controller, Post } from '@nestjs/common';
import { LoginVo, ResultType } from './user.dto';
import { UserService } from './user.service';

@Controller()
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('/login')
  login(@Body() vo: LoginVo): ResultType {
    return this.userService.login(vo.name, vo.password);
  }

  @Post('/regist')
  regist(@Body() vo: LoginVo): ResultType {
    return this.userService.regist(vo.name, vo.password);
  }
}
