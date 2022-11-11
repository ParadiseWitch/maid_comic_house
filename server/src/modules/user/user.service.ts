import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Not, Repository } from 'typeorm';
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
      return {
        state: 'fail',
        msg: 'user already esist',
      };
    }
    // TODO encry
    // TODO JWT
    if (usr.password !== password) {
      return {
        state: 'fail',
        msg: 'password mistake',
      };
    }
    return {
      state: 'success',
      data: null,
    };
  }

  async regist(name: string, password: string) {
    const usr = await this.usersRepository.findOneBy({ name });
    if (usr) {
      return {
        state: 'fail',
        msg: 'user already exist',
      };
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
