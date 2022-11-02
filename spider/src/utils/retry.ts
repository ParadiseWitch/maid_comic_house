import Log from './log'

export const delay = (delayTimes = 1000) => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(null)
    }, delayTimes)
  })
}
const retry = async <R>(fn: () => R, num: number = 3, delayTimes = 500) => {
  let i = num
  let ret: R
  while (i > 0) {
    try {
      ret = await fn()
    } catch (e) {
      i--
      Log.debug(`重试第${num - i}次失败！`, e)
      if (i <= 0) {
        Log.debug(`总共重试${num}次失败！`)
        throw e
      }
      await delay(delayTimes)
      continue
    }
    Log.debug(`重试第${num - i + 1}次成功！`)
    break
  }
  return ret
}

export default retry

