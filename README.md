# <h1 align="center">Description</h1>
- This is a very simple document scanning emulator project done using python with <a href="https://opencv.org/">OpenCv</a>
- The backend implementation is done here mainly.




# <h1 align="center">Pre-config Instructions</h1>
- To set up <a href="https://github.com/astral-sh/uv.git">uv</a> in system which is a new python pkg manager written in Rust.

```bash
pip install uv
```
- Then to sync all the packages used in the project. 
```bash
cd Simple_Document_Scanner
uv sync #this will get the dependencies needed in the enviornment
```

# <h1 align="center">Run Instructions</h1>

```bash
uv run main.py --image <path>
```
- This will take the path of the image as the args and will then process the image which here would be scanning the image


