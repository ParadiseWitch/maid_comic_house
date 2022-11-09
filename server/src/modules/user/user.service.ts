import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ResultType, User } from './user.dto';

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name);

  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  login(name: string, password: string): any {
    return {
      state: 'success',
      data: null,
    };
  }

  regist(name: string, password: string): ResultType {
    return {
      state: 'success',
      data: null,
    };
  }

  findOne(id: string): Promise<User> {
    //FIXME
    return this.usersRepository.findOne({ id });
  }
}
