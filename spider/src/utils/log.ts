import * as chalk from 'chalk'
import { dateFormat } from './DateUtil'
import FileUtil from './FileUtil'

export default class Log {
  private static logPath = './log/'
  public static log(...contents: string[]) {
    Log.writeLogFile('info', ...contents)
    console.log(chalk.rgb(149, 176, 181).bold.bgRgb(40, 44, 52)(contents.join('\n')))
  }

  public static debug(...contents: string[]) {
    Log.writeLogFile('debug', ...contents)
    console.log(chalk.rgb(83, 166, 121).bold.bgRgb(40, 44, 52)(contents.join('\n')))
  }

  public static error(...contents: any[]) {
    const newContents = contents.map((item) => {
      if (item instanceof Error)
        return `${item.message}\n${item.stack}`
      return item
    })
    Log.writeLogFile('error', ...newContents)
    console.log(chalk.rgb(218, 106, 117).bold.bgRgb(40, 44, 52)(newContents.join('\n')))
  }

  public static warn(...contents: string[]) {
    Log.writeLogFile('warn', ...contents)
    console.log(chalk.rgb(198, 192, 111).bold.bgRgb(40, 44, 52)(contents.join('\n')))
  }

  public static info(...contents: string[]) {
    Log.log(...contents)
  }

  public static writeLogFile(level: string, ...contents: string[]) {
    const logFilePath = `${`${this.logPath + dateFormat(new Date(), 'YY.mm.dd')}/${level}`}.txt`
    const isExist = FileUtil.isExist(logFilePath)
    if (!isExist) {
      try {
        FileUtil.write(logFilePath, '')
      }
      catch (error) {
        console.error(`创建文件${logFilePath}失败！${error}`)
      }
    }

    const now = dateFormat(new Date())
    const newLine = `[${level}]\t${now}\t | ${contents.join(', ')}\n`

    try {
      FileUtil.append(logFilePath, newLine)
    }
    catch (error) {
      console.log(`记录日志失败,${error}`)
    }
  }
}
