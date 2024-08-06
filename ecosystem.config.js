module.exports = {
    apps: [
      {
        name: "myapp",
        script: "./main.py",
        interpreter: "/usr/bin/python3", // Change this to the path of your Python interpreter
        interpreter_args: "-m venv /myenv/bin/python3", // Path to the Python interpreter within your virtual environment
        env: {
          // Environment variables
          PYTHONUNBUFFERED: "1",
        },
      },
    ],
  };
  