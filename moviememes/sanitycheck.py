import PIL, requests, subprocess, sys, traceback

def python_version_check():
    print("Checking Python version...")
    print("Running on:", sys.version)
    print("OK")

def requests_check():
    print("Testing requests library...")
    response = requests.get('http://example.org')
    if response.status_code == 200:
        print("OK")
    else:
        print(f"ERROR: Example query returned non-200 code: {response.status_code}")

def ffmpeg_check():
    print("Testing ffmpeg availability...")
    try:
        output = subprocess.check_output(['ffmpeg', '-version'])
        print(output)
        print("OK")
    except Exception as e:
        print("ERROR running `ffmpeg -version`")
        traceback.print_exc()

def pillow_check():
    print("Testing Pillow availability...")
    print("Using: ", PIL.PILLOW_VERSION)
    print("OK")

SANITY_CHECKS = [
    python_version_check,
    pillow_check,
    requests_check,
    ffmpeg_check,
]

def run_sanity_checks():
    for sanity_check in SANITY_CHECKS:
        sanity_check()
        print()
    print("Sanity checks complete")
