#!/usr/bin/env python3
"""Reroll rejected teacher stills. CUDA 0 = 3090."""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from pathlib import Path
import torch
from compel import Compel, ReturnedEmbeddingsType
from diffusers import StableDiffusionXLPipeline
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "assets" / "teachers"

NEG = (
    "cartoon, illustration, cgi, plastic skin, deformed face, extra fingers, "
    "text, letters, words, writing, watermark, logo, signature, alphabet, "
    "numbers, caption, nsfw, child, teen, underage, misspelled"
)

JOBS = [
    dict(
        id="sd2",
        seed=212,
        prompt=(
            "passport-style square photograph of a Polish man in his early 40s, "
            "short dark hair, light stubble, round glasses, navy shirt, "
            "BLANK dark chalkboard behind with NO writing and NO letters, "
            "only faint chalk dust, photorealistic, 85mm, natural light, "
            "calm expression, looking at camera"
        ),
    ),
    dict(
        id="sd6",
        seed=616,
        prompt=(
            "passport-style square photograph of a Polish man in his mid-30s, "
            "short blond hair, athletic, grey polo shirt, "
            "indoor school gymnasium clearly visible: basketball hoop and wooden wall bars, "
            "photorealistic, 85mm, easy smile, looking at camera, no text"
        ),
    ),
]


def main():
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "SG161222/RealVisXL_V5.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    pipe.to("cuda")
    pipe.vae.enable_slicing()
    compel = Compel(
        tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
        text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
        returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
        requires_pooled=[False, True],
        device="cuda",
    )
    for t in JOBS:
        cond, pooled = compel(t["prompt"])
        ncond, npooled = compel(NEG)
        gen = torch.Generator(device="cuda").manual_seed(t["seed"])
        img = pipe(
            prompt_embeds=cond,
            pooled_prompt_embeds=pooled,
            negative_prompt_embeds=ncond,
            negative_pooled_prompt_embeds=npooled,
            width=1024,
            height=1024,
            num_inference_steps=28,
            guidance_scale=7.0,
            generator=gen,
        ).images[0]
        dest = OUT / f"{t['id']}.webp"
        img.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS).save(dest, "WEBP", quality=86)
        print("wrote", dest)


if __name__ == "__main__":
    main()
