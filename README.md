# qrattack

## Setup

1. `pipenv install`
2. `brew install zbar`

## TODO
### Friday 04/23
1. QR class (QrCode wrapper) @RRustom
2. Test code @RRustom @Eric
3. Work more on URLs, simpler verify_url @Eric
4. Write tests @Lindsey
5. Run `generate_malicious_qr()` @RRustom

### Friday 04/30
1. URL -> any payload? (alphanumeric -> binary)
2. Exploring types of attacks
  - minimum distance tampering?
  - changing payload
  - changing url


TODO Rami:
- use https://github.com/ewino/qreader to get EC level from qr code
- finish verify_solution
- generate image that shows which codes to change
DONE - generate from matrix
- run full pass

Research:
- experiment with normal vs qr codes with modifications, see what people do
- survey restaurants/coffee shops/bars about their qr code usage
- deploy in restaurants, see how many people fall for it

## Resources
- https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
- https://github.com/lincolnloop/python-qrcode
- https://www.youtube.com/watch?v=qnq0UfOUTlM
- https://github.com/lincolnloop/python-qrcode
