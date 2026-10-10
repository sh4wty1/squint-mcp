// Runs in the page and returns how wide it scrolls: the scroll width of the element
// that scrolls the viewport, which is `html`, or `body` in quirks mode. A page in
// quirks mode whose `body` is its own scroll container has no such element, and
// `html` is read instead.
() => (document.scrollingElement ?? document.documentElement).scrollWidth;
