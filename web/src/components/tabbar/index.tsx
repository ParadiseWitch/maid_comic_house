import { Badge, TabBar } from 'antd-mobile'
import { CompassOutline, ShopbagOutline, UserOutline } from 'antd-mobile-icons'
import type { FC } from 'react'
import {
  useLocation,
  useNavigate,
} from 'react-router-dom'

const tabs = [
  {
    key: '/subscribe',
    title: '订阅',
    icon: <ShopbagOutline />,
    badge: Badge.dot,
  },
  {
    key: '/discover',
    title: '发现',
    icon: <CompassOutline />,
    badge: Badge.dot,
  },
  {
    key: '/user',
    title: '我的',
    icon: <UserOutline />,
    badge: '5',
  },
]

const MaidTabBar: FC = (_props: any) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { pathname } = location

  const setRouteActive = (value: string) => {
    navigate(value)
  }

  return (
    <TabBar activeKey={pathname === '/' ? '/subscribe' : pathname} onChange={value => setRouteActive(value)}>
      {tabs.map(item => (
        <TabBar.Item {...item} />
      ))}
    </TabBar>
  )
}

export default MaidTabBar

