# Import required libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# Initialize FastAPI app
app = FastAPI()

# Load the BiRefNet model
device = "cuda" if torch.cuda.is_available() else "cpu"
birefnet = AutoModelForImageSegmentation.from_pretrained(
    "zhengpeng7/BiRefNet", trust_remote_code=True
)
birefnet.to(device)
birefnet.eval()

# Image transformation
transform_image = transforms.Compose(
    [
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def refine_foreground(image, mask):
    """
    Refine the foreground of the image using the mask.
    """
    # Convert mask to RGBA
    mask = mask.convert("L")
    mask = mask.point(lambda p: p > 128 and 255)  # Binarize the mask
    mask = mask.convert("RGBA")

    # Apply the mask to the image
    image_rgba = image.convert("RGBA")
    image_masked = Image.composite(
        image_rgba, Image.new("RGBA", image.size, (0, 0, 0, 0)), mask
    )
    return image_masked


@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    """
    API endpoint to process an image using BiRefNet.
    Returns only the refined foreground image (subject.png).
    """
    # Save the uploaded file temporarily
    with open("temp_image.jpg", "wb") as buffer:
        buffer.write(await file.read())

    # Load and process the image
    image = Image.open("temp_image.jpg")
    input_images = transform_image(image).unsqueeze(0).to(device)

    # Prediction
    with torch.no_grad():
        preds = birefnet(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()

    # Save the results
    pred_pil = transforms.ToPILImage()(pred)
    pred_pil = pred_pil.resize(image.size)

    # Refine the foreground and save the subject image
    image_masked = refine_foreground(image, pred_pil)
    image_masked.putalpha(pred_pil)
    image_masked.save("subject.png")

    # Return only the subject image
    return FileResponse("subject.png", media_type="image/png")


# Run the FastAPI app
if __name__ == "_main_":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0",port=8000)