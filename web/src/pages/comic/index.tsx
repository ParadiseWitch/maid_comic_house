import { Badge, Button, Collapse, Ellipsis, Grid, Image, NavBar } from 'antd-mobile'
import { useNavigate } from 'react-router-dom'
import './index.css'

function comic() {
  const navigate = useNavigate()
  return (
    <>
      <div className='app'>
        <div className='top'>
          <NavBar back='' onBack={() => { navigate('/') }}>
            漫画标题
          </NavBar >

        </div>
        <div className='body'>
          <div style={{
            display: 'flex',
            paddingBottom: 10,
            justifyContent: 'space-between',
            width: '100%',
          }}>
            <div className='cover-container'>
              <div className='cover'>
                <Image src={'https://api.ixiaowai.cn/mcapi/mcapi.php'} width={'%'} height={'100%'} fit={'cover'} />
              </div>
            </div>
            <div style={{
              width: '60%',
              height: '50vw',
              padding: '0 10px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}>
              <div>
                <div className='info-txt'>共10话</div>
                <div className='info-txt'>已读10话</div>
                <div style={{ height: '100%', width: '100%' }}>
                  <Ellipsis style={{
                    wordWrap: 'break-word',
                    wordBreak: 'normal',
                    fontSize: 10,
                    lineHeight: 1.2,
                  }} direction='end' rows={8} content={'2018-8-5 · 原文地址为： CSS禁止文字自动换行 当中文文字很长的时候（中间没有空格也没有 换行符号），不管是IE还是firefox，到达边界都会 自动换行。 但是有的情况，我们并不希望这样 在css中，可以使用white-space属性来让文本不换行，只需要给文本文字元素添加“white-space:nowrap;”样式即可。. white-space属性用于设置元素内的空白怎样处理，当normal: 默认。空白会被浏览器忽略。'} />
                </div>
              </div>
              <Button size='small' color={'primary'} style={{ fontSize: 10, width: 80 }}>续看10话</Button>
            </div>
          </div>
          <div style={{ paddingTop: 5 }}>
            <Collapse defaultActiveKey={['2']}>
              <Collapse.Panel key='1' title='简介'>
                {'2018-8-5 · 原文地址为： CSS禁止文字自动换行 当中文文字很长的时候（中间没有空格也没有 换行符号），不管是IE还是firefox，到达边界都会 自动换行。 但是有的情况，我们并不希望这样 在css中，可以使用white-space属性来让文本不换行，只需要给文本文字元素添加“white-space:nowrap;”样式即可。. white-space属性用于设置元素内的空白怎样处理，当normal: 默认。空白会被浏览器忽略。'}
              </Collapse.Panel>
              <Collapse.Panel key='2' title='漫画章节'>
                <Grid columns={4} gap={8}>
                  {
                    new Array(20).fill(0).map((item, index) =>
                      <Badge key={index} content='new' style={{ '--right': '35%', '--top': '10%' }}>
                        <Button
                          size='small'
                          style={{ fontSize: 10 }}
                          onClick={() => { navigate('/chapter') }}>
                          第{index + 1}话
                        </Button>
                      </Badge>)
                  }
                </Grid>
              </Collapse.Panel>
            </Collapse>
          </div>
        </div>
      </div>
    </>
  )
}
export default comic
