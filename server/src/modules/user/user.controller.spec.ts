import { Test, TestingModule } from '@nestjs/testing';
import { UserController } from './user.controller';
import { UserService } from './user.service';

describe('UserController', () => {
  let userController: UserController;
  beforeEach(async () => {
    const user: TestingModule = await Test.createTestingModule({
      controllers: [UserController],
      providers: [UserService],
    }).compile();

    userController = user.get<UserController>(UserController);
  });

  describe('login', () => {
    it('should return success', () => {
      expect(userController.login({ name: '', password: '' })).toEqual({
        state: 'success',
        data: null,
      });
    });
  });

  describe('regist', () => {
    it('should return success', () => {
      expect(userController.login({ name: '', password: '' })).toEqual({
        state: 'success',
        data: null,
      });
    });
  });
});
