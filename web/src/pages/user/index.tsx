import { AutoCenter, Avatar, Button, Input, Space } from 'antd-mobile'
import { CameraOutline, CheckCircleOutline, EditSOutline } from 'antd-mobile-icons'

import type { FC } from 'react'
import { useState } from 'react'
import PageTemplate from '/@/components/page-template'

// 自定义上传按钮
const UploadButton: FC = () => {
  const onClick = () => {
    const uploadInput = document.getElementById('upload-input')
    uploadInput?.click()
  }
  return (<>
    <Button block color='default' size='middle' onClick={onClick} style={{ border: 0, backgroundColor: '#fff' }}>
      <Space block>
        <CameraOutline color='var(--adm-color-danger)' fontSize={24}/>
        <Space style={{ color: 'var(--adm-color-danger)', fontSize: 14 }}>更换头像</Space>
      </Space>
    <input id='upload-input' placeholder='请输入用户名' type='file' style={{ display: 'none' }} onChange={() => {}}/>
    </Button>
  </>)
}

const user: FC = (_props) => {
  const [userName] = useState('Maid')
  const [isEditingUserName, setIsEditingUserName] = useState(false)

  return (
    <PageTemplate>
      <AutoCenter>
        <Avatar src='' style={{ '--size': '7rem', '--border-radius': '4rem' }}/>
      </AutoCenter>

      <AutoCenter>
        <div style={{ fontSize: 20, color: '#333', marginTop: 10 }}>
          {/* <div className={[isEditingUserName ? 'hidden' : 'flex'].join(' ')}> */}
          <Space>
            {!isEditingUserName && userName}
            {!isEditingUserName && <EditSOutline onClick={() => { setIsEditingUserName(true) }}/>}
            {isEditingUserName && <Input className='font-size-2' placeholder='请输入用户名'></Input>}
            {isEditingUserName && <CheckCircleOutline onClick={() => { setIsEditingUserName(false) }}/>}

          </Space>
          {/* </div> */}
        </div>
      </AutoCenter>
      <div style={{ marginTop: 20 }}>
        <UploadButton />
      </div>
    </PageTemplate>
  )
}

export default user
