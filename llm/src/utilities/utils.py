from temporalio import activity

@activity.defn
async def read_file_as_string(filepath: str) -> str:
    try:
        with open(filepath, 'r') as file:
            content = file.read().strip()  # strip to remove unnecessary whitespace
            if not content:
                raise ValueError("File is empty")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {filepath}: {str(e)}")
