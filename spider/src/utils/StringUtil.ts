const trim = (str: string): string => {
  return str.replace(/(^\s*)|(\s*$)/g, '')
}

export {
  trim,
}
