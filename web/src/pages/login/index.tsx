import { AutoCenter, Button, Input, List, Toast } from "antd-mobile"
import { EyeInvisibleOutline, EyeOutline } from "antd-mobile-icons"
import { ListItem } from "antd-mobile/es/components/list/list-item"
import axios, { AxiosResponse } from "axios"
import { useState } from "react"

function login() {
  const [name, setName] = useState('')
  const [password, setPassWord] = useState('')
  const [visible, setVisible] = useState(false)

  const submit = () => {
    if (!name) {
      Toast.show('用户名不为空')
    }
    if (!password) {
      Toast.show('密码不为空')
    }

    axios.post('/api/login', { name, password }).then((res :AxiosResponse) => {
      Toast.show('登录成功')
      // TODO
    }).catch(err => {
      const msg = err?.response?.data?.message || '请求错误'
      Toast.show(msg)
      console.warn(msg, err);
    })
  }

  return (
    <>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        justifyContent: 'space-evenly'
      }}>
        <List header=''>
          <List.Item>
            <AutoCenter>用户登录</AutoCenter>
          </List.Item>
          <List.Item>
            <Input placeholder='用户名' value={name} onChange={val => setName(val)} />
          </List.Item>
          <List.Item>
            <div style={{
              display: 'flex',
              alignItems: 'center',
            }}>
              <Input
                value={password}
                onChange={val => {
                  setPassWord(val)
                }}
                style={{ flex: 'auto' }}
                placeholder='密码'
                type={visible ? 'text' : 'password'}
              />
              <div style={{
                flex: 'none',
                marginLeft: 8,
                padding: 4,
                cursor: 'pointer'
              }}>
                {!visible ? (
                  <EyeInvisibleOutline onClick={() => setVisible(true)} />
                ) : (
                  <EyeOutline onClick={() => setVisible(false)} />
                )}
              </div>
            </div>
          </List.Item>
          <ListItem>
            <Button block type='submit' color='primary' size='large' onClick={submit}>
              提交
            </Button>
          </ListItem>
        </List>
      </div>
    </>
  )
}
export default login
