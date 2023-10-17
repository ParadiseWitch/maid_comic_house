import { AutoCenter, Avatar } from 'antd-mobile'
import type { FC } from 'react'
import PageTemplate from '/@/components/page-template'

const user: FC = (_props) => {
  return (
    <PageTemplate>
      <AutoCenter>
        <Avatar src='' style={{ '--size': '7rem', '--border-radius': '4rem' }}/>
      </AutoCenter>

      <AutoCenter>
        <div style={{ fontSize: 20, fontWeight: 'bolder', color: '#333', marginTop: 10 }}>Maid</div>
      </AutoCenter>
    </PageTemplate>
  )
}

export default user
