import { Badge } from 'antd-mobile'
import type { Comic } from '/@/pkg/comic'
import ComicItem from '/@/components/comic-item'
import './index.css'

export type Layout = 'grid' | 'list'

type ComicListPType = {
  layout: 'grid'
  comicList: Pick<Comic, 'title' | 'cover'>[]
} | {
  layout: 'list'
  comicList: Pick<Comic, 'title' | 'cover' | 'desc'>[]
}

function comicList(props: ComicListPType) {
  return <>
    <div className='comic-list'>
      {
        props.comicList.map((comic, index) =>
          <Badge key={index} content='new' style={{ '--right': '10%', '--top': '5%' }}>
            <ComicItem title={comic.title} cover={comic.cover} layout={'grid'} />
          </Badge>,
        )
      }
    </div>
  </>
}

export default comicList
