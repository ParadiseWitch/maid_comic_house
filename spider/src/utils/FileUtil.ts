import type { Stats } from 'fs'
import * as fs from 'fs'
import * as path from 'path'

export default class FileUtil {
  /**
   * 判断文件(夹)是否存在
   * @param dirname
   * @returns
   */
  public static isExist(dirname: string): boolean {
    try {
      fs.accessSync(dirname, fs.constants.F_OK)
    }
    catch (error) {
      return false
    }
    return true
  }

  public static read(dirname: string): string {
    if (!FileUtil.isExist(dirname))
      throw new Error(`文件不存在：${path}`)
    return fs.readFileSync(dirname, 'utf-8')
  }

  public static append(dirname: string, data: string) {
    fs.appendFileSync(dirname, data)
  }

  public static write(dirname: string, data: string) {
    if (!FileUtil.isExist(dirname))
      FileUtil.mkdir(dirname)
    fs.writeFileSync(dirname, data)
  }

  /**
   * 递归创建文件夹，会一直创建到以/结尾的最后一个文件夹, 因此使用时传入的路径要以/结尾，如
   * ```js
   * await FileUtil.mkdir('./a/')
   * await FileUtil.mkdir('./a/b/')
   * ```
   * @param dirname
   * @returns
   */
  public static mkdir(dirname: string) {
    dirname = dirname.replace(/\/[^\/]*$/, '')
    const isExist = FileUtil.isExist(dirname)
    if (!isExist) {
      FileUtil.mkdir(`${path.dirname(dirname)}/`)
      fs.mkdirSync(dirname)
    }
  }

  public static isFile(dirname: string): boolean {
    return FileUtil.getInfo(dirname).isFile()
  }

  public static getInfo(dirname: string): Stats {
    if (!FileUtil.isExist(dirname))
      throw new Error(`${dirname} 文件/文件夹不存在！`)
    return fs.statSync(dirname)
  }

  public static getFiles(dirname: string): string[] {
    if (!FileUtil.isExist(dirname))
      throw new Error(`${dirname} 文件/文件夹不存在！`)
    return fs.readdirSync(dirname)
  }
}
