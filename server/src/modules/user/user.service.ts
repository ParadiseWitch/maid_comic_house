import { ForbiddenException, Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { compareSync } from 'bcrypt';
import { Repository } from 'typeorm';
import { User } from './user.entity';

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name);

  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async login(name: string, password: string) {
    const usr = await this.usersRepository.findOneBy({ name });
    if (!usr) {
      throw new ForbiddenException('user not exist');
    }

    if (!compareSync(password, usr.password)) {
      throw new ForbiddenException('password mistake');
    }
    return {
      state: 'success',
      data: null,
    };
  }

  async regist(name: string, password: string) {
    const usr = await this.usersRepository.findOneBy({ name });
    if (usr) {
      throw new ForbiddenException('user already exist');
    }
    const nuser = new User();
    nuser.name = name;
    nuser.password = password;
    await this.usersRepository.insert(nuser);
    return {
      state: 'success',
      data: nuser,
    };
  }
}
