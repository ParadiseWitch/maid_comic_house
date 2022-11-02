import type Chapter from '../chapter'

export class Comic {
  id = ''
  title = '暂无标题'
  cover = ''
  desc = ''
  chapterNum = 0
  alreadyRead = 0
  chapters: Chapter[] = []

  constructor(id: string, title: string, cover: string, chapters: Chapter[]) {
    this.id = id
    this.title = title
    this.cover = cover
    this.chapters = chapters
  }

  hasNotReadChapter() {
    return this.alreadyRead < this.chapterNum
  }
}
