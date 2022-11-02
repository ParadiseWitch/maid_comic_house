import { Badge, NavBar, SearchBar, TabBar } from 'antd-mobile'
import ComicList from '../../components/comic-list'

import './index.css'

function home() {
  const tabs = [
    {
      key: 'all',
      title: '全部',
      icon: '',
      badge: Badge.dot,
    },
    {
      key: 'new',
      title: '未看',
      icon: '',
      badge: '5',
    },
  ]

  return (
    <>
      <div className='app'>
        <div className='top'>
          <NavBar back={null}>
            Maid漫画屋☕
          </NavBar >
        </div>
        <div className='body'>
          <div style={{ paddingBottom: 10 }}>
            <SearchBar placeholder='请输入内容' showCancelButton />
          </div>

          <ComicList layout={'grid'} comicList={[
            {
              title: 'xxxx',
              cover: 'https://api.ixiaowai.cn/mcapi/mcapi.php',
            },
            {
              title: '2222',
              cover: 'https://api.ixiaowai.cn/mcapi/mcapi.php',
            },
            {
              title: '3333',
              cover: 'https://api.ixiaowai.cn/mcapi/mcapi.php',
            },
            {
              title: '4444',
              cover: 'https://api.ixiaowai.cn/mcapi/mcapi.php',
            },
            {
              title: '555',
              cover: 'https://api.ixiaowai.cn/mcapi/mcapi.php',
            },

          ]}></ComicList>
        </div>
        <div className='bottom'>
          <TabBar>
            {tabs.map(item => (
              <TabBar.Item key={item.key} title={item.title} />
            ))}
          </TabBar>
        </div>
      </div>
    </>
  )
}
export default home

