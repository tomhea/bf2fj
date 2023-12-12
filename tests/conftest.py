def pytest_addoption(parser):
    parser.addoption("--compile-only", action="store_true",
                     help="If specified, just compile the brainfuck files, and don't run the compiled flipjump.")
