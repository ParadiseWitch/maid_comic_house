import { AutoCenter, Image, NavBar, Slider, Swiper } from 'antd-mobile'
import type { SwiperRef } from 'antd-mobile/es/components/swiper'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Chapter from '/@/pkg/chapter'

function chapter() {
  const navigate = useNavigate()
  const [showInfo, setShowInfo] = useState(false)
  const swiperRef = useRef<SwiperRef>(null)
  const [curIndex, setCueIndex] = useState(1)

  const chapterData: Chapter = new Chapter('第1话')
  chapterData.imgs = [
    'https://cdn.1he7c.com/zhuanshengzhihouwoxiangyaozaitianyuanguomanshenghu/4a895/16408000298076/h1500x.jpg',
    'xxx',
    'https://hi77-overseas.mangafuna.xyz/dianjuren/d4e9c/1647068876240001.png.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    ' https://hi77-overseas.mangafuna.xyz/huayuanjiadeshuangzi/e7a24/1647249435180007.jpg.c800x.jpg',
    'https://cdn.1he7c.com/zhuanshengzhihouwoxiangyaozaitianyuanguomanshenghu/4a895/16408000298076/h1500x.jpg',
  ]
  return <>
    {showInfo && <>
      <div style={{ position: 'fixed', backgroundColor: '#eee', width: '100%' }}>
        <NavBar back={''} onBack={() => { navigate('/comic') }}>
          {chapterData.name}
        </NavBar >
      </div>
      <div style={{ position: 'fixed', width: '100%', bottom: '0', marginBottom: '10px' }}>
        <Slider popover={true} min={1} max={chapterData.imgs.length}
          value={curIndex}
          onChange={(val) => {
            swiperRef?.current?.swipeTo(val as number - 1)
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
            setCueIndex(index + 1)
          }}>
          {chapterData.imgs.map((src, index) =>
            <Swiper.Item
              onClick={() => { setShowInfo(!showInfo) }}
              style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }} key={index}>
              <div>
                <Image
                  lazy
                  src={src}
                  width={'100%'}
                  fit='cover'
                  height={'100%'}
                  fallback={<AutoCenter style={{ color: '#eee' }}>加载失败</AutoCenter>}
                />
              </div>
            </Swiper.Item>)}
        </Swiper>
      </div>

    </div >
  </>
}
export default chapter
