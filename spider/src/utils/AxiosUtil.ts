import * as https from 'https'
import * as fs from 'fs'
import axios from 'axios'
import FileUtil from './FileUtil'

const download = async (src: string, dirname: string) => {
  await axios.get(src, {
    responseType: 'stream',
    // FIXME 忽略SSL证书，不校验https证书，可能有风险
    httpsAgent: new https.Agent({
      rejectUnauthorized: false,
    }),
    timeout: 30000,
  }).then((res) => {
    // FileUtil.mkdir(dirname)
    res.data.pipe(fs.createWriteStream(dirname))
  }).catch((err) => {
    throw new Error(`文件下载失败: ${src}\n${err}`)
  })
}

export { download }

