# qrattack

The final paper can be found [here](https://courses.csail.mit.edu/6.857/2021/projects/Pence-Rustom-McAllister.pdf)

## Setup

1. `pipenv install`
2. `brew install cmake`
3. `git clone https://github.com/nu-book/zxing-cpp.git`
4. Rename `zxing-cpp` to `zxingcpp` then `cd zxingcpp`
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
7. Setup backend service + HTTP server
8. Generate any payload
9. Investigate tampering techniques
10. Setup script

### Research
1. How to know if people don't scan in restaurant?
2. Setup infra for dorm + restaurant tests
3. Get in touch with restaruants @RRustom

## TODO 07/5/2021
### Experiment
1. Get in touch with restaurants in Central/Kendall/Harvard this weekend
2. Set up infra restaurant + dorm testing.
	- dorm:
		- talk to people in dorms
		- design poster
		- ideas
			1. Google form with info about QR codes/random questions
			2. set up a server and count the number of visits
		- distribute posters
	- restaurant:
		- talk to restaurants
		- setup server and count visits
		- Talk to LAs about how to best count baseline # QR scans
### Code
1. Work on decoding optimizations @RRustom


## Resources
- https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
- https://github.com/lincolnloop/python-qrcode
- https://www.youtube.com/watch?v=qnq0UfOUTlM
- https://github.com/lincolnloop/python-qrcode
