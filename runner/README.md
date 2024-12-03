# Mobly test runner

The Mobly test runner is a tool that serves as the entry point for executing a
given Mobly test or suite. It is designed with a focus on simplicity and 
flexibility. 

The runner analyzes the contents of a Mobly test package, performs test 
environment setup/teardown, and executes the test.

As a basic usage example:

```bash
python3 mobly_runner.py -p my_test_package.zip 
```

executes the Mobly test binary contained in `my_test_package.zip`.

For more details, please refer to the CLI options in `python mobly_runner.py -h`.
