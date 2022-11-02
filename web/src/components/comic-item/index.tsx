import { Image } from 'antd-mobile'
import { useNavigate } from 'react-router-dom'
import type { Comic } from '/@/pkg/comic'
import type { Layout } from '/@/components/comic-list'
import './index.css'

type ComicItemPT = Pick<Comic, 'title' | 'cover'> & { layout: Layout }

function comicItem(props: ComicItemPT) {
  const navigate = useNavigate()
  const handleClick = () => {
    navigate('/comic?cid=huayuanjiadeshuangzi')
  }
  return (<>
    <div className='comic-container' onClick={handleClick}>
      <div className='comic-cover'>
        <Image src={props.cover} width={'100%'} height={'100%'} fit={'cover'} />
      </div>
      {props.title}
    </div>
  </>)
}

export default comicItem
