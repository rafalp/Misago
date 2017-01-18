const ytRegExp = new RegExp('^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*');

export class OneBox {
  constructor() {
    this._youtube = {};
  }

  // jshint ignore:start
  render = (domnode) => {
    if (!domnode) return;

    const anchors = domnode.querySelectorAll('p>a');
    for(let i = 0; i < anchors.length; i++ ) {
      const a = anchors[i];
      const p = a.parentNode;
      const onlyChild = p.children.length === 1;

      if (!this._youtube[a.href]) {
        this._youtube[a.href] = parseYoutubeUrl(a.href);
      }

      const youtubeMovie = this._youtube[a.href];
      if (onlyChild && !!youtubeMovie && youtubeMovie.data !== false) {
        this.swapYoutubePlayer(a, youtubeMovie);
      }
    }
  };
  // jshint ignore:end

  swapYoutubePlayer(element, youtube) {
    let url = 'https://www.youtube.com/embed/';
    url += youtube.video;
    url += '?rel=0';
    if (youtube.start) {
      url += '&start=' + youtube.start;
    }

    $(element).replaceWith($('<iframe width="560" height="315" src="' + url + '" frameborder="0" allowfullscreen></iframe>'));
  }
}

export default new OneBox();

export function parseYoutubeUrl(url) {
  const cleanedUrl = cleanUrl(url);
  const video = getVideoIdFromUrl(cleanedUrl);

  if (!video) return null;

  let start = 0;
  if (cleanedUrl.indexOf('?') > 0){
    const query = cleanedUrl.substr(cleanedUrl.indexOf('?') + 1);
    const timebit = query.split('&').filter((i) => {
      return i.substr(0, 2) === 't=';
    })[0];

    if (timebit) {
      const bits = timebit.substr(2).split('m');
      if (bits[0].substr(-1) === 's') {
        start += parseInt(bits[0].substr(0, bits[0].length - 1));
      } else {
        start += parseInt(bits[0]) * 60;
        if (!!bits[1] && bits[1].substr(-1) === 's') {
          start += parseInt(bits[1].substr(0, bits[1].length - 1));
        }
      }
    }
  }

  return {
    start,
    video
  };
}

export function cleanUrl(url) {
  let clean = url;

  if (url.substr(0, 8) === 'https://') {
    clean = clean.substr(8);
  } else if (url.substr(0, 7) === 'http://') {
    clean = clean.substr(7);
  }

  if (clean.substr(0, 4) === 'www.') {
    clean = clean.substr(4);
  }

  return clean;
}

export function getVideoIdFromUrl(url) {
  const video = url.match(ytRegExp);
  if (video) {
    return video[1];
  }
  return null;
}