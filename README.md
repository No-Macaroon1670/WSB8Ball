# 🎱 WSB Magic 8-Ball

**[▶️ Play it here — no-macaroon1670.github.io/WSB8Ball](https://no-macaroon1670.github.io/WSB8Ball/)**

A free online **Magic 8-Ball for WallStreetBets degens**. Tap the ball to shake it and get one of **27 WSB-themed answers** — from *"To the moon!"* to *"GUH"* to *"Ask wife's boyfriend"*.

No ads. No tracking. No signup. Nothing for sale. Just a fidget toy.

![WSB Magic 8-Ball demo — tap to shake for a new answer](demo.gif)

## Features

- **27 WallStreetBets answers** — balanced 11 bullish / 10 bearish / 6 hazy
- **Tap, click, or press Space** to shake
- **Zero dependencies** — vanilla HTML, CSS, and JavaScript. No frameworks, no CDN, no build step, no backend
- **Works offline** — [`magic8ball.html`](magic8ball.html) is a single self-contained file with the image inlined as a data URI. Download it and double-click
- **Responsive** — scales to any screen, phone or desktop

## The answers

**Bullish 🚀** — To the moon! · YOLO · Stonks only go up · Buy the dip · Tendies incoming · Calls will print · Diamond hands · Apes strong together · We're so back · Buy everything · Generational wealth

**Bearish 📉** — GUH · Margin call · Priced in · Bagholder confirmed · Paper hands · Puts will print · Theta gang wins · Freak the fuck out · Sell everything · It's fucking over

**Hazy 🤷** — Ask wife's boyfriend · Sir, this is a Wendy's · Market manipulation · Inverse Cramer · Check Robinhood later · Wendy's Parking Lot

## Run it locally

Clone and open `index.html` in any browser — that's it, there's no build step:

```bash
git clone https://github.com/No-Macaroon1670/WSB8Ball.git
```

Or just download [`magic8ball.html`](magic8ball.html) and double-click it. It works with no internet connection.

## Adding your own phrases

Open [`index.html`](index.html) and add a line to the `PHRASES` array:

```js
const PHRASES = [
  "To the moon!",
  "Your phrase here",
];
```

Text auto-shrinks to fit the ball's window, so long phrases are fine.

## Not financial advice

It's a random number generator with a rocket emoji attached. Obviously do not make trades based on it.

## License

MIT — see [LICENSE](LICENSE).
