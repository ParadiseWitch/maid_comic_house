import { Test, TestingModule } from '@nestjs/testing'
import { UserController } from './user.controller'
import { UserService } from './user.service'
import { compareSync, hashSync } from 'bcrypt'
import { TypeOrmModule } from '@nestjs/typeorm'
import { User } from './user.entity'

describe('UserController', () => {
  let userController: UserController
  beforeEach(async () => {
    const user: TestingModule = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'mysql',
          host: 'maiiiiiid.fun',
          port: 23306,
          username: 'root',
          password: '123456',
          database: 'maid_comic_house',
          entities: [User],
          synchronize: true,
        }),
        TypeOrmModule.forFeature([User]),
      ],
      controllers: [UserController],
      providers: [UserService],
    }).compile()

    userController = user.get<UserController>(UserController)
  })

  describe('login', () => {
    it('test login use the admin account', async () => {
      expect(
        await userController.login({ name: 'admin', password: 'admin' }),
      ).toEqual({
        state: 'success',
        data: null,
      })
    })
  })

  describe('regist', () => {
    it('test regist use an unregistered account', async () => {
      const rep = await userController.regist({
        name: 'test' + new Date().getTime(),
        password: 'xxx',
      })
      expect(rep.state).toEqual('success')
    })
  })

  describe('bcrypt', () => {
    it('test bcrypt', () => {
      const pad = '4edfasdfssgsdgdhgd'
      const hashPad = hashSync(pad, 6)
      expect(compareSync(pad, hashPad)).toEqual(true)
    })

    it('test compareSync', () => {
      expect(
        compareSync(
          'xxx',
          '$2b$06$gBfOnai9OKRZ85WPi9IrdeJJrT1zhgHu0ebTHHcTZD2LysMdKr2cu',
        ),
      ).toEqual(true)
    })
  })
})
