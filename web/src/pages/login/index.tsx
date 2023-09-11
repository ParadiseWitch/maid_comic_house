import { AutoCenter, Input, List, NavBar, Toast } from 'antd-mobile'
import { EyeInvisibleOutline, EyeOutline } from 'antd-mobile-icons'
import { ListItem } from 'antd-mobile/es/components/list/list-item'
import axios from 'axios'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function login() {
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [password, setPassWord] = useState('')
  const [visible, setVisible] = useState(false)

  const submit = () => {
    if (!name)
      Toast.show('用户名不为空')

    if (!password)
      Toast.show('密码不为空')

    axios.post('/api/user/login', { name, password }).then(() => {
      Toast.show('登录成功')
      // TODO
    }).catch((err) => {
      const msg = err?.response?.data?.message || '请求错误'
      Toast.show(msg)
      console.warn(msg, err)
    })

    // fetch('/api/user/login', {
    //   method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //   headers: {
    //     'Content-Type': 'application/json',
    //     // 'Content-Type': 'application/x-www-form-urlencoded',
    //   },
    //   body: JSON.stringify({ name, password }), // body data type must match "Content-Type" header

    // }).then(res => res.json()).then(res => console.log(res))
  }

  return (
    <>
      <div className='top'>
        <NavBar back={true} onBack={() => {
          navigate(-1)
        }} >
          Maid漫画屋☕
        </NavBar >
      </div>

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        height: '90vh',
        justifyContent: 'space-evenly',
      }}>
        <List header='' style={{
          borderLeft: '1px solid #eee',
          borderRight: '1px solid #eee',
          margin: 30,
        }}>
          <List.Item>
            <AutoCenter>用户登录</AutoCenter>
          </List.Item>
          <List.Item title="用户名">
            <Input placeholder='请输入用户名' value={name} onChange={val => setName(val)} />
          </List.Item>
          <List.Item title="密码">
            <div style={{
              display: 'flex',
              alignItems: 'center',
            }}>
              <Input
                value={password}
                onChange={(val) => {
                  setPassWord(val)
                }}
                style={{ flex: 'auto' }}
                placeholder='请输入密码'
                type={visible ? 'text' : 'password'}
              />
              <div style={{
                flex: 'none',
                marginLeft: 8,
                padding: 4,
                cursor: 'pointer',
              }}>
                {!visible
                  ? (<EyeInvisibleOutline onClick={() => setVisible(true)} />)
                  : (<EyeOutline onClick={() => setVisible(false)} />)}
              </div>
            </div>
          </List.Item>
          <ListItem
            style={{ background: '#c9dffd' }}
            arrow={false}
            clickable={true}
            onClick={submit}>
            <AutoCenter>提交</AutoCenter>
          </ListItem>
          <ListItem
            style={{ background: '#eee' }}
            arrow={false}
            clickable={true}
            onClick={() => { navigate('/regist') }}>
            <AutoCenter>注册</AutoCenter>
          </ListItem>
        </List>
      </div>
    </>
  )
}
export default login
