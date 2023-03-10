const ytRegExp = new RegExp(
  "^.*(?:(?:youtu.be/|v/|vi/|u/w/|embed/)|(?:(?:watch)??v(?:i)?=|&v(?:i)?=))([^#&?]*).*"
)

export class OneBox {
  constructor() {
    this._youtube = {}
  }

  render = (element) => {
    if (!element) return
    this.highlightCode(element)
    this.embedYoutubePlayers(element)
  }

  highlightCode(element) {
    import("highlight").then(({ default: hljs }) => {
      const codeblocks = element.querySelectorAll("pre>code")
      for (let i = 0; i < codeblocks.length; i++) {
        hljs.highlightElement(codeblocks[i])
      }
    })
  }

  embedYoutubePlayers(element) {
    const anchors = element.querySelectorAll("p>a")
    for (let i = 0; i < anchors.length; i++) {
      const a = anchors[i]
      const p = a.parentNode
      const onlyChild = p.childNodes.length === 1

      if (!this._youtube[a.href]) {
        this._youtube[a.href] = parseYoutubeUrl(a.href)
      }

      const youtubeMovie = this._youtube[a.href]
      if (onlyChild && !!youtubeMovie && youtubeMovie.data !== false) {
        this.swapYoutubePlayer(a, youtubeMovie)
      }
    }
  }

  swapYoutubePlayer(element, youtube) {
    let url = "https://www.youtube.com/embed/"
    url += youtube.video
    url += "?feature=oembed"
    if (youtube.start) {
      url += "&start=" + youtube.start
    }

    const player = $(
      '<iframe class="embed-responsive-item" frameborder="0" ' +
        'src="' +
        url +
        '" ' +
        'allow="encrypted-media; gyroscope; picture-in-picture" ' +
        "allowfullscreen></iframe>"
    )
    $(element).replaceWith(player)
    player.wrap('<div class="embed-responsive embed-responsive-16by9"></div>')
  }
}

export default new OneBox()

export function parseYoutubeUrl(url) {
  const cleanedUrl = cleanUrl(url)
  const video = getVideoIdFromUrl(cleanedUrl)

  if (!video) return null

  let start = 0
  if (cleanedUrl.indexOf("?") > 0) {
    const query = cleanedUrl.substr(cleanedUrl.indexOf("?") + 1)
    const timebit = query.split("&").filter((i) => {
      return i.substr(0, 2) === "t="
    })[0]

    if (timebit) {
      const bits = timebit.substr(2).split("m")
      if (bits[0].substr(-1) === "s") {
        start += parseInt(bits[0].substr(0, bits[0].length - 1))
      } else {
        start += parseInt(bits[0]) * 60
        if (!!bits[1] && bits[1].substr(-1) === "s") {
          start += parseInt(bits[1].substr(0, bits[1].length - 1))
        }
      }
    }
  }

  return {
    start,
    video,
  }
}

export function cleanUrl(url) {
  let clean = url

  if (url.substr(0, 8) === "https://") {
    clean = clean.substr(8)
  } else if (url.substr(0, 7) === "http://") {
    clean = clean.substr(7)
  }

  if (clean.substr(0, 4) === "www.") {
    clean = clean.substr(4)
  }

  return clean
}

export function getVideoIdFromUrl(url) {
  if (url.indexOf("youtu") === -1) return null

  const video = url.match(ytRegExp)
  if (video) {
    return video[1]
  }
  return null
}
