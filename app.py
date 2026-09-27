import streamlit as st
from PIL import Image
import requests

# 1. Page settings & main titles
st.set_page_config(page_title="Tomato AI Doctor", page_icon="🍅", layout="wide")
st.title("🍅 Tomato Leaf Disease Detector & Care Assistant")
st.write("Upload an image of a tomato leaf to detect disease patterns, possible causes, and general treatment suggestions.")

# 2. Complete educational database matching dataset classes to insights
causes_map = {
    "Tomato___Bacterial_spot": "Infestation of Xanthomonas bacteria, typically spread via wind-driven rain splash.",
    "Tomato___Early_blight": "Infection triggered by the fungus Alternaria solani, often flourishing in high humidity.",
    "Tomato___Late_blight": "Rapid oomycete infection (Phytophthora infestans) that thrives in cool, damp weather conditions.",
    "Tomato___Leaf_Mold": "Caused by the fungus Passalora fulva, which thrives in high humidity and stagnant air.",
    "Tomato___Septoria_leaf_spot": "Septoria lycopersici fungus, which overwinters on old plant debris.",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Infestation of microscopic spider mites, multiplying rapidly in hot, dry weather.",
    "Tomato___Target_Spot": "Fungus Corynespora cassiicola, forming dark concentric rings on leaves.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Viral infection transmitted by whiteflies, causing stunted, upward-curling leaves.",
    "Tomato___Tomato_mosaic_virus": "Highly contagious Tobamovirus infection, spread mechanically by hands or tools.",
    "Tomato___Healthy": "The leaf appears structurally sound and exhibits optimal photosynthetic characteristics."
}

cures_map = {
    "Tomato___Bacterial_spot": ["Avoid overhead watering.", "Apply copper-mancozeb sprays.", "Sanitize tools."],
    "Tomato___Early_blight": ["Prune lower foliage.", "Apply copper-based preventative fungicides.", "Use drip irrigation."],
    "Tomato___Late_blight": ["Destroy infected plants immediately.", "Apply protectant fungicides.", "Plant resistant varieties."],
    "Tomato___Leaf_Mold": ["Increase ventilation.", "Keep humidity below 85%.", "Apply copper fungicides."],
    "Tomato___Septoria_leaf_spot": ["Clean old crop debris.", "Mulch base to stop soil splash.", "Apply fungicides early."],
    "Tomato___Spider_mites Two-spotted_spider_mite": ["Spray leaf undersides with water.", "Introduce predatory mites.", "Use insecticidal soaps."],
    "Tomato___Target_Spot": ["Ensure wide plant spacing.", "Prune lowest branches.", "Use chlorothalonil sprays."],
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": ["Use floating row covers.", "Hang yellow sticky traps.", "Remove infected plants immediately."],
    "Tomato___Tomato_mosaic_virus": ["Sanitize tools in disinfectant.", "Discard infected crops.", "Use certified clean seeds."],
    "Tomato___Healthy": ["Maintain consistent soil moisture.", "Ensure regular baseline feeding.", "Monitor lower foliage routinely."]
}

# 3. Create the clean File Uploader
uploaded_file = st.file_uploader("Select a tomato leaf image...", type=["jpg", "jpeg", "png", "JPG", "JPEG", "PNG", "jfif", "JFIF"])

if uploaded_file is not None:
    # Save image temporarily inside the cloud folder
    img_path = "temp_uploaded_leaf.jpg"
    image = Image.open(uploaded_file)
    image.save(img_path)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Uploaded Foliage")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🤖 AI Diagnosis Panel")
        
        with st.spinner("Streaming image to high-speed cloud model server..."):
            # 📋 CRUCIAL: Make sure your exact API key is pasted right here!
            api_key = "ycYp9oLtZ7Amx7n0G90L"
            url = f"https://roboflow.com{api_key}"
            
            try:
                with open(img_path, "rb") as image_file:
                    response = requests.post(url, files={"file": image_file})
                predictions = response.json().get("predictions", [])
                
                if not predictions:
                    st.info("🔍 AI Analysis: No clear plant disease anomalies recognized on this image input sample.")
                
                seen_classes = set()
                for pred in predictions:
                    class_name = pred.get("class")
                    confidence = pred.get("confidence", 0) * 100
                    
                    if class_name in seen_classes or confidence < 20:
                        continue
                    seen_classes.add(class_name)
                    
                    # Style out clean markdown blocks for visual user feedback
                    st.markdown(f"### 📋 Condition Detected: **{class_name.replace('___', ' - ')}** ({confidence:.1f}% Confidence)")
                    
                    if class_name in causes_map:
                        st.markdown(f"**🔍 Possible Causes:**\n* {causes_map[class_name]}")
                        st.markdown("**🌱 General Management Options:**")
                        for cure in cures_map[class_name]:
                            st.markdown(f" * ☑️ {cure}")
                    st.markdown("---")
            except Exception as api_err:
                st.error(f"Cloud API link lost: {api_err}")

st.write("⚠️ **General Scope Notice:** Diagnostic classifications reflect general agricultural consensus guidelines for academic project exhibitions.")
