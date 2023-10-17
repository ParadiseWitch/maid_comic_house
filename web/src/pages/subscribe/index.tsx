import { SearchBar } from 'antd-mobile'
import ComicList from '/@/components/comic-list'
import PageTemplate from '/@/components/page-template'

export default function subscribe() {
  return (
    <>
    <PageTemplate>
      <div style={{ paddingBottom: 10 }}>
        <SearchBar placeholder="请输入内容" showCancelButton />
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
      ]}
      ></ComicList>
    </PageTemplate>

    </>
  )
}
