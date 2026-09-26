from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from markitdown import MarkItDown
import tempfile
import os

app = FastAPI(title="MarkItDown Converter API")
md = MarkItDown()

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.post("/api/convert")
async def convert_to_markdown(file: UploadFile = File(...)):
    try:
        suffix = f".{file.filename.split('.')[-1]}" if '.' in file.filename else ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        result = md.convert(temp_file_path)

        os.remove(temp_file_path)

        return {
            "filename": file.filename,
            "markdown_content": result.text_content
        }

    except Exception as e:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")