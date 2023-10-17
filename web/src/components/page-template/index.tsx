import './index.css'
import { NavBar } from 'antd-mobile'
import MaidTabBar from '/@/components/tabbar'
import type { PropsWithChildren } from 'react'

type Props = PropsWithChildren<{
  header?: JSX.Element | String
  footer?: JSX.Element
}>

const pageTemplate: React.FC<Props> = ({ header, footer, children }) => {
  header = (header === undefined) ? <NavBar back={null}> Maid漫画屋☕ </NavBar> : header
  footer = (footer === undefined) ? <MaidTabBar/> : footer

  if (typeof header == 'string') {
    header = (
      <NavBar back={null}>
        {header}
      </NavBar>
    )
  }

  return (
    <>
      <div className="app">
        <div className="top">
          {header}
        </div>
        <div className="body">
          {children}
        </div>
        <div className="bottom">
          {footer}
        </div>
      </div>
    </>
  )
}

export default pageTemplate
