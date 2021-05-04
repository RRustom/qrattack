# qrattack

## Setup

1. `pipenv install`
2. `brew install cmake`
3. `git clone https://github.com/nu-book/zxing-cpp.git`
4. `cd zxingcpp`
5. `cmake CMakeLists.txt`
6. `cd ..`
7. `python generate_malicious_qr.py` to test it

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

### Next
1. Write tests
2. Add color to QR code diff
3. Find a faster way to get QR code info (ecc/version/mask)
4. Improve URL generation (random vs brute force) + multiprocessing: https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing/
5. More robust image scanning
6. Add camera scanner
7. Generate any payload
8. Investigate tampering techniques
9. Setup script

### Research
1. How to know if people don't scan in restaurant?
2. Setup infra for dorm + restaurant tests
3. Get in touch with restaruants @RRustom
