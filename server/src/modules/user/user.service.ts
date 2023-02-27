import { ForbiddenException, Injectable, Logger } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
import { compareSync } from 'bcrypt'
import { Repository } from 'typeorm'
import { User } from './user.entity'

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name)

  constructor (
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async login (name: string, password: string) {
    const usr = await this.usersRepository.findOneBy({ name })
    if (!usr) {
      throw new ForbiddenException('用户不存在')
    }

    if (!compareSync(password, usr.password)) {
      throw new ForbiddenException('密码错误')
    }
    return {
      state: 'success',
      data: null,
    }
  }

  async regist (name: string, password: string) {
    const usr = await this.usersRepository.findOneBy({ name })
    if (usr) {
      throw new ForbiddenException('用户已存在')
    }
    const nuser = new User()
    nuser.name = name
    nuser.password = password
    await this.usersRepository.insert(nuser)
    return {
      state: 'success',
      data: nuser,
    }
  }
}
