import { AutoCenter, Image, NavBar, Slider, Swiper } from 'antd-mobile'
import type { SwiperRef } from 'antd-mobile/es/components/swiper'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Chapter from '/@/pkg/chapter'

function chapter() {
  const navigate = useNavigate()
  const [showInfo, setShowInfo] = useState(true)
  const swiperRef = useRef<SwiperRef>(null)
  // 从0开始
  const [curIndex, setCurIndex] = useState(0)

  const chapterData: Chapter = new Chapter('第1话')
  chapterData.imgs = [
    'http://images.dmzj.com/z/%E4%BD%90%E4%BD%90%E6%9C%A8%E5%A4%A7%E5%8F%94%E4%B8%8E%E5%B0%8F%E5%93%94/08/038.jpg',
    'x',
    'http://images.dmzj.com/z/%E4%BD%90%E4%BD%90%E6%9C%A8%E5%A4%A7%E5%8F%94%E4%B8%8E%E5%B0%8F%E5%93%94/08/038.jpg',
    'http://images.dmzj.com/z/%E4%BD%90%E4%BD%90%E6%9C%A8%E5%A4%A7%E5%8F%94%E4%B8%8E%E5%B0%8F%E5%93%94/08/038.jpg',
  ]

  const goTo = (index: number) => {
    if (index < 0)
      swiperRef?.current?.swipeTo(0)
    if (index > chapterData.imgs.length - 1)
      swiperRef?.current?.swipeTo(chapterData.imgs.length - 1)
    swiperRef?.current?.swipeTo(index)
  }
  return <>
    {showInfo && <>
      <div style={{ position: 'fixed', backgroundColor: '#eee', width: '100%' }}>
        <NavBar back={''} onBack={() => { navigate('/comic') }}>
          {chapterData.name}
        </NavBar >
      </div>
      <div style={{ position: 'fixed', width: '100%', bottom: '0', marginBottom: '10px' }}>
        <Slider popover={true} min={1} max={chapterData.imgs.length}
          value={curIndex + 1}
          onChange={(val) => {
            goTo(val as number - 1)
          }} />
      </div>
    </>}
    <div style={{ backgroundColor: 'black' }}>
      <div style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}>
        <Swiper
          ref={swiperRef}
          indicator={(total, current) => (
            <>
              {showInfo && <div style={{
                position: 'absolute',
                top: 6,
                right: 6,
                background: 'rgba(0, 0, 0, 0.3)',
                padding: '4px 8px',
                color: '#ffffff',
                borderRadius: 4,
                userSelect: 'none',
              }}>
                {`${current + 1} / ${total}`}
              </div>}
            </>
          )}
          onIndexChange={(index) => {
            setCurIndex(index)
          }}>
          {chapterData.imgs.map((src, index) =>
            <Swiper.Item
              style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }} key={index}>
              <div style={{ height: '100%' }}>
                <div style={{ position: 'fixed', height: '100%', width: '100%', display: 'flex' }}>
                  <div style={{ flex: 1 }} onClick={() => { goTo(curIndex - 1) }}></div>
                  <div style={{ flex: 1 }} onClick={() => { setShowInfo(!showInfo) }}></div>
                  <div style={{ flex: 1 }} onClick={() => { goTo(curIndex + 1) }}></div>
                </div>
                <Image
                  lazy
                  src={src}
                  width={'100%'}
                  fit='cover'
                  height={'100%'}
                  fallback={
                    <AutoCenter style={{ color: '#eee', height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <AutoCenter>
                        加载失败
                      </AutoCenter>
                  </AutoCenter>}
                />
              </div>
            </Swiper.Item>)}
        </Swiper>
      </div>

    </div >
  </>
}
export default chapter
