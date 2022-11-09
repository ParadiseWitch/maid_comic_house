export type LoginVo = {
  name: string;
  password: string;
};

export type ResultType<D = any> =
  | {
      state: 'success';
      data: D;
    }
  | {
      state: 'fail';
      msg: string;
    };

export class User {
  id: string;
  name: string;
  password: string;

  constructor(id: string, name?: string, password?: string) {
    this.id = id;
    this.name = name;
    this.password = password;
  }
}
