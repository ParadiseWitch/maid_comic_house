import { hashSync } from 'bcrypt';
import { BeforeInsert, Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: string;

  @Column()
  name: string;

  @Column()
  password: string;

  @BeforeInsert()
  bcryptPad() {
    this.password = hashSync(this.password, 6);
  }
}
