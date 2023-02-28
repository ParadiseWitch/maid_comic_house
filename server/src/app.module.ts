import { Module } from '@nestjs/common'
import { TypeOrmModule } from '@nestjs/typeorm'
import { AppController } from './app.controller'
import { AppService } from './app.service'
import { User } from './modules/user/user.entity'
import { UserModule } from './modules/user/user.module'
import { SpiderModule } from './modules/spider/spider.module';

@Module({
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
    UserModule,
    SpiderModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
